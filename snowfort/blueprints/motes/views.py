from flask import flash, g, redirect, render_template, request, session, url_for

from snowfort import db
from snowfort.shared.decorators import requires_login
from snowfort.blueprints.data.models import Datum

from . import mod
from forms import MoteForm
from models import Mote

@mod.route('/new/', methods=['GET', 'POST'])
@requires_login
def new():
  """
  New mote action to create a new mote. Tags should be unique!
  """
  form = MoteForm(request.form)
  if form.validate_on_submit():
    mote = Mote(form.tag.data, form.type.data, form.station.data.id, form.sampling.data, form.comment.data,
                form.last_pkt.data, form.received.data, form.missed.data)
    db.session.add(mote)
    db.session.commit()

    flash('You have successfully added a new mote.', 'success')
    return redirect(url_for('motes.view', id=mote.id))
  return render_template('motes/new.html', form=form)

@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
@requires_login
def edit(id):
  """
  Edit mote form to modify a mote.
  """
  mote = Mote.query.get(id)
  form = MoteForm(request.form, obj=mote)
  if request.method == 'POST':
    form.populate_obj(mote)
    if form.validate():
      db.session.commit()
      flash('You have successfully modified the mote.', 'success')
      return redirect(url_for('motes.edit', id=mote.id))
  return render_template('motes/edit.html', form=form, mote=mote)

@mod.route('/view/<int:id>', methods=['GET'])
@requires_login
def view(id):
  """
  View action for showing a particular mote data.
  """
  mote = Mote.query.get(id)
  if mote:
    data = Datum.query.filter_by(mote_tag=mote.tag).order_by(Datum.packet_num.desc()).limit(100).all()
    return render_template('motes/view.html', mote=mote, data=data)
  flash('Invalid mote ID of ' + str(id) + ' given!', 'danger')
  return redirect(url_for('motes.all'))

@mod.route('/all/', methods=['GET'])
@requires_login
def all():
  """
  All action to show all motes that are in the database.
  """
  motes = Mote.query.all()
  return render_template('motes/all.html', motes=motes)

