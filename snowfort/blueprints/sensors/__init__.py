from flask import Blueprint

mod = Blueprint('sensors', __name__, url_prefix='/sensors')

import views
