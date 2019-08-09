from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer
from datetime import datetime

from app.ext import gfw
from app.model import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    blog_id = Column(String(32))
    guest_email = Column(String(32))
    guest_name = Column(String(32))
    comment = Column(Text)
    comment_clean = Column(Text)
    create_time = Column(DateTime, default=lambda: datetime.now())
    display = Column(Boolean)

    def add_comment(self, form, name="", yes=False):
        self.blog_id = form.code.data
        self.comment = form.text.data
        self.comment_clean = gfw.filter(form.text.data)
        self.guest_email = form.email.data
        self.guest_name = name
        self.display = yes
        error = self.add(self)
        if not error:
            create_time = self.create_time.strftime("%Y年 %m月 %d日 %H时:%M分")
            data = {"guest_name": self.guest_name, "comment": self.comment,
                    "create_time": create_time}
            return data
        return None


comment_col = {
    "blog_id": "博客id",
    "guest_email": "访客email",
    "guest_name": "访客昵称",
    "comment": "留言",
    "comment_clean": "留言清洗",
    "create_time": "创建时间",
    "display": "显示"
}
