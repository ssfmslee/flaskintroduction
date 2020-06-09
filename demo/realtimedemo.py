#!/usr/bin/env python

"""
This is a realtime demo that will put data into the database every second. It'll space out the data to be
every minute though so it is easier to read on the graph!
"""
import datetime
import math
import sys
from time import sleep
import os

import numpy as np

from snowfort import db
from snowfort.blueprints.data.models import Datum
from snowfort.blueprints.motes.models import Mote
from snowfort.blueprints.sensors.models import Sensor
from snowfort.blueprints.stations.models import Station
from snowfort.blueprints.users.models import User

# For SQLite Development Database
if not os.path.exists("snowfort/development.db"):
  print "You need to have set up the development.db first!"
  print "Create yourself or use demo.py"
  sys.exit(1)

# Motes
motes = Mote.query.all()

# Data
i = 201
next_time = 0
time = datetime.datetime.utcnow()
print "Starting Data Insertion"
print "Starting Time: {0}".format(time)
while (True):
  offset = 0
  for mote in motes:
    # Data for the station
    #datum = Datum("temperature", 50*math.sin(math.radians(i*30 + offset)),
    #              time + datetime.timedelta(minutes=next_time), mote.tag)
    # db.session.add(datum)


    datum = Datum("acc_x", np.random.uniform()*math.sin(math.radians(i*30 + offset)),time + datetime.timedelta(minutes=next_time), mote.tag)
    # datum = Datum("acc_x", math.sin(math.radians(i*30 + offset)),time + datetime.timedelta(minutes=next_time), mote.tag)
   
    db.session.add(datum)

    offset += 15

  db.session.commit()
  print "Last Insert -- {0}. Sleeping.".format(time + datetime.timedelta(minutes=next_time))
  sleep(1);
  next_time += 1
  i += 1
