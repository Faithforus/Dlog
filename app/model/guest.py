from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer
from datetime import datetime
from app.model import Base


class Guest(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(32))
    guest_email = Column(String(32))
    state = Column(Boolean, default=False)
    black = Column(Boolean, default=False)

    @staticmethod
    def generate_token(data, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(data).decode('utf8')

    @staticmethod
    def decode_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf8'))
            return data
        except BadSignature as e:
            return "签名过期"


guest_col = {
    "nickname": "访客昵称",
    "guest_email": "访客email",
    "state": "检验状态",
    "black": "拉黑"
}
