from flask import request, render_template, jsonify

from core.ali_ssl import Sample
from core.file_processing import download_file, unzip_and_rename_keys, SCRIPT
from core.tencent_ssl import apply_certificate, describe_certificate, download_certificate_url, check_certificate_domain_verification
from web import socketio
import time


def index():
    from utils.config import config
    config = config.get('config', {})
    return render_template('index.html', config=config)


def config():
    from utils.config import config
    config = config.get('config', {})
    return render_template('config.html', config=config)


def update():
    if request.is_json:
        new_config = request.get_json()
        from utils.config import update_config
        update_config(new_config)
        print("接收到更新的数据:", new_config['config'])
        # 返回成功响应
        return jsonify({"status": "success", "message": "配置已更新"}), 200
    return jsonify({"status": "error", "message": "请求格式错误"}), 400


def apply_ssl_logic(ssl_data):
    """
    处理SSL证书申请的核心业务逻辑。
    """
    from utils.config import config
    config_data = config.get('config', {})

    if not config_data.get('TENCENT_CLOUD', {}).get('SECRET_ID'):
        error_msg = "未填写腾讯云 SECRET_ID，2秒后将自动跳转到配置页面..."
        socketio.emit('log', {"code": 10001, "status": "error", "message": error_msg})
        return

    domain_name = ssl_data.get('domainName')
    if not domain_name:
        socketio.emit('log', {"code": 0, "status": "error", "message": "域名不能为空"})
        return

    socketio.emit('log', {"code": 0, "status": "info", "message": "开始申请免费证书..."})
    result = apply_certificate(domain_name)
    CertificateId = result.get('CertificateId')

    if CertificateId:
        socketio.emit('log', {"code": 0, "status": "success", "message": f"申请成功，证书ID：{CertificateId}"})
        socketio.emit('log', {"code": 0, "status": "info", "message": "开始验证域名所有权..."})

        ssl_result = ssl_detail(CertificateId)
        if ssl_result:
            socketio.emit('log', {"code": 0, "status": "success", "message": "域名验证成功，等待证书签发..."})

            max_retries = 30
            retry_count = 0

            while retry_count < max_retries:
                statu = check_certificate_domain_verification(CertificateId)
                issued = statu.get('VerificationResults', {}).get('Issued')

                if issued:
                    socketio.emit('log', {"code": 0, "status": "success", "message": "证书已签发，准备部署证书..."})
                    deploy_certificate(CertificateId, domain_name)
                    break
                else:
                    socketio.emit('log', {"code": 0, "status": "waiting",
                                          "message": f"证书尚未签发，10秒后将再次重试... ({retry_count + 1}/30)"})
                    time.sleep(10)
                    retry_count += 1
            else:
                socketio.emit('log', {"code": -1, "status": "failed", "message": "证书在5分钟内未完成签发，请手动查询证书申请情况。"})
        else:
            socketio.emit('log', {"code": 0, "status": "error", "message": "域名验证失败"})
    else:
        error_message = result.get("Error", {}).get("Message", "未知错误")
        socketio.emit('log', {"code": 0, "status": "error", "message": f"证书申请失败: {error_message}"})


def ssl_detail(ssl_id):
    try:
        detail = describe_certificate(ssl_id)
        # 2. 检查DV证书验证信息是否存在
        DvAuthDetail = detail.get('DvAuthDetail')
        if DvAuthDetail:
            DvAuthKeySubDomain = DvAuthDetail.get('DvAuthKeySubDomain')
            if DvAuthKeySubDomain:
                # 3. 提取动态参数
                domain_name = DvAuthDetail.get('DvAuths')[0].get('DvAuthDomain')
                rr = DvAuthKeySubDomain
                value = DvAuthDetail.get('DvAuthValue')
                # 4. 调用阿里云DNS解析功能
                try:
                    sample = Sample()
                    result = sample.main(domain_name=domain_name, rr=rr, value=value)
                    if result:
                        return True
                except Exception as e:
                    print(f"调用ali_ssl.main时发生内部错误: {e}")
                    return False

            else:
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False


def deploy_certificate(ssl_id: str, ssl_name: str):
    result = download_certificate_url(ssl_id)
    socketio.emit('log', {"code": 0, "status": "success", "message": "开始下载证书..."})
    save_path = download_file(result.get('DownloadCertificateUrl'), 'temp/' + result.get('DownloadFilename'))
    if save_path:
        from utils.config import config
        config = config.get('config', {})
        unzip_and_rename_keys(save_path, config.get('ssl_path'), ssl_name)
        result = SCRIPT()
        socketio.emit('log', {"code": 0, "status": "failed", "message": result})