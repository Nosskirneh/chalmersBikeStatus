#!/usr/bin/env python
# coding=utf-8
from config import *
import os
import json
import requests
from flask import Flask, render_template

def getData(latitude, longitude, radius, dictType):
    r = requests.get(HOST + APP_KEY + "?getclosingperiods=False" + "&latitude=" + latitude + "&longitude=" + longitude + "&radius=" + radius + "&format=" + dictType)

    return r.json()

def compileStation(latitude, longitude, radius, dictType):
    global stations

    data = getData(latitude, longitude, radius, dictType)

    for entry in data:
        station = {}
        station['Name'] = entry['Name']
        if not 'AvailableBikes' in entry.keys():
            station['AvailableBikes'] = 0
        else:
            station['AvailableBikes'] = entry['AvailableBikes']
        station['BikeStands'] = entry['BikeStands']
        stations.append(station)
        #print("Station: %s, Number of free bikes: %s, Number of empty slots: %s"%(station['Name'], station['AvailableBikes'], station['BikeStands'])) #logging

def available(stationlist):
    issues = 0
    if stationlist is DEP_STATIONS:
        item = 'AvailableBikes'
    else:
        item = 'BikeStands'
    for sta1 in stations:
        for sta2 in stationlist:
            if sta2 == sta1['Name'] and sta1[item] is 0:
                    issues += 1
    if issues > 1:
        return False
    return True

def analyzeData():
    global stations
    stations = []
    compileStation("57.708074", "11.972737", "200", "JSON")
    compileStation("57.68979", "11.97305", "410", "JSON")

    # for test scenarios
    # stations[0]['BikeStands'] = 5
    # stations[1]['BikeStands'] = 4
    # stations[2]['AvailableBikes'] = 1
    # stations[3]['AvailableBikes'] = 0

    if not available(DEP_STATIONS) or not available(ARR_STATIONS):
        return False
    return True

# Create flask application.
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def root():
    data = analyzeData()
    dep_arr = [DEP_STATIONS, ARR_STATIONS]
    return render_template('index.html', data=data, stations=stations, dep_arr=dep_arr)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=True) 
