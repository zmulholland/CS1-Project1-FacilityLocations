#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 15:21:33 2023

@author: zackmulholland
"""

# Load all of the data contained in miles.dat
def loadData(cityList, coordList, popList, distanceList):
    
    f = open("miles.dat")
    i = -1
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    distsList = []
    for line in f:
        # Check if line starts with an upper case letter. Such lines contain
        # information about cities.
        if ("A" <= line[0]) and (line[0] <= "Z"):
            # extract cityName and stateCode
            j = 0
            while (line[j] != '['):
                j = j + 1
            cityName = line[:j-4]
            # The last two characters are the state code
            stateCode = line[j-2:j]
            
            cityList.append(cityName + " " + stateCode)
            
            # extracting the latitude and longitude
            
            j = j + 1
            
            latitude = ""
            longitude = ""
            while (line[j] != ','):
                latitude = latitude + line[j]
                j = j + 1
            j = j + 1
            while (line[j] != ']'):
                longitude = longitude + line[j]
                j = j + 1
            
            latitude = int(latitude)
            longitude = int(longitude)
            
            coordList.append([latitude,longitude])
            
            # extracting the population
            popList.append(int( line[j+1:len(line)-1] ))
            
            # if the line does not include distances, we need to clear the distLists below
            i = i + 1
            # Since the first city does not have numbers, we want to skip that one.
            if i != 0:
                distanceList.append(distsList)
                distsList = []
            
        # extract the distances    
        elif line[0] in digits:
            distance = ""
            for ch in line:
                if ch in digits:
                    distance = distance + ch
                else:
                    distsList.append(int(distance))
                    distance = ""
    
    # Once the entire file is read
    distanceList.append(distsList)
    # Reverse the entire distances list
    k = 0
    while k < 128:
        distanceList[k] = distanceList[k][::-1]
        k = k + 1
    
    
# Function that returns the coordinates of any city
def getCoordinates(cityList, coordList, name):
    i = 0
    while cityList[i] != name:
        i = i + 1
    
    return coordList[i]
            

# Function that returns the population of any city
def getPopulation(cityList, popList, name):
    i = 0
    while cityList[i] != name:
        i = i + 1
    
    return popList[i]


# Function that returns the distance between any two cities
def getDistance(cityList, distanceList, name1, name2):
    # Identify the indices of the two cities in cityList
    i = 0
    while cityList[i] != name1:
        i = i + 1
    j = 0
    while cityList[j] != name2:
        j = j + 1

    # Rearrange them so the jth index comes after the ith index.
    if i > j:
        filler = j
        j = i
        i = filler
    elif i == j:
        return 0
    
    return distanceList[j][i]


# Function that returns the cities within a distance r of a particular city
def nearbyCities(cityList, distanceList, name, r):
    cities = []
    # Find index of the city in cityList
    i = 0
    while cityList[i] != name:
        i = i + 1
    j = 0
    
    # Find the distance between that city and every other city and compare it with r
    while j < i:
        if distanceList[i][j] <= r:
            cities.append(cityList[j])
        j = j + 1
        
    j = i + 1
    while j < 128:
        if distanceList[j][i] <= r:
            cities.append(cityList[j])
        j = j + 1
    
    return cities



# Function that uses a greedy algorithm to assign facilities to cities that serve other cities within a distance r.
def locateFacilities(cityList, distanceList, r):
    facilities = []
    served = [False] * 128
    while (served != [True] * 128):
        # Find the index of the optimal facility
        maxIndex = greedyAlgorithm(distanceList, r, served)
        # Update the "served" list with the facility identified
        markdown(maxIndex, distanceList, r, served)
        # Add the facility to the list
        facilities = facilities + [cityList[maxIndex]]
    
    return facilities


# Function that finds the city that serves the most unserved cities.
def greedyAlgorithm(distanceList, r, served):
    i = 0
    countMax = 0
    maxIndex = 0
    while i < 128:
        count = 0
        # If the city itself is unserved, a facility there will serve itself
        if served[i] == False: 
            count = count + 1
        j = 0
        while j < i:
            # If the other cities are unserved and within distance r, mark it down as another potential city served
            if (distanceList[i][j] <= r) and (served[j] == False):
                count = count + 1
            j = j + 1
        j = i + 1
        while j < 128:
            if (distanceList[j][i] <= r) and (served[j] == False):
                count = count + 1
            j = j + 1
        
        # Compare the cities served to the previous maximum for other cities
        if count > countMax:
            countMax = count
            maxIndex = i
        i = i + 1
            
    
    return maxIndex


# Function that identifies which cities will be served by a particular facility and updates the served list
def markdown(maxIndex, distanceList, r, served):
    i = maxIndex
    j = 0
    while j < i:
        if (distanceList[i][j] <= r):
            served[j] = True
        j = j + 1
    served[i] = True
    j = i + 1
    while j < 128:
        if (distanceList[j][i] <= r):
            served[j] = True
        j = j + 1
    
    pass



# Line style for a KML file
def createLineStyle(name, width, color):
    result  = ""
    result += "<Style id=\"" + name + "\">\n"
    result += "  <LineStyle>\n"
    result += "    <color>" + color + "</color>\n"
    result += "    <width>" + width + "</width>\n"
    result += "  </LineStyle>\n"
    result += "</Style>\n"
    return result



# Balloon Style for a kml file
def createBalloonStyle(name, text, color):
    result  = ""
    result += "<Style id=\"" + name + "\">\n"
    result += "  <BalloonStyle>\n"
    result += "    <color>" + color + "</color>\n"
    result += "  </BalloonStyle>\n"
    result += "  <IconStyle>\n"
    result += "    <color>" + color + "</color>\n"
    result += "  </IconStyle>\n"
    result += "</Style>\n"
    return result

    
    
# Creates a point for a KML file
def createPoints(name, desc, style, coordString):
    result  = ""
    result += "<Placemark>\n"
    result += "  <name>" + name + "</name>/n"
    result += "  <description>" + desc + "</description>\n"
    result += "  <styleUrl>#" + style + "</styleUrl>\n"
    result += "  <Point>\n    <coordinates>" + coordString + "</coordinates>\n"
    result += "  </Point>\n"
    result += "</Placemark>\n"
    return result
 
# Creates a line for a KML file   
def createLines(name, desc, style, coordString1, coordString2):
    result  = ""
    result += "<Placemark>\n"
    result += "  <name>" + name + "</name>/n"
    result += "  <description>" + desc + "</description>\n"
    result += "  <styleUrl>#" + style + "</styleUrl>\n"
    result += "  <LineString>\n    <coordinates>" + coordString1 + "," + coordString2 + "</coordinates>\n"
    result += "  </LineString>\n"
    result += "</Placemark>\n"
    return result


# Function that writes a KML file that shows all facilities and the cities they serve in Google Earth
def display(cityList, coordList, facilities, distanceList, r):
    f = open("visualization" + str(r) + ".kml", "w")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    f.write("<Document>\n")
    styelBlueLine = createLineStyle("BlueLine", "2", "ffff0000")
    styleBlackBalloon = createBalloonStyle("BlackBalloon", "Black Balloon", "ffff0000")
    styleRedBalloon = createBalloonStyle("RedBalloon", "Red Balloon", "ff0000ff")
    
    f.write(styelBlueLine)
    f.write(styleBlackBalloon)
    f.write(styleRedBalloon)
    
    
    for i in range(len(cityList)):
        city = cityList[i]
        coordinates = coordList[i]
        # Turn the coordinates into Google Earth coordinate language
        coordString = str(-1 * coordinates[1]/100) + "," + str(coordinates[0]/100) + ",0"
        
        # Update the color of the balloon depending on if it is a facility (black) or not (red)
        if city in facilities:
            f.write(createPoints(city, "Facility", "BlackBalloon", coordString))
        else:
            f.write(createPoints(city, "City", "RedBalloon", coordString))
            
    # Create the lines that connect the cities to the facilities
    f.write(writeLines(cityList, coordList, facilities, distanceList, r))
    f.write("</Document>\n</kml>")
    
    f.close()
    pass
        
        

# Function that creates lines between any city and its closest facility
def writeLines(cityList, coordList, facilities, distanceList, r):
        f = ""
        # For all cities, find all facilities and find the smallest distance
        for i in range(len(cityList)):
            distance = 10000000
            for j in range(len(cityList)):
                if cityList[j] in facilities:
                    newDistance = getDistance(cityList, distanceList, cityList[i], cityList[j])
                    if newDistance < distance:
                        distance = newDistance
                        index = j
                        
            # Create the line using the identified index
            coordinates1 = coordList[i]
            coordinates2 = coordList[index]
            coordString1 = str(-1 * coordinates1[1]/100) + "," + str(coordinates1[0]/100) + ",0"
            coordString2 = str(-1 * coordinates2[1]/100) + "," + str(coordinates2[0]/100) + ",0"
            f = f + createLines("Edge", cityList[i] + " to " + cityList[index], "BlueLine", coordString1, coordString2)
                        
        return f



# Main program: Gathers the data and creates two KML files, one with a radius of 300 miles and one with a radius of 800 miles.
cityList = []
coordList = []
popList = []
distanceList = []
loadData(cityList, coordList, popList, distanceList)

display(cityList, coordList, locateFacilities(cityList, distanceList, 300), distanceList, 300)
display(cityList, coordList, locateFacilities(cityList, distanceList, 800), distanceList, 800)





 