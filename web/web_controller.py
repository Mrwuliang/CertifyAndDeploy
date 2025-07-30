from flask import Blueprint

from .web_service import index, config, update, ssl, ssl_detail, deploy_certificate

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


@web_bp.route("/getSsl", methods=['POST'])
def _ssl():
    return ssl()


@web_bp.route('/getSslDetail/<ssl_id>')
def _ssl_detail(ssl_id):
    return ssl_detail(ssl_id)


@web_bp.route('/download', methods=['POST'])
def download():
    return deploy_certificate()

