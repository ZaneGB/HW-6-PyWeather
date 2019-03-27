#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies

get_ipython().system('pip install citipy')

import json
import csv
import random
import matplotlib.pyplot as plt
import requests
import numpy as np
import pandas as pd
import openweathermapy as ow

#import api_key from config file

from config_2 import weather_api_key
print(weather_api_key)


# In[2]:


# Create a settings object with your API key and preferred units

settings = {"units": "imperial", "appid": weather_api_key}
print(settings)


# In[3]:


# Need to get a list of 500+ random cities. There is a module called random that will generate a list of
# random numbers. Latitude ranges from -90 to 90 whilst longitude varies from -180 to 180. So lets randomly 
# generate coordinates for latitude & longitude and store them in lists.

latitude_random=[]
longitude_random=[]

np.random.seed(1)

for i in range (750):
    latitude_random.append(random.uniform(-90,90))
    longitude_random.append(random.uniform(-180,180))
    
    
#print(latitude_random)
#print(longitude_random)
len(latitude_random)


# In[4]:


# We can use the module Citypy to find the closest city to our geo coordinates. The ocean covers much of our planet,
# So it is possible that a random lat/long combination will not find a real city match. Lets start with 600 tries.

from citipy import citipy

# intialize a lsit of cities

cities_list = []

for j in range(600):
      
    city_nearby = citipy.nearest_city(latitude_random[j],longitude_random[j])
          
    cities_list.append([city_nearby.city_name, city_nearby.country_code])

#print(cities_list)
len(cities_list)


# In[5]:


# The Open Weather Map API provides current weather information for the cities we have randomly selected

url = 'https://api.openweathermap.org/data/2.5/weather'

# Initialize a list to hold our weather info.

weather_info = []

for k in range(len(cities_list)):
    
    city = cities_list[k][0]
    country = cities_list[k][1]
        
    params ={'q': city + ',' + country,'units': 'imperial', 'appid': weather_api_key}
    
    response = requests.get(url, params).json()

# There is a possibility that a city from CityPy will not be included in the Weather API.
# We want the program to skip non-matches. So lets use "try-except-pass".
                            
    try:
        weather_info.append({'City': city,'Country': country,'Longitude': response['coord']['lon'], 
            'Latitude': response['coord']['lat'],'Max Temp': response['main']['temp_max'],
            'Humidity': response['main']['humidity'],'Cloudiness': response['clouds']['all'],
            'Wind Speed': response['wind']['speed']})
        
    except:
        pass
    
len(weather_info)


# In[6]:


column_names = ["City", "Country", "Cloudiness", "Humidity", "Latitude", "Longitude", "Max Temp", "Wind Speed"]

#column_names = ["City", "Cloudiness", "Country", "Date", "Humidity", "Latitude", "Longitude", "Max Temp", "Wind Speed"]

#weather_data = pd.DataFrame(weather_info, index=city, columns=column_names)

weather_data = pd.DataFrame(weather_info, columns=column_names)
#weather_data.head()
weather_data


# In[7]:


#Save Data to csv
    
weather_data.to_csv("Weather_Output.csv")


# In[30]:


# Latitude vs. Humidity Plot

# Build a scatter plot for each data type

plt.figure(figsize=(12,6))

plt.scatter(weather_data["Latitude"], weather_data["Humidity"], marker="o", s=50, alpha=0.50, color='Green', 
            edgecolor='Black')

# Incorporate the other graph properties

plt.title("Humidity in World Cities on March 25, 2019")
plt.ylabel("Humidity (%)")
plt.xlabel("Latitude")
plt.grid(True)
plt.ylim(0, 110)

# Save the figure
plt.savefig("Lat-Humidity.InWorldCities.png")

# Show plot
plt.show()


# In[24]:


# Latitude vs. Max Temperature Plot

# Build a scatter plot for each data type

plt.figure(figsize=(12,6))

plt.scatter(weather_data["Latitude"], weather_data["Max Temp"], marker="o", s=50, alpha=0.50, color='Red', 
            edgecolor='Black')

# Incorporate the other graph properties



plt.title("Maximum Temperature in World Cities on March 25, 2019")
plt.ylabel("Max Temperature (Fahrenheit)")
plt.xlabel("Latitude")
plt.grid(True)
plt.ylim(0, 100)

# Save the figure
plt.savefig("Lat-MaxTemp.InWorldCities.png")

# Show plot
plt.show()


# In[31]:


# Latitude vs. Cloudiness Plot

# Build a scatter plot for each data type

plt.figure(figsize=(12,6))

plt.scatter(weather_data["Latitude"], weather_data["Cloudiness"], marker="o", s=50, alpha=0.50, color='Blue', 
            edgecolor='Black')

# Incorporate the other graph properties

plt.title("Cloudiness in World Cities on March 25, 2019")
plt.ylabel("Cloudiness (%)")
plt.xlabel("Latitude")
plt.grid(True)
plt.ylim(-10, 100)

# Save the figure
plt.savefig("Lat-Cloudiness.InWorldCities.png")

# Show plot
plt.show()


# In[36]:


# Latitude vs. Wind Speed Plot

# Build a scatter plot for each data type

plt.figure(figsize=(12,6))

plt.scatter(weather_data["Latitude"], weather_data["Wind Speed"], marker="o", s=50, alpha=0.50,
            color='Purple', edgecolor='Black')

# Incorporate the other graph properties

plt.title("Wind Speed in World Cities on March 25, 2019")
plt.ylabel("Wind Speed (mph)")
plt.xlabel("Latitude")
plt.grid(True)
plt.ylim(-3, 35)

# Save the figure
plt.savefig("Lat-WindSpeed.InWorldCities.png")

# Show plot
plt.show()


# In[ ]:




