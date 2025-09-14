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
from linktools.decorator import cached_property
from linktools_cntr import BaseContainer, ExposeLink


class Container(BaseContainer):

    @property
    def dependencies(self) -> [str]:
        return ["nginx"]

    @cached_property
    def configs(self):
        return dict(
            HOME_ASSISTANT_TAG="stable",
            HOME_ASSISTANT_DOMAIN=self.get_nginx_domain("homeassistant"),
            HOME_ASSISTANT_EXPOSE_PORT=Config.Alias(type=int, default=8123),
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_public("HomeAssistant", "homeAssistant", "Home Assistant", self.load_nginx_url("HOME_ASSISTANT_DOMAIN")),
            self.expose_container("HomeAssistant", "homeAssistant", "Home Assistant", self.load_port_url("HOME_ASSISTANT_EXPOSE_PORT", https=False)),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.get_config("HOME_ASSISTANT_DOMAIN"),
            self.get_source_path("nginx.conf"),
        )
