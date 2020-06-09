#!/usr/bin/env python

"""
This script will generate a test bed of data for you to view.
You should delete the development database if you already have it set up.
"""
import datetime
import math
import sys
import os

from snowfort import db
from snowfort.blueprints.data.models import Datum
from snowfort.blueprints.motes.models import Mote
from snowfort.blueprints.sensors.models import Sensor
from snowfort.blueprints.stations.models import Station
from snowfort.blueprints.users.models import User

db.create_all()

# Users
print "Generating Users"
user = User("Richard", "Hsu", "richardhsu.cs@gmail.com", "mypasswordcool");
db.session.add(user)

# Stations
print "Generating Stations"
station_1 = Station("Stanford", "Stanford")
db.session.add(station_1)
station_2 = Station("Berkeley", "Berkeley")
db.session.add(station_2)

# Sensors
print "Generating Sensors"
sensor = Sensor("Temperature", "temperature")
db.session.add(sensor)
sensor = Sensor("Gyroscope", "gyro")
db.session.add(sensor)
sensor = Sensor("Accelerometer", "acc")
db.session.add(sensor)

db.session.commit()

# Motes
print "Generating Motes"
station_1_motes = []
for i in range(0, 10):
  mote = Mote("Stanford-{0}".format(i), "blueberry-pi", station_1.id, '1.0')
  db.session.add(mote)
  station_1_motes.append(mote)

station_2_motes = []
for i in range(0, 5):
  mote = Mote("Berkeley-{0}".format(i), "model-s", station_2.id, '1.0')
  db.session.add(mote)
  station_2_motes.append(mote)

db.session.commit()
print "Committed"
