from datetime import datetime

from snowfort import db

class Datum(db.Model):
  __tablename__ = 'data'
  id = db.Column(db.Integer, primary_key=True)
  attribute = db.Column(db.String(128), db.ForeignKey('sensors.attribute'))
  value = db.Column(db.String(256))
  timestamp = db.Column(db.DateTime)
  timeslot = db.Column(db.Integer)
  packet_num = db.Column(db.Integer)
  axis = db.Column(db.String(16))
  mote_tag = db.Column(db.String(128), db.ForeignKey('motes.tag'))
  mote = db.relationship("Mote")
  sensor = db.relationship("Sensor")

  def __init__(self, attribute=None, value=None, timestamp=None, mote_tag=None, timeslot=None, axis='',
               packet_num=0):
    self.attribute = attribute.lower()
    self.value = value
    self.mote_tag = mote_tag
    self.timestamp = timestamp
    self.timeslot = timeslot
    self.axis = axis
    self.packet_num = packet_num

    # Set the timestamp if set to None
    if self.timestamp is None:
      # Make sure timestamps are in GMT time zone to be consistent
      self.timestamp = datetime.utcnow()

  def __repr__(self):
    d_id = self.id
    if d_id is None: d_id = 0
    return '<Datum id:%d att:%s val:%s pnum:%s>' % (d_id, self.attribute, self.value, self.packet_num)

  def __str__(self):
    d_id = self.id
    if d_id is None: d_id = 0
    return '<Datum id:%d att:%s val:%s pnum:%s>' % (d_id, self.attribute, self.value, self.packet_num)
