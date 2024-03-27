#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author  : Hu Ji
@file    : deploy.py 
@time    : 2023/05/21
@site    :  
@software: PyCharm 

              ,----------------,              ,---------,
         ,-----------------------,          ,"        ,"|
       ,"                      ,"|        ,"        ,"  |
      +-----------------------+  |      ,"        ,"    |
      |  .-----------------.  |  |     +---------+      |
      |  |                 |  |  |     | -==----'|      |
      |  | $ sudo rm -rf / |  |  |     |         |      |
      |  |                 |  |  |/----|`---=    |      |
      |  |                 |  |  |   ,/|==== ooo |      ;
      |  |                 |  |  |  // |(((( [33]|    ,"
      |  `-----------------'  |," .;'| |((((     |  ,"
      +-----------------------+  ;;  | |         |,"
         /_)______________(_/  //'   | +---------+
    ___________________________/___  `,
   /  oooooooooooooooo  .o.  oooo /,   \,"-----------
  / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
 /_==__==========__==_ooo__ooo=_/'   /___________,"
"""
from linktools.container import BaseContainer, ExposeLink
from linktools.decorator import cached_property


class Container(BaseContainer):

    @property
    def dependencies(self) -> [str]:
        return ["flare", "nextcloud"]

    @cached_property
    def configs(self):
        return dict(
            PVE_DOMAIN=self.get_nginx_domain("pve"),
            PVE_LOCAL_URL="https://10.10.10.254:8006",
            IKUAI_DOMAIN=self.get_nginx_domain("ikuai"),
            IKUAI_LOCAL_URL="http://10.10.10.253:80",
            OPENWRT_DOMAIN=self.get_nginx_domain("openwrt"),
            OPENWRT_LOCAL_URL="http://10.10.10.252:80",

            OMV_LOCAL_URL="http://10.10.10.1:80",
            OMV_DOMAIN="",
            DSM_LOCAL_URL="",
            DSM_DOMAIN="",
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_public("Proxmox", "server", "虚拟化环境", self.load_nginx_url("PVE_DOMAIN")),
            self.expose_public("iKuai", "RouterNetwork", "主路由管理", self.load_nginx_url("IKUAI_DOMAIN")),
            self.expose_public("OpenWrt", "RouterNetwork", "旁路由管理", self.load_nginx_url("OPENWRT_DOMAIN")),
            self.expose_public("openmediavault", "nas", "OMV系统", self.load_nginx_url("OMV_DOMAIN")),
            self.expose_public("DSM", "nas", "群晖系统", self.load_nginx_url("DSM_DOMAIN")),

            self.expose_private("Proxmox", "server", "虚拟化环境", self.load_config_url("PVE_LOCAL_URL")),
            self.expose_private("iKuai", "RouterNetwork", "主路由管理", self.load_config_url("IKUAI_LOCAL_URL")),
            self.expose_private("OpenWrt", "RouterNetwork", "旁路由管理", self.load_config_url("OPENWRT_LOCAL_URL")),
            self.expose_private("openmediavault", "nas", "OMV系统", self.load_config_url("OMV_LOCAL_URL")),
            self.expose_private("DSM", "nas", "群晖系统", self.load_config_url("DSM_LOCAL_URL")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.manager.config.get("PVE_DOMAIN"),
            self.get_path("nginx", "pve.conf"),
            name="pve",
        )
        self.write_nginx_conf(
            self.manager.config.get("IKUAI_DOMAIN"),
            self.get_path("nginx", "ikuai.conf"),
            name="ikuai",
        )
        self.write_nginx_conf(
            self.manager.config.get("OPENWRT_DOMAIN"),
            self.get_path("nginx", "openwrt.conf"),
            name="openwrt",
        )
