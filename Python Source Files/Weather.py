# Weather.py
import pyttsx3
import datetime
import os
import requests
import json

#API key 1481183c75501986d143a344d9785a00
#API - Application programming Interface: To access online web-based software applications
# Python program to find current
# weather details of any city
# using openweathermap api

# Enter your API key here
api_key = "1481183c75501986d143a344d9785a00"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = "Bangalore"

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x = response.json()

# Now x contains list of nested dictionariesWeather
# Check the value of "cod" key is equal to
# "404", means city is found otherwise, city is not found

def weather_report():
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]-273.15

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # print following values
        return "It is currently " + str(int(current_temperature)) + " degree Celsius in Bangalore. The atmospheric pressure is " + str(current_pressure) + " and the humidity is " + str(current_humidiy) + ". " + str( weather_description).upper() + " may also occur."
    else:
        return "Sorry Sir. I am not able to connect to the Internet."
