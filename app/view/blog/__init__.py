from flask import Blueprint

blog_bp = Blueprint('blog_bp',__name__)

import app.view.blog.imgs
import app.view.blog.comment