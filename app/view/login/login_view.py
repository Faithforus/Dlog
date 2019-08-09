from _datetime import datetime, timedelta

from flask import render_template, url_for, request, jsonify, redirect, session, current_app
from flask_login import login_user, current_user
from flask_socketio import emit, send

from app.view.login import login_bp
from app.form.admin import LoginForm, get_errors_msg
from app.lib.common import trueReturn, falseReturn
from app.lib.email import send_mail
from app.model.blogger import Blogger
from app.ext import limiter

def set_login(user):
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(hours=1)
    login_user(user)
    return


@login_bp.route('/Dlog', methods=['GET', "POST"])
def Dlog():
    if request.method == "POST":
        form = LoginForm(request.values)
        if form.validate():
            b = Blogger.query.filter_by(email=form.email.data).first()
            if b and b.check_pwd(form.password.data):
                if b.role == "Faith":
                    if not current_app.config.get('LOGIN_EMAIL'):
                        set_login(b)
                        emit('receive', trueReturn(data=url_for('admin.index')), namespace='/chat', broadcast=True)
                        return jsonify(falseReturn())
                    token = b.generate_token()
                    login_time = datetime.now()
                    send_mail(to=form.email.data, subject='登录确认',
                              template='email/confirm_login', user=b, token=token, login_time=login_time)
                    return jsonify(trueReturn(msg='E-mail sent successfully!'))
                else:
                    return jsonify(falseReturn(msg='Authentication failure'))
            else:
                return jsonify(falseReturn(msg="Email doesn't exist or Password error!"))
        else:
            return jsonify(falseReturn(msg=get_errors_msg(form.errors)))

    if request.method == "GET":
        return render_template('Dlog.html')


@login_bp.route('/confirm_login/<string:token>', methods=['GET'])
def confirm_login(token):
    """
    确认登录
    :return:
    """
    return render_template('email/active_login.html', token=token)


@login_bp.route('/active_login', methods=['POST'])
def active_login():
    token = request.values.get('token')
    result = Blogger.decode_token(token)
    if result == "签名过期":
        print(result)
        return render_template('page_404.html')
    uid = result['uid']
    b = Blogger.query.filter_by(uid=uid).first()
    if b:
        set_login(b)
        emit('receive', trueReturn(data=url_for('admin.index')), namespace='/chat', broadcast=True)
        print("login success")
        return render_template('email/active_login.html', msg='登录成功!请查看')
    print("not eamil")
    return render_template('page_404.html')


from app.ext import socketio


@socketio.on('my_connect', namespace='/chat')
def connect_handler(json):
    if json.get('key') != "0432e54857a2f97af2a411b9f00e5cd5":
        return False
    print('received message: ', json)
    # emit('receive', trueReturn(msg="Connect Success!"))
