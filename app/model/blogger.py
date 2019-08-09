from flask import current_app
from sqlalchemy import Column, String, Integer, Boolean, Text
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
from flask_login import UserMixin

from app.model import Base
from app.ext import login_manager
from app.lib.common import generate_uid



class Blogger(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    uid = Column(String(16), unique=True, nullable=False, default=lambda: generate_uid())
    username = Column(String(32))
    email = Column(String(32))
    password_ = Column(String(256), nullable=False)
    role = Column(String(8), default="Faith")
    profile = Column(Text)

    def new_it(self):
        self.username = current_app.config['USERNAME']
        self.password = current_app.config['PASSWORD']
        self.email = current_app.config['EMAIL']
        return self.add(self)

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, raw):
        self.password_ = generate_password_hash(raw)

    def check_pwd(self, raw):
        if not self.password_:
            return False
        return check_password_hash(self.password_, raw)

    def generate_token(self, expiration=300):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'uid': self.uid}).decode('utf8')

    @staticmethod
    def decode_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf8'))
            return data
        except BadSignature as e:
            return "签名过期"


blogger_col = {
    "uid": 'UID',
    "username": "昵称",
    "password_": "密码",
    'email': "Email",
    "profile": "简介"

}


@login_manager.user_loader
def get_user(uid):
    return Blogger.query.get(uid)
