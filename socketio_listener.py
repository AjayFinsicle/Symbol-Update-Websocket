from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(message):
    print('Message received: ', message)
    socketio.emit('message', message)

if __name__ == '__main__':
    socketio.run(app, port=9999)
