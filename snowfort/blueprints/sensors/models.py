from snowfort import db

class Sensor(db.Model):
  __tablename__ = 'sensors'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  attribute = db.Column(db.String(128), unique=True)
  comment = db.Column(db.String(256))
  data = db.relationship("Datum")

  # Transfer Function
  # y = c_1 x + c_2
  c_1 = db.Column(db.Float)
  c_2 = db.Column(db.Float)

  def __init__(self, name=None, attribute=None, comment='', c_1=1.0, c_2=0.0):
    self.name = name
    self.attribute = attribute.lower()
    self.comment = comment
    self.c_1 = c_1
    self.c_2 = c_2

  def __repr__(self):
    return '<Sensor %r attr:%r>' % (self.name, self.attribute)
