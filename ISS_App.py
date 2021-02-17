# -*- coding: utf-8 -*-
"""
@Author: tonykip
@Sources: nasa, wikipedia, and https://projects.raspberrypi.org/en/projects/where-is-the-space-station

This app tracks the current location of the ISS and current Astronauts on board the ISS
ISS = International Space Station
The program starts by writing the names of current astronauts onboard the ISS into "iss.txt" file
than proceeds to load the current location of ISS and starts tracking its path with a red line on 
the map

"""

# ---------------------------------------------------------------------------------------------------------------------
# Import dependencies
import json
import turtle
import urllib.request
import time
import webbrowser

import geocoder

# ---------------------------------------------------------------------------------------------------------------------
# Global variables
# URL for the API's
url_astro = 'http://api.open-notify.org/astros.json'
url_loc = 'http://api.open-notify.org/iss-now.json'

# turtle instance variables
screen = turtle.Screen()
iss = turtle.Turtle()


# ---------------------------------------------------------------------------------------------------------------------
def astronauts_on_board_iss():
    """
    Returns a list of astronauts currently onboard the ISS 
    in a *.txt file (iss.txt)
    """
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


# ---------------------------------------------------------------------------------------------------------------------
def setup_world_map_and_iss():
    """
    Sets up the world map and the ISS gif images on the turtle module
    (GUI)
    The images have to be .gif to work
    """
    screen.setup(1200, 635)
    screen.setworldcoordinates(-180, -90, 180, 90)

    # load the map and iss
    screen.bgpic("world.gif")
    screen.register_shape("iss.gif")
    iss.shape("iss.gif")
    iss.setheading(45)
    iss.penup()


# ---------------------------------------------------------------------------------------------------------------------
def locate_iss():
    """
    Method to find current location of the ISS 
    using the Open Notify API
    """
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


# ---------------------------------------------------------------------------------------------------------------------
def draw_iss_route():
    """
    Draws the path taken by ISS -> in 'real-time'
    on the map
    """
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


# ---------------------------------------------------------------------------------------------------------------------
def main():
    """
    Function to execute the entire program
    """
    print("###################")
    print("# ISS TRACKER APP #")
    print("###################")
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


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    """
    Top-level main scope script
    """
    # execute only if run as a script
    main()
