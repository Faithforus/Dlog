from datetime import datetime
import time
import bleach
from markdown import markdown
from sqlalchemy import Column, String, DateTime, Integer, Text
from app.model import Base, db


class Blog(Base):
    id = Column(Integer, primary_key=True)
    blog_id = Column(String(32), default=lambda: str(int(time.time())))
    title = Column(String(128))
    body = Column(Text)
    category = Column(String(32))
    body_html = Column(Text)
    create_time = Column(DateTime, index=True, default=lambda: datetime.now())

    # @staticmethod
    # def on_changed_body(target, value, oldvalue, initiator):
    #     allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
    #                     'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
    #                     'h1', 'h2', 'h3', 'p', 'img', 'video', 'div', 'iframe', 'p', 'br', 'span', 'hr', 'src', 'class']
    #     allowed_attrs = {'*': ['class'],
    #                      'a': ['href', 'rel'],
    #                      'img': ['src', 'alt']}
    #     target.body_html = bleach.linkify(bleach.clean(
    #         markdown(value, output_format='html'),
    #         tags=allowed_tags, strip=True, attributes=allowed_attrs))


# db.event.listen(Blog.body, 'set', Blog.on_changed_body)

blog_col = {
    "id": "ID",
    'blog_id': "博客ID",
    "title": "标题",
    "category": "类别",
    "body": "内容",
    "body_html": "内容html",
    "create_time": "创建时间"
}
