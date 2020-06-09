from data import mod as data_blueprint
from motes import mod as motes_blueprint
from sensors import mod as sensors_blueprint
from stations import mod as stations_blueprint
from users import mod as users_blueprint

app_blueprints = [
  data_blueprint,
  motes_blueprint,
  sensors_blueprint,
  stations_blueprint,
  users_blueprint
]
