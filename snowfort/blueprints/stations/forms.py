#from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import IntegerField, TextAreaField, TextField
from wtforms.validators import Length, Required
from wtforms.widgets import HiddenInput

from snowfort.shared.validators import Unique

from models import Station

class StationForm(Form):
  id = IntegerField(widget=HiddenInput())
  name = TextField('Station Name', [Required(), Length(max=128),
                                    Unique(Station, Station.name, message='Station name already exists.')])
  location = TextAreaField('Location', [Length(max=128)])
  comment = TextAreaField('Comments', [Length(max=256)])
