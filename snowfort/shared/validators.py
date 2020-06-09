from sqlalchemy import func
from wtforms import ValidationError

class Unique(object):
  """
  Validator that checks field uniqueness.
  """
  def __init__(self, model, field, message=None):
    self.model = model
    self.field = field
    if not message:
      message = "This element already exists."
    self.message = message

  def __call__(self, form, field):
    check = self.model.query.filter(func.lower(self.field) == func.lower(field.data)).first()
    if 'id' in form:
      id = form.id.data
    else:
      id = None
    if check and (id is None or id != check.id):
      raise ValidationError(self.message)
