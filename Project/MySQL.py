import mysql.connector
import json

# Before first connecting one have to create a DataBase "Weather_DB"
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="Weather_DB"
)

mycursor = mydb.cursor()

class SQL():

    def Create_DataBase_And_Table(self):

        #  create sql table
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS  Weather "
                              "(id INT AUTO_INCREMENT PRIMARY KEY ,"
                              "LAT VARCHAR(1000),"
                              "LON VARCHAR(1000),"
                              "DATE VARCHAR(1000),"
                              "TEMP VARCHAR(1000),"
                              "MAX FLOAT(10),"
                              "AVG FLOAT(10) ,"
                              "MIN FLOAT(10) )")



    def Save_To_Sql(self,data,temp,lat,lon,max_temp, avg_temp, min_temp):

        # change lists to string in order to save to sql
        data = json.dumps(data)
        temp = json.dumps(temp)

        # parameters to sql
        adr = (lat, lon)
        val = [lat, lon, data, temp, max_temp, avg_temp, min_temp]

        # sql commends
        sql_insert = "INSERT INTO Weather (LAT, LON ,DATE,TEMP, MAX , AVG ,MIN) VALUES (%s, %s ,%s , %s , %s, %s , %s)"
        sql_delete = "DELETE FROM weather WHERE LAT =%s AND LON =%s"

        # if DB contains the same lat and lon value the record is replaced
        sql_select = f"SELECT * FROM weather WHERE LAT ={lat} AND LON ={lon}"

        mycursor.execute(sql_select)
        myresult = mycursor.fetchall()


        if len(myresult) != 0:
          # Delete old record and save a new one
          mycursor.execute(sql_delete, adr)
          mycursor.execute(sql_insert, val)
        else:
          mycursor.execute(sql_insert, val)

        mydb.commit()

    def SearchInDb(self,lat,lon):

        # Extract data from SQL , and return
        sql_select_Data = f"SELECT DATE,TEMP,MAX , AVG ,MIN FROM weather WHERE LAT ={lat} AND LON ={lon}"
        mycursor.execute(sql_select_Data)
        myresult = mycursor.fetchall()
        return myresult

    def FindPlace(self,lat,lon):

        # Extract data from SQL , and return
        sql_select_Data = f"SELECT DATE,TEMP,MAX , AVG ,MIN FROM weather WHERE LAT ={lat} AND LON ={lon}"
        mycursor.execute(sql_select_Data)
        myresult = mycursor.fetchall()
        # cleaning data
        date = myresult[0][0].replace('[', '').replace(']', '').replace('"', '').split(', ')
        temp = myresult[0][1].replace('[', '').replace(']', '').split(',')
        return date,temp