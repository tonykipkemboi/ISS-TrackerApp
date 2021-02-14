# -*- coding: utf-8 -*-
"""
@Author: tonykip
@Sources: nasa, wikipedia, and https://projects.raspberrypi.org/en/projects/where-is-the-space-station

This app tracks the current location of the ISS and current Astronauts on board the ISS

ISS = International Space Station

"""

# --------------------------------------------------------------------------------------------------------------------#
# Import dependencies
import json
import turtle
import urllib.request
import time
import webbrowser

import geocoder

# --------------------------------------------------------------------------------------------------------------------#
# Global variables
# URL for the API's
url_astro = 'http://api.open-notify.org/astros.json'
url_loc = 'http://api.open-notify.org/iss-now.json'

# turtle instance variables
screen = turtle.Screen()
iss = turtle.Turtle()


# --------------------------------------------------------------------------------------------------------------------#
# Return a list of astronauts currently aboard the ISS
def astronauts_on_board_iss():
    # URL for the API to show astronauts onboard the ISS
    response_1 = urllib.request.urlopen(url_astro)
    result_1 = json.loads(response_1.read())

    file = open("iss.txt", "w")
    file.write("Currently, there are " + str(result_1["number"]) +
               " Astronauts aboard the ISS.\n" + "\nThey are: " + "\n")

    people = result_1['people']

    # loop over list of astros and write to file
    for person in people:
        file.write("\n - " + person['name'] + "\n")

    # get my longitude and latitude
    g = geocoder.ipinfo("me")
    file.write("\nYour current latitude / longitude is: " + str(g.latlng))
    file.write("\nYour current location is: " + g.city + ", " + g.state + ", " + g.country)

    # close file
    file.close()

    # open file
    return webbrowser.open("iss.txt")


# --------------------------------------------------------------------------------------------------------------------#
# Setup the world map and the ISS on turtle module
def setup_world_map_and_iss():
    screen.setup(1200, 635)
    screen.setworldcoordinates(-180, -90, 180, 90)

    # load the map and iss
    screen.bgpic("world.gif")
    screen.register_shape("iss.gif")
    iss.shape("iss.gif")
    iss.setheading(45)
    iss.penup()


# --------------------------------------------------------------------------------------------------------------------#
# method to find current location of the ISS
def locate_iss():
    # URL for the API to show current location of ISS
    response = urllib.request.urlopen(url_loc)
    result = json.loads(response.read())

    # extract ISS location (latitude and longitude)
    location = result["iss_position"]
    lat = location["latitude"]
    lon = location["longitude"]

    # output lon and lat on terminal
    lat = float(lat)
    lon = float(lon)
    print("\nLatitude: " + str(lat))
    print("\nLongitude: " + str(lon))


# --------------------------------------------------------------------------------------------------------------------#
# draws path taken by ISS -> in 'real-time'
def draw_iss_route():
    # URL for the API to show current location of ISS
    response = urllib.request.urlopen(url_loc)
    result = json.loads(response.read())

    # pen and color to draw path
    iss.pensize(3)
    iss.pencolor("red")
    iss.penup()

    # extract ISS location (latitude and longitude)
    location = result["iss_position"]
    lat = location["latitude"]
    lon = location["longitude"]

    # output longitude and latitude on terminal
    lat = float(lat)
    lon = float(lon)
    iss.setposition(float(lon), float(lat))
    iss.pd()

    # update ISS location on the map
    iss.goto(lon, lat)


# --------------------------------------------------------------------------------------------------------------------#
# function to execute the program
def main():
    print("===============================================================================================")
    print("This is an app to track the ISS and the names of those currently on board the station! \nEnjoy!")
    print("===============================================================================================")
    print(" ")

    # outputs a file with names of astronauts onboard the ISS
    astronauts_on_board_iss()

    while True:
        # loads the map and iss tracker
        setup_world_map_and_iss()

        # shows current location of the ISS
        locate_iss()

        # draws the path taken by the ISS over time
        draw_iss_route()

        # refresh every 5 seconds
        time.sleep(5)

        # exit program if and only if app screen is clicked
        screen.exitonclick()


# --------------------------------------------------------------------------------------------------------------------#
# top-level main scope script
if __name__ == "__main__":
    # execute only if run as a script
    main()
