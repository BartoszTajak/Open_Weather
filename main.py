import mysql.connector
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

# loading config files  and  parameters like API_KEY
load_dotenv()
API_KEY = os.getenv("API_KEY")



class CheckWeather:
  '''


  '''

  def __init__(self,lat=35.88,lon=76.51):
    self.lat = lat
    self.lon = lon
    self.API()
    self.Create_DataBase_And_Table()
    self.Save_To_Sql()
    self.Weather_Figure()



  def API(self):
    place = {"lat": self.lat, "lon": self.lon}

    # link to API on openweathermap
    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={place["lat"]}&lon={place["lon"]}&APPID={API_KEY}&units=metric')
    p = response.json()

    # Adding all weather's parameters to empty list
    mylist = []
    for i in p["list"]:
      temp = i['main']['temp']
      pressure = i['main']['pressure']
      clouds = i['clouds']['all']
      date = i['dt_txt']
      data = [temp, pressure, clouds, date]
      mylist.append(data)




    # create DataFrame and convert data
    df = pd.DataFrame(data=np.array(mylist), columns=['temp', 'pressure', 'clouds', 'date'])
    df['temp'] = df['temp'].apply(lambda x: float(x))
    df.set_index(['date'], inplace=True)

    data = [i[5:-3:] for i in list(df.index.values)]
    self.data = [i.replace(' ', '   ') for i in data]
    self.temp = df['temp'].tolist()

    # Variable : temp. max,avg,min
    self.max_temp = round(max(self.temp),2)
    self.avg_temp = round(np.mean(self.temp),2)
    self.min_temp = round(min(self.temp),2)


  def Create_DataBase_And_Table(self):

    # Before first connecting one have to create a DataBase "Weather_DB"
    self.mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="yourpassword",
      database="Weather_DB"
    )

    self.mycursor = self.mydb.cursor()

    # create sql table
    self.mycursor.execute(f"CREATE TABLE IF NOT EXISTS  Weather "
                     "(id INT AUTO_INCREMENT PRIMARY KEY ,"
                     "LAT VARCHAR(1000),"
                     "LON VARCHAR(1000),"
                     "DATE VARCHAR(1000),"
                     "TEMP VARCHAR(1000),"
                     "MAX FLOAT(10),"
                     "AVG FLOAT(10) ,"
                     "MIN FLOAT(10) )")



  def Save_To_Sql(self):

    # change lists to string in order to save to sql
    self.data = json.dumps(self.data)
    self.temp = json.dumps(self.temp)

    # parameters to sql
    adr = (self.lat, self.lon)
    val = [self.lat, self.lon, self.data, self.temp, self.max_temp, self.avg_temp, self.min_temp]

    # sql commends
    sql_insert = "INSERT INTO Weather (LAT, LON ,DATE,TEMP, MAX , AVG ,MIN) VALUES (%s, %s ,%s , %s , %s, %s , %s)"
    sql_delete = "DELETE FROM weather WHERE LAT =%s AND LON =%s"


    # if DB contains the same lat and lon value the record is replaced
    self.sql_select = f"SELECT * FROM weather WHERE LAT ={self.lat} AND LON ={self.lon}"
    self.mycursor.execute(self.sql_select)
    myresult = self.mycursor.fetchall()


    if len(myresult) != 0:
      # Delete old record and save a new one
      self.mycursor.execute(sql_delete, adr)
      self.mycursor.execute(sql_insert, val)
    else:
      self.mycursor.execute(sql_insert, val)
    self.mydb.commit()

  def Weather_Figure(self):

    # Extract data from SQL
    sql_select_Data = f"SELECT DATE,TEMP,MAX , AVG ,MIN FROM weather WHERE LAT ={self.lat} AND LON ={self.lon}"
    self.mycursor.execute(sql_select_Data)
    myresult = self.mycursor.fetchall()

    # cleaning data
    date = myresult[0][0].replace('[','').replace(']','').replace('"','').split(', ')
    temp = myresult[0][1].replace('[','').replace(']','').split(',')

    temp_lista=[]
    for i in temp:
      temp_lista.append(float(i))



    geolocator = Nominatim(user_agent="usr")
    point = self.lat,self.lon
    location = str(geolocator.reverse(point)).split(',')[1::]




    # Parameters  for diagram
    plt.figure(figsize=(28, 20))
    plt.grid(linewidth=0.1, color = 'black')
    plt.plot(date, temp_lista,linewidth=2)
    plt.xticks(fontsize=8,rotation=90)
    plt.ylabel('Temperature [C]',fontsize = 15)
    plt.title(f"Weather for  {location}" )
    # Dictionary in order to create a diagram  contains max,avg,min
    Dic_temp = {'Max temp = ' : myresult[0][2] ,'Avg temp = ' : myresult[0][3] , 'Min temp = ' : myresult[0][4] }


    for item in Dic_temp:
      plt.axhline(Dic_temp[item] , color = 'black',label= f'{item} = {Dic_temp[item]}',linewidth=1)
      plt.text(len(date)+1.2,Dic_temp[item], f'{item} {Dic_temp[item]}',color= 'black',alpha=1)

    plt.show()

p = CheckWeather()


