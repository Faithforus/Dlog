from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer

from app.model import Base


class RecycleBin(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(64))
    content = Column(Text())
    operator = Column(String(64))
    create_at = Column(DateTime)
    restore = Column(Boolean, default=False)


recycle_bin_col = {
    "table_name": "表名",
    "content": "内容",
    "operator": "操作者",
    "create_at": "删除时间",
    "restore": "还原"
}