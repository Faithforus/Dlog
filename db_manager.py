from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app.create_app import app
from app.ext import db

#需要导入要迁移的数据库模型
from app.model.blogger import Blogger
from app.model.blog import Blog
from app.model.comment import Comment
from app.model.guest import Guest
from app.model.setting import Setting


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db',MigrateCommand)
if __name__ == '__main__':
    manager.run()