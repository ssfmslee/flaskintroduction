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

GENERATE_DATA = False

if os.path.exists("snowfort/development.db"):
  print "ERROR: You should delete the development.db file yourself."
  print "Demo exiting."
  sys.exit(0)

db.create_all()

# Users
# print "Adding Users"
# user = User("Jae", "Hwang", "yunjaeh@stanford.edu", "1234");
# db.session.add(user)

# Stations
print "Adding Stations"
# station_0 = Station("Huang", "Stanford")
# db.session.add(station_0)
# station_1 = Station("Durand", "Stanford")
# db.session.add(station_1)
station_2 = Station("Y2E2", "Stanford_Y2E2")
db.session.add(station_2)



# Sensors
print "Adding Sensors"
print "None"
# sensor = Sensor("Temperature", "temperature")
# db.session.add(sensor)
# sensor = Sensor("Wind_speed", "Wind_speed")
# db.session.add(sensor)
# sensor = Sensor("Wind_direction", "Wind_direction")
# db.session.add(sensor)

db.session.commit()

# Motes
print "Generating Motes"
mote = Mote("Y2E2_pressure", "CR300", station_2.id, '1.0')
db.session.add(mote)
# mote = Mote("WE_lab-2", "CR300", station_1.id, '1.0')
# db.session.add(mote)

db.session.commit()

# station_0_motes = []
#for i in range(0, 1):
#  mote = Mote("WE_lab-{0}".format(i), "CR300", station_3.id, '1.0')
#  db.session.add(mote)
#  station_3_motes.append(mote)

