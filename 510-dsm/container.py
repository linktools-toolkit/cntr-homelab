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

from linktools import Config, utils
from linktools.decorator import cached_property
from linktools_cntr import BaseContainer, ExposeLink


class Container(BaseContainer):

    @property
    def dependencies(self) -> [str]:
        return ["nginx"]

    @cached_property
    def configs(self):
        return dict(
            DSM_TAG="latest",
            DSM_DOMAIN="",
            DSM_EXPOSE_PORT=Config.Alias(type=int, default=5000),
            DSM_DISK_SIZE="16G",
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_public("DSM", "nas", "群晖系统", self.load_nginx_url("DSM_DOMAIN")),
            self.expose_private("DSM", "nas", "群晖系统", self.load_config_url("DSM_LOCAL_URL")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            domain=self.get_config("OMV_DOMAIN"),
            url="http://dsm:5000",
        )

