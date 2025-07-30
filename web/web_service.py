from flask import request, render_template, jsonify

from core.ali_ssl import Sample
from core.file_processing import download_file, unzip_and_rename_keys, SCRIPT
from core.tencent_ssl import apply_certificate, describe_certificate, download_certificate_url


def index():
    return render_template('index.html')


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


def ssl():
    if request.is_json:
        new_config = request.get_json()
        apply_certificate(new_config.get('domainName'))


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

                print(f"检测到DV验证信息: 域名={domain_name}, RR={rr}, Value={value}")

                # 4. 调用阿里云DNS解析功能
                try:
                    sample = Sample()
                    result = sample.main(domain_name=domain_name, rr=rr, value=value)
                    if result:
                        return 'success'
                except Exception as e:
                    print(f"调用ali_ssl.main时发生内部错误: {e}")

            else:
                return jsonify({"status": "error", "message": "证书验证信息为空"}), 400
        else:
            return jsonify({"status": "error", "message": "证书验证信息为空"}), 400
    except Exception as e:
        print(e)


def deploy_certificate():
    if request.is_json:
        new_config = request.get_json()
        result = download_certificate_url(new_config.get('ssl_id'))
        save_path = download_file(result.get('DownloadCertificateUrl'), 'temp/' + result.get('DownloadFilename'))
        if save_path:
            from utils.config import config
            config = config.get('config', {})
            unzip_and_rename_keys(save_path, config.get('ssl_path'), new_config.get('ssl_name'))

