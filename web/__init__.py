import os
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

from .web_controller import web_bp

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
template_dir = os.path.join(current_dir, '..', 'templates')
static_dir = os.path.join(current_dir, '..', 'static')

app.template_folder = template_dir
app.static_folder = static_dir
app.register_blueprint(web_bp)