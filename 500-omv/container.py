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
            DSM_LOCAL_URL="",

            JELLYFIN_LOCAL_URL="",
            JELLYFIN_DOMAIN="",
        )

    @cached_property
    def exposes(self) -> Iterable[ExposeLink]:
        return [
            self.expose_public("Proxmox", "server", "虚拟化环境", self.load_nginx_url("PVE_DOMAIN")),
            self.expose_public("PrimaryGateway", "RouterNetwork", "主路由管理", self.load_nginx_url("PRIMARY_GATEWAY_DOMAIN")),
            self.expose_public("BypassGateway", "RouterNetwork", "旁路由管理", self.load_nginx_url("BYPASS_GATEWAY_DOMAIN")),
            self.expose_public("Jellyfin", "movie", "jellyfin", self.load_nginx_url("JELLYFIN_DOMAIN")),

            self.expose_private("Proxmox", "server", "虚拟化环境", self.load_config_url("PVE_LOCAL_URL")),
            self.expose_private("PrimaryGateway", "RouterNetwork", "主路由管理", self.load_config_url("PRIMARY_GATEWAY_LOCAL_URL")),
            self.expose_private("BypassGateway", "RouterNetwork", "旁路由管理", self.load_config_url("BYPASS_GATEWAY_LOCAL_URL")),
            self.expose_private("OpenMediaVault", "nas", "OMV系统", self.load_config_url("OMV_LOCAL_URL")),
            self.expose_private("DSM", "nas", "群晖系统", self.load_config_url("DSM_LOCAL_URL")),
            self.expose_private("Jellyfin", "movie", "jellyfin", self.load_config_url("JELLYFIN_LOCAL_URL")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            domain=self.get_config("PVE_DOMAIN"),
            url=self.get_config("PVE_LOCAL_URL"),
            name="pve",
        )

        self.write_nginx_conf(
            domain=self.get_config("PRIMARY_GATEWAY_DOMAIN"),
            url=self.get_config("PRIMARY_GATEWAY_LOCAL_URL"),
            name="primary-gateway",
        )

        self.write_nginx_conf(
            domain=self.get_config("BYPASS_GATEWAY_DOMAIN"),
            url=self.get_config("BYPASS_GATEWAY_LOCAL_URL"),
            name="bypass-gateway",
        )

        self.write_nginx_conf(
            domain=self.get_config("JELLYFIN_DOMAIN"),
            url=self.get_config("JELLYFIN_LOCAL_URL"),
            name="jellyfin",
        )
