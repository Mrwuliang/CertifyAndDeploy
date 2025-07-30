import os
from flask import Flask
from .web_controller import web_bp # 从 web_service.py 导入蓝图

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
# 获取 config.yaml 的绝对路径
template_dir = os.path.join(current_dir, '..', 'templates')
static_dir = os.path.join(current_dir, '..', 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# 注册蓝图
app.register_blueprint(web_bp)