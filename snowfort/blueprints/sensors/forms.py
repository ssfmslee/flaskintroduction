#from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import IntegerField, FloatField, TextAreaField, TextField
from wtforms.validators import Length, Required
from wtforms.widgets import HiddenInput

from snowfort.shared.validators import Unique

from models import Sensor

class SensorForm(Form):
  id = IntegerField(widget=HiddenInput())
  name = TextField('Sensor Name', [Required(), Length(max=128)])
  attribute = TextField('Sensor Attribute Name',
                        [Required(), Length(max=128),
                         Unique(Sensor, Sensor.attribute, message='Sensor attribute name already exists.')])
  comment = TextAreaField('Comments', [Length(max=256)])
  c_1 = FloatField('Coefficient 1')
  c_2 = FloatField('Coefficient 2')
