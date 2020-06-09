from flask import Blueprint

mod = Blueprint('motes', __name__, url_prefix='/motes')

import views
