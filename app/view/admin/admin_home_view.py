from flask import redirect, url_for, request
from flask_login import current_user

from flask_admin import AdminIndexView as _AdminIndexView, expose


class AdminIndexView(_AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and not current_user.is_anonymous:
            if current_user.role == "Faith":
                return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('page_404', next=request.url))


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/admin_home.html')
