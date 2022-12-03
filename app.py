from Project.main import CheckWeather
from Project.MySQL import SQL


# create the object to execute whole program with arguments or not
p =CheckWeather()


# just check temerature based on lat ,lon
p = SQL()
results = p.FindPlace(35.88,76.51)
for i in zip(*results):
  print(i[0],'-----','temp',i[1])