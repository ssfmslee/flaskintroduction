from flask import flash, g, redirect, render_template, request, session, url_for

from snowfort import db
from snowfort.shared.decorators import requires_login

from . import mod
from forms import EditForm, LoginForm, RegistrationForm
from models import User

@mod.route('/register/', methods=['GET', 'POST'])
def register():
  """
  Registration action will produce registration form and if given post
  request it will register the user.
  """
  form = RegistrationForm(request.form)
  if form.validate_on_submit():
    user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id

    flash('You have successfully been registered!', 'success')
    return redirect(url_for('users.profile'))
  return render_template('users/register.html', form=form)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
  """
  Login action will produce the form and if given post request it will
  verify the user and log them in.
  """
  form = LoginForm(request.form)
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and user.verify_password(form.password.data):
      session['user_id'] = user.id  # Create session for user_id
      flash('Welcome back %s %s!' % (user.first_name, user.last_name), 'success')
      return redirect(url_for('users.profile'))
    # Otherwise error couldn't find email or bad password
    flash('Incorrect email and password. Please try again.', 'danger')
  return render_template('users/login.html', form=form)

@mod.route('/profile/')
@requires_login
def profile():
  """
  Profile action that is the default page redirected to after login.
  """
  return render_template('users/profile.html', user=g.user)

@mod.route('/edit/', methods=['GET', 'POST'])
@requires_login
def edit():
  """
  Edit action for personal profile.
  """
  form = EditForm(g.user.id, formdata=request.form, obj=g.user)
  if form.validate_on_submit():
    user = User.query.get(g.user.id)
    # Must exist since they are logged in!
    user.update(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Updates saved, you should see the changes below.', 'success')
  return render_template('users/edit.html', form=form)

@mod.route('/logout/', methods=['GET'])
@requires_login
def logout():
  """
  Logout action that clears the session and redirects to login page.
  """
  session.clear()
  return redirect(url_for('users.login'))
