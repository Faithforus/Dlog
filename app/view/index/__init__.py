from flask import Blueprint

index_bp = Blueprint('index_bp',__name__)


import app.view.index.index_view
