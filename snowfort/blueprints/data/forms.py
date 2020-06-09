#from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import DateTimeField, IntegerField, TextAreaField, TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length, NumberRange, Optional, Required
from wtforms.widgets import HiddenInput

from snowfort.blueprints.motes.models import Mote
from snowfort.blueprints.sensors.models import Sensor

from models import Datum

def select_motes():
  return Mote.query.all()

def select_sensors():
  return Sensor.query.all()

class DatumForm(Form):
  id = IntegerField(widget=HiddenInput())
  mote = QuerySelectField(query_factory=select_motes, get_label='tag')
  sensor = QuerySelectField(query_factory=select_sensors, get_label='attribute')
  value = TextAreaField('Value', [Required(), Length(max=256)])
  timestamp = DateTimeField('Timestamp', [Optional()])
  timeslot = IntegerField('Timeslot', [NumberRange(min=0)])
  axis = TextField('Axis', [Optional()])
  packet_num = IntegerField('Packet Number', [NumberRange(min=0)])
