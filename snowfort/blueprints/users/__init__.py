from flask import Blueprint

mod = Blueprint('users', __name__, url_prefix='/users')

import views
