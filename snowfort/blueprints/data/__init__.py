from flask import Blueprint

mod = Blueprint('data', __name__, url_prefix='/data')

import views
