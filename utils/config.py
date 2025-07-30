import json
import os
from threading import Lock

# --- 核心代码开始 ---

# 确保我们能正确找到 config.json 文件，无论从哪里运行脚本
# 这会获取当前文件(config.py)所在的目录
_current_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.join(_current_dir, 'config.json')

# 创建一个线程锁，以防止多线程同时写入配置文件导致数据错乱
_lock = Lock()


def _deep_update(source, overrides):
    """
    深度更新字典。
    会递归地合并字典，而不是直接替换。
    """
    for key, value in overrides.items():
        if isinstance(value, dict) and key in source:
            source[key] = _deep_update(source.get(key, {}), value)
        else:
            source[key] = value
    return source


def load_config():
    """
    从 config.json 文件加载配置。
    """
    with _lock:
        try:
            with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或格式错误，可以返回一个空字典或默认配置
            return {}


def update_config(json_string: dict) -> bool:
    """
    接收一个JSON字符串，解析它并用其内容更新配置文件。
    只会更新传入JSON中存在的键，不会删除或覆盖其他键。

    :param json_string: 配置字典。
    :return: 如果成功则返回 True，否则返回 False。
    """
    try:
        # 1. 解析传入的JSON字符串
        if not isinstance(json_string, dict):
            print("错误：JSON字符串必须解析为一个对象（字典）。")
            return False
    except json.JSONDecodeError:
        print(f"错误：传入的字符串不是有效的JSON格式: {json_string}")
        return False

    # 2. 读取当前的完整配置
    current_config = load_config()
    with _lock:

        # 3. 深度合并配置，用新数据覆盖旧数据
        updated_config = _deep_update(current_config, json_string)

        # 4. 将更新后的完整配置写回文件
        try:
            with open(CONFIG_FILE_PATH, 'w', encoding='utf-8') as f:
                # indent=4 让JSON文件保持格式化，易于阅读
                json.dump(updated_config, f, ensure_ascii=False, indent=4)

            # 5. 更新当前运行时的全局配置变量
            config.clear()
            config.update(updated_config)

            return True
        except IOError as e:
            print(f"错误：无法写入配置文件 {CONFIG_FILE_PATH}: {e}")
            return False


# --- 核心代码结束 ---

# 创建一个全局配置变量，项目启动时加载一次
# 其他模块可以直接从这里导入和使用配置
config = load_config()