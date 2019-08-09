from _datetime import datetime, timedelta
import json

from flask import request, redirect, url_for, session, current_app
from flask_login import current_user, logout_user

from flask_admin import BaseView as _BaseView, expose
from flask_admin.contrib.sqla import ModelView as _ModelView
from werkzeug.security import generate_password_hash

from app.ext import admin, babel
from app.model import db
from app.model.blogger import Blogger, blogger_col
from app.model.blog import Blog, blog_col
from app.model.recycle import RecycleBin, recycle_bin_col
from app.model.comment import Comment, comment_col
from app.model.setting import Setting, setting_col
from app.model.guest import Guest, guest_col
from app.lib.common import trueReturn, falseReturn

table_to_model = {
    'blogger': Blogger,
    'blog': Blog,
    "comment": Comment,
    'guest': Guest,
    'setting': Setting
}


def put_recycle_bin(table_name, content):
    data = {
        'table_name': table_name,
        'content': json.dumps(content, ensure_ascii=False)
    }
    recycle = RecycleBin()
    recycle.set_attrs(data)
    recycle.operator = 'Dlog'
    recycle.create_at = datetime.now()
    recycle.add(recycle)


def restore(table_name, content):
    model = table_to_model[table_name]
    restore_model = model()
    restore_model.set_attrs(content)
    restore_model.add(restore_model)


class ModelView(_ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            if current_user.role == "Faith":
                return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('page_404', next=request.url))


class BaseView(_BaseView):
    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            if current_user.role == "Faith":
                return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('page_404', next=request.url))


class Publish(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def publish(self):
        if request.method == 'GET':
            return self.render('admin/write_md.html')
        if request.method == 'POST':
            title = request.values.get("title")
            category = request.values.get("category")
            md = request.values.get('doc')
            html = request.values.get("html")
            if not title or not category or not md:
                msg = falseReturn(msg="是不是有什么没写就提交了啊")
                return self.render("admin/write_md.html", msg=msg, title=title, body=md)
            data = Blog()
            data.title = title
            data.category = category
            data.body = md
            data.body_html = html
            error = data.add(data)
            if not error:
                msg = trueReturn(msg='发布成功～')
                return self.render("admin/write_md.html", msg=msg)
            else:
                msg = falseReturn(msg="出错了～")
                return self.render("admin/write_md.html", msg=msg, title=title, body=md)


class Logout(BaseView):
    @expose('/')
    def logout(self):
        logout_user()
        return redirect(url_for('login_bp.Dlog'))


class BloggerView(ModelView):
    column_list = ['uid', "username", "password_", 'email', 'profile']
    column_labels = blogger_col
    form_columns = column_list
    can_delete = False
    can_create = False
    column_formatters = dict(password_=lambda v, c, m, p: m.password_[:10] + "...", )

    def on_model_change(self, form, model, is_created):
        if len(model.password_) > 56 and model.password_.startswith('pbkdf2:sha256:'):
            """防止再次加密"""
            model.password_ = model.password_
        else:
            model.password_ = generate_password_hash(model.password_)


class BlogView(ModelView):
    column_labels = blog_col
    column_searchable_list = blog_col.keys()
    column_filters = blog_col.keys()
    column_formatters = dict(body=lambda v, c, m, p: m.body[:30] + "...",
                             body_html=lambda v, c, m, p: m.body_html[:30] + "...")

    def on_model_delete(self, model):
        """回收"""
        data = dict()
        for col in blog_col.keys():
            if col == 'create_time':
                data[col] = getattr(model, col).strftime("%Y-%m-%d %H:%M:%S")
                continue
            data[col] = getattr(model, col)
        put_recycle_bin('blog', data)


class GuestView(ModelView):
    column_labels = guest_col
    column_searchable_list = guest_col.keys()
    column_filters = guest_col.keys()

    def on_model_delete(self, model):
        """回收"""
        data = dict()
        for col in guest_col.keys():
            if col == 'create_time':
                data[col] = getattr(model, col).strftime("%Y-%m-%d %H:%M:%S")
                continue
            data[col] = getattr(model, col)
        put_recycle_bin('guest', data)




class CommentView(ModelView):
    column_labels = comment_col
    column_searchable_list = comment_col.keys()
    column_filters = comment_col.keys()

    def on_model_delete(self, model):
        """回收"""
        data = dict()
        for col in comment_col.keys():
            if col == 'create_time':
                data[col] = getattr(model, col).strftime("%Y-%m-%d %H:%M:%S")
                continue
            data[col] = getattr(model, col)
        put_recycle_bin('comment', data)


class SettingView(ModelView):
    column_labels = setting_col

    def on_model_change(self, form, model, is_created):
        for key in setting_col.keys():
            current_app.config[key.upper()] = getattr(model, key)


class RecycleBinView(ModelView):
    column_list = recycle_bin_col.keys()
    column_searchable_list = column_list
    column_filters = column_list
    column_labels = recycle_bin_col

    column_editable_list = ["restore"]

    can_create = False
    can_edit = False
    column_formatters = dict(content=lambda v, c, m, p: m.content[:200] + "...")

    def on_model_change(self, form, model, is_created):
        """还原"""
        if model.restore is True:
            table_name = model.table_name
            content = json.loads(model.content)
            restore(table_name=table_name, content=content)
            RecycleBin.delete(RecycleBin(), model.id)


admin.add_view(BloggerView(Blogger, db.session, name='博主信息'))
admin.add_view(Publish(name='写博客', endpoint='publish'))
admin.add_view(BlogView(Blog, db.session, name='博客'))
admin.add_view(CommentView(Comment, db.session, name=u'评论'))
admin.add_view(GuestView(Guest, db.session, name=u'访客'))
admin.add_view(SettingView(Setting, db.session, name=u'系统设置'))
admin.add_view(RecycleBinView(RecycleBin, db.session, name=u'回收站'))
admin.add_view(Logout(name=u'注销', endpoint='logout', category='Logout'))


@babel.localeselector
def get_locale():
    return session.get('lang', 'zh_Hans_CN')
