from threading import Thread

from flask_mail import Message
from app import mail
from flask import current_app, render_template


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message('[Dlog]' + subject, sender=app.config['MAIL_USERNAME'], body='Test',
                  recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
