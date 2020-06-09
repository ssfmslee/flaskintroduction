#!/usr/bin/env python

from datetime import datetime
import json
import random
import time
import urllib2

SERVER = 'http://localhost:5000/data/post'
STATION = 'Stanford'
NUM_MOTES = 5
NUM_ITERATIONS = 300  # Tests 255 loop around

FAILURE = 0.1

packet_nums = [0]*NUM_MOTES
sent = [0]*NUM_MOTES
missing = [0]*NUM_MOTES

for iteration in range(0, NUM_ITERATIONS):
  for mote_id in range(0, NUM_MOTES):
    # Decide whether to send or not
    if random.random()*10 > (10 - FAILURE*10):
      # Choose to skip
      missing[mote_id] += 1
      packet_nums[mote_id] = (packet_nums[mote_id] + 1) % 256
      continue

    data = {
             "station": STATION,
             "mote_id": mote_id,
             "timeslot": mote_id,
             "timestamp": datetime.utcnow(),
             "timestamp": time.mktime(datetime.utcnow().timetuple()),
             "packet_num": packet_nums[mote_id],
             "data": {
                "acc_x": [round(10*random.random(), 2) for i in range(0, 5)],
                "acc_y": [round(10*random.random(), 2) for i in range(0, 5)],
                "acc_z": [round(10*random.random(), 2) for i in range(0, 5)],
                "gyro_x": [round(10*random.random(), 2) for i in range(0, 5)],
                "gyro_x": [round(10*random.random(), 2) for i in range(0, 5)],
                "gyro_x": [round(10*random.random(), 2) for i in range(0, 5)],
                "temperature": [round(10*random.random(), 2) for i in range(0, 5)]
             }
    }
    print "Starting request for mote_id: %d" % (mote_id)
#    print "Sending data: %s" % (json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    print "Sending data: %s" % (json.dumps(data))
    req = urllib2.Request(SERVER)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))

    # Test response
    response_data = response.read()
    json_data = json.loads(response_data)
    if json_data["status"] == "success":
      sent[mote_id] += 1

    response.close()
    packet_nums[mote_id] = (packet_nums[mote_id] + 1) % 256

# Done
print "Done Drop Demo"
print "Assumed successfully sent packets:"
print sent
print "Forced missed packets:"
print missing
