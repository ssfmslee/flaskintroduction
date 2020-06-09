from snowfort import db

class Station(db.Model):
  __tablename__ = 'stations'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  location = db.Column(db.String(128))
  comment = db.Column(db.String(256))
  motes = db.relationship("Mote")
  #TODO: Cascade Delete on Station to Motes?
  #motes = db.relationship("Mote", cascade="all,delete")

  def __init__(self, name=None, location='', comment=''):
    self.name = name
    self.location = location
    self.comment = comment

  def __str__(self):
    return self.name

  def __repr__(self):
    return '<Station %r>' % (self.name)
