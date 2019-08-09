from flask import Flask
from flask_uploads import patch_request_class, configure_uploads

from app.ext import mail, login_manager, admin, db, babel, photos, socketio, limiter
from app.view.admin.admin_home_view import MyHomeView


def register_blueprint(app):
    from app.view.index import index_bp
    from app.view.blog import blog_bp
    from app.view.login import login_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(login_bp)


def init_app():
    app = Flask(__name__)

    app.config.from_object('app.setting')

    mail.init_app(app=app)

    configure_uploads(app, photos)
    patch_request_class(app, size=None)

    socketio.init_app(app=app)

    admin.init_app(app=app, index_view=MyHomeView())
    babel.init_app(app=app)

    limiter.init_app(app=app)

    login_manager.init_app(app=app)
    login_manager.login_view = 'page_404'
    login_manager.login_message = '温馨提醒：请先登录或注册'
    # 注册sqlalchemy
    db.init_app(app=app)
    # db.drop_all(app=app)
    db.create_all(app=app)

    register_blueprint(app)
    return app
