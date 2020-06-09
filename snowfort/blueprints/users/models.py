import hashlib
import uuid

from snowfort import db

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(32))
  last_name = db.Column(db.String(32))
  email = db.Column(db.String(128), unique=True)
  salt = db.Column(db.String(32))
  password_digest = db.Column(db.String(128))
  role = db.Column(db.SmallInteger, default=0)

  def __init__(self, first_name=None, last_name=None, email=None, password=None):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.salt = uuid.uuid4().hex
    self.password_digest = hashlib.sha512(password + self.salt).hexdigest()

  def __repr__(self):
    return '<User %r>' % (self.email)

  def verify_password(self, password):
    return (self.password_digest == hashlib.sha512(password + self.salt).hexdigest())

  def full_name(self):
    return self.first_name + " " + self.last_name

  def update(self, first_name=None, last_name=None, email=None, password=None):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    if len(password) > 0:
      # New password given so update
      self.salt = uuid.uuid4().hex
      self.password_digest = hashlib.sha512(password + self.salt).hexdigest()

