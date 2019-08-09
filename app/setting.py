DEBUG = True

DIALECT = 'mysql'  # 数据库类型
DRIVER = 'cymysql'  # 连接数据库驱动
DB_USERNAME = ''  # 用户名
DB_PASSWORD = ''  # 密码
HOST = 'localhost'  # 服务器
PORT = '3306'  # 端口
DATABASE = ''  # 数据库名

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, DB_USERNAME, DB_PASSWORD, HOST,
                                                                       PORT,
                                                                       DATABASE)

# blogger
USERNAME = 'Dlog'
PASSWORD = '000000'
EMAIL = ''

# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

#
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'a8b1985c9017d5ca6533f53a8e1d805d'

# img upload
import os

UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd() + '/app/blog_img/upload')
MAX_CONTENT_LENGTH = 2 * 1024 * 1024

# cookie
from datetime import timedelta
REMEMBER_COOKIE_DURATION = timedelta(hours=2)


PAGE_SIZE = 3
