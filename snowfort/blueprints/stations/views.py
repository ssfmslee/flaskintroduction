from flask import flash, g, redirect, render_template, request, session, url_for

from snowfort import db
from snowfort.blueprints.sensors.models import Sensor
from snowfort.shared.decorators import requires_login

from . import mod
from forms import StationForm
from models import Station

@mod.route('/new/', methods=['GET', 'POST'])
@requires_login
def new():
  """
  New station form to create a station.
  """
  form = StationForm(request.form)
  if form.validate_on_submit():
    station = Station(form.name.data, form.location.data, form.comment.data)
    db.session.add(station)
    db.session.commit()

    flash('You have successfully added a new station.', 'success')
    return redirect(url_for('stations.view', id=station.id))
  return render_template('stations/new.html', form=form)

@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@requires_login
def edit(id):
  """
  Edit station form to modify a station.
  """
  station = Station.query.get(id)
  form = StationForm(request.form, obj=station)
  if request.method == 'POST':
    form.populate_obj(station)
    if form.validate():
      db.session.commit()
      flash('You have successfully modified the station.', 'success')
      return redirect(url_for('stations.edit', id=station.id))
  return render_template('stations/edit.html', form=form, station=station)

@mod.route('/view/<int:id>', methods=['GET'])
#deactivated login for public view
#@requires_login
def view(id):
  """
  View action for showing a particular station data.
  """
  station = Station.query.get(id)
  sensors = Sensor.query.all()
  if station:
    # return render_template('stations/view.html', station=station, motes=station.motes, sensors=sensors)
    return render_template('stations/view.html', station=station, motes=station.motes, sensors=sensors)
  flash('Invalid station ID of ' + str(id) + ' given!', 'danger')
  return redirect(url_for('stations.all'))

@mod.route('/all/', methods=['GET'])
#deactivated login for public view
#@requires_login
def all():
  """
  All action to show all stations that are in the database.
  """
  stations = Station.query.all()
  return render_template('stations/all.html', stations=stations)

