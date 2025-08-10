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
    def items(self):
        import dotenv
        env = dotenv.dotenv_values(self.get_path("env"))
        return env

    @cached_property
    def configs(self):
        return dict(
            XIAOYA_ALIST_TAG="latest",
            XIAOYA_ALIST_DATA_PATH=Config.Prompt(cached=True, type="path") | self.get_app_data_path("data"),
            XIAOYA_ALIST_DOMAIN=self.get_nginx_domain(),
            XIAOYA_ALIST_EXPOSE_PORT=Config.Alias(type=int) | 0,
            XIAOYA_ALIST_ADMIN_PASSWORD=Config.Prompt(cached=True) | utils.make_uuid()[:12],
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_container("Xiaoya-Alist", "folderSync", "", self.load_port_url("XIAOYA_ALIST_EXPOSE_PORT", https=False)),
            self.expose_public("Xiaoya-Alist", "folderSync", "", self.load_nginx_url("XIAOYA_ALIST_DOMAIN")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.get_config("XIAOYA_ALIST_DOMAIN"),
            url="http://xiaoya-alist:5678",
        )
