# -*- coding: utf-8 -*-
"""
This app tracks the current location of the ISS
and current astornauts on board the ISS
ISS = International Space Station

"""

# Import dependencies
import json
import turtle 
import urllib.request
import time
import webbrowser
import geocoder

# URL for the API to locate ISS
url_loc = 'http://api.open-notify.org/iss-now.json'

# URL for the API to show astronauts onboard the ISS
url_astro = 'http://api.open-notify.org/astros.json'
response = urllib.request.urlopen(url_astro)
result = json.loads(response.read())
file = open("iss.txt", "w")
file.write("There are " + str(result["number"]) + 
           " Astronauts currently on the International Space Station!")

people = result['people']
for person in people:
    file.write(person['name'] + " - on board the ISS" + "\n")

# print longitude and latitude
g = geocoder.ip("me")
file.write("\n Your current latitude / longitude is: " + str(g.latlng))
file.close()

webbrowser.open("iss.txt")
