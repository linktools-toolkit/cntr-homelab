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
import os

from linktools import Config
from linktools.container import BaseContainer, ExposeLink
from linktools.decorator import cached_property


class Container(BaseContainer):

    @property
    def dependencies(self) -> [str]:
        return ["nginx"]

    @cached_property
    def configs(self):
        return dict(
            QBITTORRENT_TAG="latest",
            QBITTORRENT_DOMAIN=self.get_nginx_domain(),
            QBITTORRENT_EXPOSE_PORT=None,
            QBITTORRENT_TORRENTING_PORT=6881,
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_container("qBittorrent", "tools", "", self.load_port_url("QBITTORRENT_EXPOSE_PORT", https=False)),
            self.expose_public("qBittorrent", "tools", "", self.load_nginx_url("QBITTORRENT_DOMAIN")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.manager.config.get("QBITTORRENT_DOMAIN"),
            self.get_path("nginx.conf"),
        )

    def on_started(self):
        uid = self.manager.config.get("DOCKER_UID")
        if os.stat(self.get_app_path()).st_uid != uid:
            self.manager.change_owner(
                self.get_app_path(),
                self.manager.config.get("DOCKER_USER"),
            )
        if os.stat(self.get_download_path("qbittorrent")).st_uid != uid:
            self.manager.change_owner(
                self.get_download_path("qbittorrent"),
                self.manager.config.get("DOCKER_USER"),
            )
