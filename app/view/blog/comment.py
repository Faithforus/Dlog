from flask import request, redirect, render_template, jsonify
from sqlalchemy import and_
from app.view.blog import blog_bp
from app.model import db, session_commit
from app.model.comment import Comment
from app.model.guest import Guest
from app.form.admin import CommentForm, get_errors_msg
from app.lib.email import send_mail
from app.lib.common import trueReturn, falseReturn
from app.ext import limiter, gfw


@blog_bp.route('/comment', methods=["POST"])
@limiter.limit('30 per day,8 per hour')
def comment():
    form = CommentForm(request.values)
    if form.validate():
        email = form.email.data
        guest = Guest.query.filter_by(guest_email=email).first()
        if guest:
            if guest.state and not guest.black:  # 检验成功，未被拉黑
                c = Comment()
                res = c.add_comment(form, guest.nickname, yes=True)
                if res is not None:
                    return jsonify(trueReturn(msg="留言成功！", data=res))
                if res is None:
                    return jsonify(falseReturn(msg='网络错误'))
            if guest.black:
                return jsonify(falseReturn(msg='此邮箱在小黑屋反省中...'))
        if not guest or not guest.state:
            c = Comment()
            res = c.add_comment(form)
            token = Guest.generate_token({"email": email, "id": c.id})
            send_mail(to=email, subject="Dlog留言", template='email/confirm_comment', token=token)
            return jsonify(trueReturn(msg='此邮箱为第一次留言,为确认是否有效,请登录邮箱查看并确认,后续不再检验.'), data="")
    if not form.validate():
        msg = get_errors_msg(form.errors)
        return jsonify(falseReturn(msg=msg))


@blog_bp.route('/yourname/<string:token>', methods=['GET'])
def yourname(token):
    return render_template('email/active_comment.html', token=token)


@blog_bp.route('/active_comment', methods=['POST'])
def active_comment():
    nickname = request.values.get('nickname')
    if not nickname or not gfw.check(nickname):
        return render_template('email/active_comment.html', error='昵称为空或包含敏感词汇')
    token = request.values.get('token')
    res = Guest.decode_token(token)
    if res == "签名过期":
        return render_template('page_404.html')
    email = res['email']
    id = res['id']
    """新留言激活，加昵称"""
    comt = Comment.query.filter(and_(Comment.guest_email == email, Comment.id == id)).first()
    comt.guest_name = nickname
    comt.display = True
    """新建访客"""
    gst = Guest()
    gst.nickname = nickname
    gst.guest_email = email
    gst.state = True
    """同时提交"""
    db.session.add_all([comt, gst])
    error = session_commit()
    if not error:
        print('发布成功')
        return render_template('email/active_comment.html', msg="检验成功!留言已发布")
    return render_template('email/active_comment.html', error='网络错误')
