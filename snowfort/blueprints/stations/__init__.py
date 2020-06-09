from flask import Blueprint

mod = Blueprint('stations', __name__, url_prefix='/stations')

import views
