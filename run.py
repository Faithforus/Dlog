from app.create_app import app

from app.ext import socketio

if __name__ == '__main__':
    socketio.run(app)