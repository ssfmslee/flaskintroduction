from flask import flash, g, redirect, request, url_for
from functools import wraps

def requires_login(f):
  """
  Requires login decorator so that actions that require login are preprocessed.
  """
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if g.user is None:
      flash('You need to be signed in to view this page.', 'danger')
      return redirect(url_for('users.login', next=request.path))
    return f(*args, **kwargs)
  return decorated_function

