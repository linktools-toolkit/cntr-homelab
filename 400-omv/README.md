# nas

## 准备工作

1. 公网ip
2. 域名（需要配置cname记录"*"解析到本域名）

## 宿主机

### pve

1. 配置ip（10.10.10.254/24），网关（10.10.10.252），dns（10.10.10.252）
2. 安装omv、ikuai、openwrt虚拟机

## 虚拟机

### ikuai

1. 配置ip（10.10.10.253）
2. 配置dns（114.114.114.114，8.8.8.8）
3. 配置dhcp，客户端（10.10.10.0/24），网关（10.10.10.252），dns（10.10.10.252，10.10.10.253）
4. 配置拨号
5. 配置ddns
6. 配置端口映射，把需要暴露的接口映射到外网

### openwrt

1. 配置ip（10.10.10.252/24），网关（10.10.10.253），dns（114.114.114.114，8.8.8.8），忽略dhcp
2. 配置frpc
3. 配置passwall2
4. 配置vpn

### omv

1. 配置ip（10.10.10.1/24），网关（10.10.10.252），dns（10.10.10.252）
2. 配置用户
3. 配置文件系统
4. 配置各类文件系统服务
5. 安装docker
6. 使用本项目一键搭建nextcloud、acme等环境
7. 配置nextcloud定时任务（docker exec nextcloud php cron.php）

#### 部署

##### 部署docker容器

先按照[文档](../../README.md)安装依赖项，然后按照以下命令部署docker容器

```
# 以下export的环境变量，也可写在configs/config.py（需要自己创建，可参考configs/sample/config.py）文件中

# 配置acme的dns类型
# 比如用的阿里云的dns就填dns_ali，顺带配上Ali_Key和Ali_Secret参数
# dns类型和所需参数参照：https://github.com/acmesh-official/acme.sh/wiki/dnsapi
export ACME_DNS_API=dns_ali
export Ali_Key=xxx
export Ali_Secret=yyy

# 各个系统域名配置
export ROOT_DOMAIN="xxx"
# export WILDCARD_DOMAIN="true" # 必须打开泛域名解析，安装omv时默认打开
# export NEXTCLOUD_DOMAIN="nextcloud.$ROOT_DOMAIN"
# export ARIA2_DOMAIN="aria2.$ROOT_DOMAIN"
# export GITLAB_DOMAIN="gitlab.$ROOT_DOMAIN"
# export PVE_DOMAIN="pve.$ROOT_DOMAIN"
# export IKUAI_DOMAIN="ikuai.$ROOT_DOMAIN"
# export OPENWRT_DOMAIN="openwrt.$ROOT_DOMAIN"
# export VSCODE_DOMAIN="vscode.$ROOT_DOMAIN"
# export PORTAINER_DOMAIN="portainer.$ROOT_DOMAIN"

python3 manager.py add omv gitlab portainer vscode # omv中包含了（nextcloud、flare），其他的像（vscode、gitlab）按需添加
python3 manager.py up
```

##### 配置docker延迟加载

避免开机时未挂载硬盘的时候就加载容器，导致容器加载失败，通过以下命令编辑延迟启动docker：

```
SYSTEMD_EDITOR="vim" systemctl edit docker.service
```

添加以下配置实现延迟启动:

```
[Unit]
ExecStartPre=/bin/sleep 60
```
