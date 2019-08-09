from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_babelex import Babel
from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO


from app.lib.dfa_check import DFAFilter


db = SQLAlchemy()

babel = Babel()

mail = Mail()

login_manager = LoginManager()

admin = Admin(name="Dog-Blog", template_mode='bootstrap3')

# cipher_key = lambda :Fernet.generate_key()
my_key = b'yvmvbV6sh_MFgzSxMEV5hlmI6v54NpnqpL7W6bjdPW0='
cipher = Fernet(my_key)

photos = UploadSet('photos', IMAGES)


socketio = SocketIO()


limiter = Limiter(key_func=get_remote_address,default_limits=["200 per day", "50 per hour"])

#敏感词汇处理
gfw = DFAFilter()
