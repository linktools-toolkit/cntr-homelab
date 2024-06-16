# Homelab 环境搭建 （基于Docker）

## 开始使用

以基于debain的系统为例配置环境，其他系统请自行安装相应软件，包括Python3, Python3-pip, Git, Docker, Docker Compose

```bash
# Install Python3, Python3-pip, Git, Docker, Docker Compose
wget -qO- get.docker.com | bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git docker-compose-plugin
```

安装linktools库并添加homelab仓库

```bash
# Install linktools library and add redroid repository
python3 -m pip install -U "linktools[container]"
ct-cntr repo add https://github.com/ice-black-tea/cntr-homelab  # fetch code from remote repository
ct-cntr repo update                                             # update code from remote repository
```

## 容器部署

### Nas (主页、Nextcloud、...) 环境部署

👉 [搭建文档](400-omv/README.md)

### Xray Server (websocket + ssl + vless) 环境搭建

👉 [搭建文档](220-xray-server/README.md)

### Redroid (Redroid、Redroid-Builder) 环境搭建

👉 [搭建文档](https://github.com/redroid-rockchip)


## 常用命令

```bash
# 每个子命令都可以通过添加-h参数查看帮助
ct-cntr -h

#######################
# 代码仓库相关（支持git链接和本地路径）
#######################

# 添加仓库
ct-cntr repo add https://github.com/ice-black-tea/cntr-homelab 

# 拉去仓库最新代码
ct-cntr repo update

# 删除仓库
ct-cntr repo remove

#######################
# 容器安装列表管理
#######################

# 添加容器
ct-cntr add omv gitlab portainer vscode

# 删除容器
ct-cntr remove omv

#######################
# 容器管理
#######################

# 启动容器
ct-cntr up

# 重启容器
ct-cntr restart

# 停止容器
ct-cntr down

#######################
# 配置管理
#######################

# 查看容器docker配置
ct-cntr config

# 查看相关变量配置
ct-cntr config list

# 修改变量
ct-cntr config set ROOT_DOMAIN=test.com ACME_DNS_API=dns_ali Ali_Key=xxx Ali_Secret=yyy

# 删除变量
ct-cntr config unset ROOT_DOMAIN ACME_DNS_API Ali_Key Ali_Secret

# 使用vim编辑配置文件
ct-cntr config edit --editor vim
```
