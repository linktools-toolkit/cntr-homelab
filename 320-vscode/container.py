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
            VSCODE_TAG="latest",
            VSCODE_DOMAIN=self.get_nginx_domain(),
            VSCODE_EXPOSE_PORT=None,
            VSCODE_PASSWORD=Config.Prompt(cached=True),
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_public("VS Code", "microsoftVisualStudioCode", "在线vscode", self.load_nginx_url("VSCODE_DOMAIN")),
            self.expose_container("VS Code", "microsoftVisualStudioCode", "在线vscode", self.load_port_url("VSCODE_EXPOSE_PORT", https=False)),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.manager.config.get("VSCODE_DOMAIN"),
            self.get_path("nginx.conf"),
        )

    def on_started(self):
        self.manager.change_owner(
            self.get_app_path(),
            self.manager.config.get("DOCKER_USER")
        )
        self.manager.change_owner(
            self.get_app_data_path(),
            self.manager.config.get("DOCKER_USER")
        )
