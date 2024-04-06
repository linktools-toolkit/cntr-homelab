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
            COLLABORA_SERVER_TAG="latest",
            COLLABORA_SERVER_DOMAIN=self.get_nginx_domain("collabora"),
            COLLABORA_SERVER_EXPOSE_PORT=None,
            COLLABORA_SERVER_USERNAME=Config.Prompt(default="admin", type=str, cached=True),
            COLLABORA_SERVER_PASSWORD=Config.Prompt(default="collabora", type=str, cached=True),
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_container("collabora-code-server", "MicrosoftOffice", "", self.load_port_url("COLLABORA_SERVER_EXPOSE_PORT", https=False)),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.manager.config.get("COLLABORA_SERVER_DOMAIN"),
            self.get_path("nginx.conf"),
        )
