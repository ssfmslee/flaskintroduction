from snowfort import db

class Mote(db.Model):
  __tablename__ = 'motes'
  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(128), unique=True)
  type = db.Column(db.String(128))
  sampling = db.Column(db.Float)  # Sampling Frequency (Times per second)
  comment = db.Column(db.String(256))
  last_pkt = db.Column(db.Integer) # Tracking
  received = db.Column(db.Integer)
  missed = db.Column(db.Integer)
  station_id = db.Column(db.Integer, db.ForeignKey('stations.id'))
  station = db.relationship("Station")
  data = db.relationship("Datum")

  def __init__(self, tag=None, type=None, station_id=None, sampling=None, comment='',
               last_pkt=None, received=0, missed=0):
    self.tag = tag
    self.type = type
    self.sampling = sampling
    self.station_id = station_id
    self.comment = comment
    self.last_pkt = last_pkt
    self.received = received
    self.missed = missed

  def __repr__(self):
    return '<Mote id:%r tag:%r>' % (self.id, self.tag)
