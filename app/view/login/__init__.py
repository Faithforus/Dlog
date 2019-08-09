from flask import Blueprint


login_bp = Blueprint('login_bp',__name__)

import app.view.login.login_view