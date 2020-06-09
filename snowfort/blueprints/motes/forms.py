#from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import FloatField, IntegerField, TextAreaField, TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length, NumberRange, Optional, Required
from wtforms.widgets import HiddenInput

from snowfort.blueprints.motes.models import Mote
from snowfort.blueprints.stations.models import Station
from snowfort.shared.validators import Unique

from models import Mote

def select_stations():
  return Station.query.all()

class MoteForm(Form):
  id = IntegerField(widget=HiddenInput())
  tag = TextField('Unique ID Tag',
                  [Required(), Length(max=128), Unique(Mote, Mote.tag, message='Mote tag already exists.')])
  type = TextField('Type', [Required()])
  station = QuerySelectField(query_factory=select_stations, get_label='name')
  comment = TextAreaField('Comments', [Length(max=256)])
  sampling = FloatField('Sampling', [NumberRange(min=0.0)])
  last_pkt = IntegerField('Last Packet #', [Optional(), NumberRange(min=0, max=255)])
  received = IntegerField('Received', [NumberRange(min=0)])
  missed = IntegerField('Missed', [NumberRange(min=0)])
