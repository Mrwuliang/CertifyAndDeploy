# -*- coding: utf-8 -*-
from typing import List

from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_credentials.models import Config
from alibabacloud_credentials.client import Client


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Alidns20150109Client:
        """
        使用凭据初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码建议使用更安全的无AK方式，凭据配置方式请参见：https://help.aliyun.com/document_detail/378659.html。
        # credential = CredentialClient()
        from utils.config import config
        config = config.get('config').get('ALIYUN')
        secret_id = config.get('ACCESS_KEY_ID')
        secret_key = config.get('ACCESS_KEY_SECRET')
        config = Config(
            type='access_key',
            access_key_id=secret_id,
            access_key_secret=secret_key,
        )
        cred = Client(config)
        config = open_api_models.Config(
            credential=cred
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Alidns
        config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
        return Alidns20150109Client(config)

    @staticmethod
    def main(domain_name: str, rr: str, value: str) -> None:
        client = Sample.create_client()
        add_domain_record_request = alidns_20150109_models.AddDomainRecordRequest(
            domain_name=domain_name,
            rr=rr,
            type='TXT',
            value=value
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.add_domain_record_with_options(add_domain_record_request, runtime)
            return True
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
            return False

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        add_domain_record_request = alidns_20150109_models.AddDomainRecordRequest(
            domain_name='fooldove.top',
            rr='game',
            type='TXT',
            value='12345678'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.add_domain_record_with_options_async(add_domain_record_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
