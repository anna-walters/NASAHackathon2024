# Sunrise and Sunset

#https://sunrise-sunset.org/api

# Widecombe in the Moor 
#3 48 42 W Long (W)
# 50 34 36 Lat (N) 

import urllib
import urllib.request
import ast 

print("Welcome to Team DartMappers SolarYum application!")

url_base = "https://api.sunrise-sunset.org/json?"
lat = 50.576710 # Example Lat 
long = -3.811770 # Example Long 
#date = 2024-12-01

test = urllib.request.urlopen("https://api.sunrise-sunset.org/json?lat=50.576710&lng=-3.811770&date=today")

data = ast.literal_eval(test.read().decode())

print("All data:", data)
print("")

print("Sunrise:", data["results"]["sunrise"])
print("Sunset", data["results"]["sunset"])



