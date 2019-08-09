from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError, EqualTo, IPAddress

email_msg = "电子邮箱不符合规范!"
required_msg = "不能为空!"
name_msg = "用户名长度至少需要在4到20个字符之间"
pwd_msg = "密码长度至少需要在6到20个字符之间"


class EmailForm(Form):
    email = StringField('电子邮件', validators=[DataRequired(message="邮箱" + required_msg), Length(1, 64),
                                            Email(message=email_msg)])


class LoginForm(EmailForm):
    password = PasswordField('密码',
                             validators=[DataRequired(message='密码' + required_msg), Length(6, 20, message=pwd_msg)])

class CommentForm(EmailForm):
    text = StringField('留言',validators=[DataRequired(message="留言"+required_msg)])
    code = StringField('文章',validators=[DataRequired(message="文章"+required_msg)])


class ManagerForm(EmailForm):
    password = PasswordField('密码',
                             validators=[DataRequired(message='密码' + required_msg), Length(6, 20, message=pwd_msg)])


class GuideForm(Form):
    email = StringField('电子邮件', validators=[DataRequired(message="邮箱" + required_msg), Length(1, 64),
                                            Email(message=email_msg)])
    password = PasswordField('密码',
                             validators=[DataRequired(message='密码' + required_msg), Length(6, 20, message=pwd_msg),
                                         EqualTo('password2', message='两次输入密码不一致')])
    password2 = PasswordField('确认密码',
                              validators=[DataRequired(message='确认密码' + required_msg), Length(6, 20, message=pwd_msg)])
    # dbserver = StringField('数据库服务器',validators=[IPAddress(message='这不是有效的ip地址'),
    #                                             DataRequired(message='数据库服务器' + required_msg)])
    # dbport = StringField('数据库端口',validators=[DataRequired(message='数据库端口' + required_msg)])
    # dbusername = StringField('数据库用户名',validators=[DataRequired(message='数据库用户名' + required_msg)])
    # dbpwd = StringField('数据库密码',validators=[DataRequired(message='数据库密码' + required_msg)])
    # dbname = StringField('数据库名',validators=[DataRequired(message='数据库名' + required_msg)])


def get_errors_msg(errors):
    message = list()
    for item, msg in errors.items():
        message += msg
    return message
