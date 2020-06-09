from flask import flash, g, redirect, render_template, request, session, url_for

from snowfort import db
from snowfort.shared.decorators import requires_login

from . import mod
from forms import SensorForm
from models import Sensor

@mod.route('/new/', methods=['GET', 'POST'])
@requires_login
def new():
  """
  New sensor form to create a sensor.
  """
  form = SensorForm(request.form)
  if form.validate_on_submit():
    sensor = Sensor(form.name.data, form.attribute.data, form.comment.data, form.c_1.data, form.c_2.data)
    db.session.add(sensor)
    db.session.commit()

    flash('You have successfully added a new sensor.', 'success')
    return redirect(url_for('sensors.view', id=sensor.id))
  return render_template('sensors/new.html', form=form)

@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@requires_login
def edit(id):
  """
  Edit sensor form to modify a sensor.
  """
  sensor = Sensor.query.get(id)
  form = SensorForm(request.form, obj=sensor)
  if request.method == 'POST':
    form.populate_obj(sensor)
    if form.validate():
      db.session.commit()
      flash('You have successfully modified the sensor.', 'success')
      return redirect(url_for('sensors.edit', id=sensor.id))
  return render_template('sensors/edit.html', form=form, sensor=sensor)

@mod.route('/view/<int:id>', methods=['GET'])
@requires_login
def view(id):
  """
  View action for showing a particular sensor.
  """
  sensor = Sensor.query.get(id)
  if sensor:
    return render_template('sensors/view.html', sensor=sensor)
  flash('Invalid sensor ID of ' + str(id) + ' given!', 'danger')
  return redirect(url_for('sensors.all'))

@mod.route('/all/', methods=['GET'])
@requires_login
def all():
  """
  All action to show all sensors that are in the database.
  """
  sensors = Sensor.query.all()
  return render_template('sensors/all.html', sensors=sensors)

