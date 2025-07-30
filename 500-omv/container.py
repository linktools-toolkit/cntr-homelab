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
   /  oooooooooooooooo  .o.  oooo /,   `,"-----------
  / ==ooooooooooooooo==.o.  ooo= //   ,``--{)B     ,"
 /_==__==========__==_ooo__ooo=_/'   /___________,"
"""
from typing import Iterable

from linktools.decorator import cached_property
from linktools_cntr import BaseContainer, ExposeLink


class Container(BaseContainer):

    @property
    def dependencies(self) -> Iterable[str]:
        return ["flare", "nextcloud", "qbittorrent"]

    @cached_property
    def configs(self):
        return dict(
            PVE_DOMAIN=self.get_nginx_domain("pve"),
            PVE_LOCAL_URL="https://10.10.10.254:8006",
            PRIMARY_GATEWAY_DOMAIN=self.get_nginx_domain("primary-gateway"),
            PRIMARY_GATEWAY_LOCAL_URL="http://10.10.10.253:80",
            BYPASS_GATEWAY_DOMAIN=self.get_nginx_domain("bypass-gateway"),
            BYPASS_GATEWAY_LOCAL_URL="http://10.10.10.252:80",

            OMV_LOCAL_URL="http://10.10.10.1:80",
            OMV_DOMAIN="",
            DSM_LOCAL_URL="",
            DSM_DOMAIN="",
        )

    @cached_property
    def exposes(self) -> Iterable[ExposeLink]:
        return [
            self.expose_public("Proxmox", "server", "虚拟化环境", self.load_nginx_url("PVE_DOMAIN")),
            self.expose_public("PrimaryGateway", "RouterNetwork", "主路由管理", self.load_nginx_url("PRIMARY_GATEWAY_DOMAIN")),
            self.expose_public("BypassGateway", "RouterNetwork", "旁路由管理", self.load_nginx_url("BYPASS_GATEWAY_DOMAIN")),
            self.expose_public("OpenMediaVault", "nas", "OMV系统", self.load_nginx_url("OMV_DOMAIN")),
            self.expose_public("DSM", "nas", "群晖系统", self.load_nginx_url("DSM_DOMAIN")),

            self.expose_private("Proxmox", "server", "虚拟化环境", self.load_config_url("PVE_LOCAL_URL")),
            self.expose_private("PrimaryGateway", "RouterNetwork", "主路由管理", self.load_config_url("BYPASS_GATEWAY_LOCAL_URL")),
            self.expose_private("BypassGateway", "RouterNetwork", "旁路由管理", self.load_config_url("PRIMARY_GATEWAY_LOCAL_URL")),
            self.expose_private("OpenMediaVault", "nas", "OMV系统", self.load_config_url("OMV_LOCAL_URL")),
            self.expose_private("DSM", "nas", "群晖系统", self.load_config_url("DSM_LOCAL_URL")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.get_config("PVE_DOMAIN"),
            self.get_path("nginx", "pve.conf"),
            name="pve",
        )
        self.write_nginx_conf(
            self.get_config("PRIMARY_GATEWAY_DOMAIN"),
            self.get_path("nginx", "primary-gateway.conf"),
            name="primary-gateway",
        )
        self.write_nginx_conf(
            self.get_config("BYPASS_GATEWAY_DOMAIN"),
            self.get_path("nginx", "bypass-gateway.conf"),
            name="bypass-gateway",
        )
