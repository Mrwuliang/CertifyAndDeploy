## 自动申请证书加自动化部署
## 使用前注意
目前仅支持腾讯云申请证书，域名服务商仅支持阿里云

## 使用要求
- Python>=3.6

## 使用准备

首先当然是克隆代码并进入 CertifyAndDeploy 文件夹：

```
git clone https://github.com/Mrwuliang/CertifyAndDeploy.git
cd CertifyAndDeploy
pip3 install -r requirements.txt
```
首次启动先进入/config页面做一下基础配置，填写腾讯云和阿里云的SECRET密钥

### 运行
python3 main.py

## 使用

成功运行之后可以通过 [http://localhost:5555/](http://localhost:5555/)访问工具页
