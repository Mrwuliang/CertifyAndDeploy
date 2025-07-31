# -*- coding: utf-8 -*-
import os
import json
import types
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models


def apply_certificate(url: str):
    from utils.config import config

    config = config.get('config').get('TENCENT_CLOUD')
    secret_id = config.get('SECRET_ID')
    secret_key = config.get('SECRET_KEY')
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性
        # 以下代码示例仅供参考，建议采用更安全的方式来使用密钥
        # 请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(secret_id, secret_key)
        # 使用临时密钥示例
        # cred = credential.Credential("SecretId", "SecretKey", "Token")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ApplyCertificateRequest()
        params = {
            "DvAuthMethod": "DNS",
            "DomainName": url
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ApplyCertificateResponse的实例，与请求对象对应
        resp = client.ApplyCertificate(req)
        # 输出json格式的字符串回包
        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


def describe_certificate(id: str):
    from utils.config import config
    config = config.get('config').get('TENCENT_CLOUD')
    secret_id = config.get('SECRET_ID')
    secret_key = config.get('SECRET_KEY')

    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性
        # 以下代码示例仅供参考，建议采用更安全的方式来使用密钥
        # 请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(secret_id, secret_key)
        # 使用临时密钥示例
        # cred = credential.Credential("SecretId", "SecretKey", "Token")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeCertificateRequest()
        params = {
            "CertificateId": id
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeCertificateResponse的实例，与请求对象对应
        resp = client.DescribeCertificate(req)
        # 输出json格式的字符串回包
        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
        return {}


def download_certificate_url(id: str) -> str:
    from utils.config import config
    config = config.get('config').get('TENCENT_CLOUD')
    secret_id = config.get('SECRET_ID')
    secret_key = config.get('SECRET_KEY')
    try:
        cred = credential.Credential(secret_id, secret_key)
        # 使用临时密钥示例
        # cred = credential.Credential("SecretId", "SecretKey", "Token")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeDownloadCertificateUrlRequest()
        params = {
            "CertificateId": id,
            "ServiceType": "nginx"
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeDownloadCertificateUrlResponse的实例，与请求对象对应
        resp = client.DescribeDownloadCertificateUrl(req)
        # 输出json格式的字符串回包
        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
        return {}


def check_certificate_domain_verification(CertificateId:str):
    try:
        from utils.config import config
        config = config.get('config').get('TENCENT_CLOUD')
        secret_id = config.get('SECRET_ID')
        secret_key = config.get('SECRET_KEY')
        cred = credential.Credential(secret_id, secret_key)
        # 使用临时密钥示例
        # cred = credential.Credential("SecretId", "SecretKey", "Token")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ssl_client.SslClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.CheckCertificateDomainVerificationRequest()
        params = {
            "CertificateId": CertificateId
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个CheckCertificateDomainVerificationResponse的实例，与请求对象对应
        resp = client.CheckCertificateDomainVerification(req)
        # 输出json格式的字符串回包
        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
        return {}