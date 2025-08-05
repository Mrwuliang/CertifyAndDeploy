# certificate/core/file_processing.py
import os
import zipfile
import tempfile
import shutil
import subprocess
import requests
from urllib.parse import urlparse
from pathlib import Path


def download_file(url, save_path=None, chunk_size=8192, timeout=30, headers=None, verify_ssl=True):
    """
    从指定的 URL 下载文件。

    Args:
        url (str): 要下载的文件的 URL。
        save_path (str, optional): 文件保存的本地路径。如果为 None，则使用 URL 中的文件名保存在当前目录。
        chunk_size (int, optional): 每次读取数据块的大小（字节）。默认 8192 (8KB)。
        timeout (int, optional): 请求超时时间（秒）。默认 30 秒。
        headers (dict, optional): 请求头。例如，可以用来设置 User-Agent。
        verify_ssl (bool, optional): 是否验证 SSL 证书。默认 True。如果遇到证书问题可设为 False (不推荐用于生产环境)。

    Returns:
        str: 成功下载时返回保存的文件路径，失败时返回 None 或抛出异常。

    Raises:
        requests.exceptions.RequestException: 网络请求相关异常（超时、连接错误、HTTP 错误等）。
        IOError: 本地文件写入错误。
    """
    try:
        # 如果没有指定保存路径，则从 URL 解析文件名
        if save_path is None:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            # 如果 URL 没有文件名（例如指向目录或动态脚本），提供一个默认名
            if not filename or '.' not in filename:
                filename = 'downloaded_file'
            save_path = filename

        # 确保保存路径的目录存在
        save_dir = Path(save_path).parent
        if save_dir != Path('.'):  # 如果父目录不是当前目录
            save_dir.mkdir(parents=True, exist_ok=True)  # 创建所有必要的父目录

        print(f"开始下载: {url}")
        print(f"保存路径: {save_path}")

        # 发起 GET 请求，流式下载 (stream=True) 以节省内存，尤其适合大文件
        response = requests.get(url, stream=True, timeout=timeout, headers=headers, verify=verify_ssl)
        response.raise_for_status()  # 检查 HTTP 错误状态码 (如 404, 500)

        # 获取文件总大小（如果服务器提供）
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        # 以二进制写模式打开文件
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # 过滤掉保持连接的空块
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    # 显示下载进度（可选）
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        print(f"\r下载进度: {progress:.1f}% ({downloaded_size}/{total_size} bytes)", end='', flush=True)
            # 下载完成后换行
            if total_size > 0:
                print()  # 移到下一行

        print(f"下载完成！文件已保存至: {save_path}")
        return save_path

    except requests.exceptions.RequestException as e:
        print(f"下载请求失败: {e}")
        # 可以选择在此处记录日志或进行其他错误处理
        return None
    except IOError as e:
        print(f"文件写入失败: {e}")
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None


def unzip_and_rename_keys(zip_file_path, extract_to_path, output_filename):
    """
    解压一个可能包含多层嵌套的压缩包，查找.key和.pem文件，
    将它们重命名并移动到指定目录，然后删除原始压缩包。

    :param zip_file_path: 压缩包文件的完整路径。
    :param extract_to_path: 解压后文件存放的目标目录。
    :param output_filename: 新的文件名（不带扩展名）。
    """
    # 确保目标目录存在
    if not os.path.exists(extract_to_path):
        os.makedirs(extract_to_path)


    from utils.config import config
    config = config.get('config')

    # 创建一个临时目录来处理解压
    with tempfile.TemporaryDirectory() as temp_dir:
        # 定义一个递归函数来查找和处理文件
        def find_files_recursively(current_zip_path, search_dir):
            found_key = None
            found_pem = None

            try:
                with zipfile.ZipFile(current_zip_path, 'r') as zf:
                    zf.extractall(search_dir)
                    for item in zf.infolist():
                        extracted_item_path = os.path.join(search_dir, item.filename)
                        if item.filename.endswith('.key'):
                            found_key = extracted_item_path
                        elif item.filename.endswith(config.get('ssl_format')):
                            found_pem = extracted_item_path
                        elif item.filename.endswith('.zip'):
                            # 递归处理内层压缩包
                            key_path, pem_path = find_files_recursively(extracted_item_path, os.path.join(search_dir, "nested"))
                            if key_path:
                                found_key = key_path
                            if pem_path:
                                found_pem = pem_path
            except zipfile.BadZipFile:
                print(f"警告: {current_zip_path} 不是一个有效的zip文件或已损坏。")

            return found_key, found_pem

        # 从最外层压缩包开始查找
        key_file_path, pem_file_path = find_files_recursively(zip_file_path, temp_dir)

        # 检查是否找到了需要的文件
        if not key_file_path:
            print("错误：在压缩包中未找到.key文件。")
            return
        if not pem_file_path:
            print("错误：在压缩包中未找到.pem文件。")
            return

        # 构建新的文件路径并移动文件
        new_key_path = os.path.join(extract_to_path, f"{output_filename}.key")
        new_pem_path = os.path.join(extract_to_path, f"{output_filename}.pem")

        shutil.move(key_file_path, new_key_path)
        shutil.move(pem_file_path, new_pem_path)

        print(f"成功找到并解压文件到: {extract_to_path}")
        print(f"  - {new_key_path}")
        print(f"  - {new_pem_path}")

    # 删除原始压缩包
    try:
        os.remove(zip_file_path)
        print(f"成功删除原始压缩包: {zip_file_path}")
    except OSError as e:
        print(f"删除原始压缩包时出错: {e}")


def SCRIPT():
    """
    执行重启nginx脚本
    :return:
    """
    # 同样，在函数内部获取配置
    from utils.config import config
    config = config.get('config')
    restart_nginx = config.get('nginx_position')

    try:
        res = subprocess.run([restart_nginx, '-t'], check=True, text=True)
        if 'ok' in res:
            subprocess.run([restart_nginx, '-s', 'reload'], check=True, text=True)
            return '部署成功'
    except subprocess.CalledProcessError as e:
        print(e)
        return e