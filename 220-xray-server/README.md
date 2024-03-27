# xray scripts

先按照[文档](../../README.md)安装依赖项，然后按照以下命令部署docker容器

```
# 配置acme的dns类型
# 比如用的阿里云的dns就填dns_ali，顺带配上Ali_Key和Ali_Secret参数
# dns类型和所需参数参照：https://github.com/acmesh-official/acme.sh/wiki/dnsapi
ACME_DNS_API=dns_ali
Ali_Key=xxx
Ali_Secret=yyy

# 开始部署环境变量
python3 manager.py add xray aliyun-ddns portainer # 其中aliyun-ddns portainer可选
python3 manager.py up
```
