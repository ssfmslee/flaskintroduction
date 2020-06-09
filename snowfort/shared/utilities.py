from datetime import datetime

def to_epoch_seconds(date):
  epoch = datetime.utcfromtimestamp(0)
  return (date - epoch).total_seconds()
