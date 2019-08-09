from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer

from app.model import Base


class Setting(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    home_page = Column(Text)
    login_email = Column(Boolean, default=False)


setting_col = {
    "home_page": "首页简介",
    "login_email": "登录邮箱验证"
}
