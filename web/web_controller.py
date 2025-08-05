from flask import Blueprint

from web import socketio
from .web_service import index, config, update, apply_ssl_logic, ssl_detail, deploy_certificate, shell

# 创建一个名为 'web' 的蓝图
web_bp = Blueprint('web', __name__)


@web_bp.route("/")
def _index():
    return index()


@web_bp.route("/config")
def _config():
    return config()


@web_bp.route("/updateConfig", methods=['POST'])
def _update():
    return update()


@socketio.on('/apply_ssl')
def _ssl(ssl_data):
    return apply_ssl_logic(ssl_data)


@web_bp.route('/getSslDetail/<ssl_id>')
def _ssl_detail(ssl_id):
    return ssl_detail(ssl_id)


@web_bp.route('/download', methods=['POST'])
def download():
    return deploy_certificate()