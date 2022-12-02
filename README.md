# OpenWeatherMap
Program to display weather in an easy way.

## Program Description
Application using API from <https://openweathermap.org/> in order to take weather parameters like temperature, clouds, wind, etc.
In our case, we use only temperature and then extract max, min, and avg. One can choose any place on the earth by inserting arguments latitude and longitude (default is K2 mountain).
To find the right lat. and long. may use the website: <https://www.latlong.net/>

For Example Rybnik
```
Weather = CheckWeather(50.089722,18.530880)
```
The program saves all data on the database using MySQL.
The weather is saved in one record. The record is replaced if the same parameters lat. and lon already exist.

![alt text](https://i.postimg.cc/kGwtKKxC/sql.jpg)

To display a figure use the library matplotlib.The weather is forecast for 5 days every 3 hours.
![alt text](https://i.postimg.cc/ncGg6z1D/matplotlib.jpg)

## How to use
1. Due to the program saving to MySQL the first step is to install database from <https://www.mysql.com/>
2. Create database using code :
```
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yourpassword"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE Weather_DB")
```
3. Register on https://openweathermap.org/ and take API KEY.
4. Create a new files .env and past your API KEY
![alt text](https://i.postimg.cc/dt68ykFn/API.png)




