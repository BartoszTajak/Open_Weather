import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from Project.MySQL import *


# loading config files  and  parameters like API_KEY
load_dotenv()
API_KEY = os.getenv("API_KEY")

# creating object to make the table
p = SQL()
p.Create_DataBase_And_Table()



class CheckWeather:
  '''
  Put values lat. and lon.  as arguments (int or float) and check the weather for the next 5 days.
  Lat. vaule must be in range -90<lat<90 and  lon. -180<lon<180
  '''

  def __init__(self,lat=35.88,lon=76.51):
    self.lat = lat
    self.lon = lon
    # checking if both values lat. and lon. are int or float
    if not all([isinstance(self.lat,(int, float)) , isinstance(self.lon,(int, float))]):
      raise TypeError("Only integers and float  are allowed")

    # checking the range of value
    if abs(self.lat) >= 90 or abs(self.lon) >= 180:
      raise TabError('Incorrect value, -90<lat<90 and -180<lon<180')

    self.API()
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


    # createing  DataFrame and convert data
    df = pd.DataFrame(data=np.array(mylist), columns=['temp', 'pressure', 'clouds', 'date'])
    df['temp'] = df['temp'].apply(lambda x: float(x))
    df.set_index(['date'], inplace=True)

    data = [i[5:-3:] for i in list(df.index.values)]
    data = [i.replace(' ', '   ') for i in data]
    temp = df['temp'].tolist()

    # Variable : temp. max,avg,min
    max_temp = round(max(temp),2)
    avg_temp = round(np.mean(temp),2)
    min_temp = round(min(temp),2)

    # creating object to insert values
    p = SQL()
    p.Save_To_Sql(data,temp,self.lat,self.lon,max_temp,avg_temp,min_temp)

  def Weather_Figure(self):

    #  creating the object which takes data from SQL
    p = SQL()
    myresult = p.SearchInDb(self.lat,self.lon)

    # cleaning data
    date = myresult[0][0].replace('[','').replace(']','').replace('"','').split(', ')
    temp = myresult[0][1].replace('[','').replace(']','').split(',')

    temp_lista=[]
    for i in temp:
      temp_lista.append(float(i))

    # library to check names of positions on the world
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
    # displaying diagram
    plt.show()

if __name__ == '__main__':
  Weather = CheckWeather()


