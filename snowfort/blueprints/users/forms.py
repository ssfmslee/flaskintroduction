from flask import session
#from flask.ext.wtf import Form
from flask_wtf import Form # originally: from flask_wtf import Form 
from wtforms import PasswordField, TextField
from wtforms.validators import AnyOf, Email, EqualTo, Length, Optional, Required

from snowfort.shared.validators import Unique

from models import User

class LoginForm(Form):
  """
  Login Form for User
  Will be verified in the view for users.
  """
  email = TextField('Email Address', [Required(), Email()])
  password = PasswordField('Password', [Required()])

class RegistrationForm(Form):
  """
  Registration Form for User
  Users are only allowed to register with the code. This may need to change in future to be a database setting.
  """
  first_name = TextField('First Name', [Required(), Length(max=32)])
  last_name = TextField('Last Name', [Required(), Length(max=32)])
  email = TextField('Email Address',
                    [Required(), Email(), Length(max=128),
                     Unique(User, User.email, message='User email address already exists.')])
  password = PasswordField('Password', [Required(), Length(min=12)])
  confirm = PasswordField('Repeat Password',
                          [Required(), EqualTo('password', message='Passwords must match.')])
  code = TextField('Registration Code',
                   [Required(), AnyOf(['S3LSnowfort'], message='Invalid registration code.')])

class EditForm(Form):
  """
  Edit Form for User
  Has some custom modifications for checking uniqueness on email and changing password.
  """
  first_name = TextField('First Name', [Required(), Length(max=32)])
  last_name = TextField('Last Name', [Required(), Length(max=32)])
  email = TextField('Email Address', [Required(), Email(), Length(max=128)])
  old_password = PasswordField('Old Password', [Required(), Length(min=12)])
  password = PasswordField('Change Password', [Optional(), Length(min=12)])
  confirm = PasswordField('Confirm New Password', [EqualTo('password', message='Passwords must match.')])

  def __init__(self, user_id, *args, **kwargs):
    """
    Store the original user_id to verify against to check uniqueness.
    """
    Form.__init__(self, *args, **kwargs) # originally: Form.__init__(self, *args, **kwargs):
    self.user_id = user_id

  def validate(self):
    if not Form.validate(self): # Perform normal validations given above // originally: if not Form.validate(self):
        return False
    # Verify uniqueness of email
    user = User.query.filter_by(email=self.email.data).first()
    if user and (user.id != self.user_id):
      # Fail validation as someone else owns the address!
      self.email.errors.append('This email is already being used. Try again.')
      return False
    user = User.query.get(self.user_id)
    if user and user.verify_password(self.old_password.data):
      # Valid update
      if self.old_password.data == self.password.data:
        self.password.errors.append('Same as old password. Try again or ignore.')
        return False
    else:
      self.old_password.errors.append('Incorrect old password. Try again.')
      return False
    return True
