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
            ALIST_TAG="latest",
            ALIST_DATA_PATH=Config.Prompt(cached=True, type="path") | self.get_app_data_path("data"),
            ALIST_ADMIN_PASSWORD=Config.Prompt(cached=True) | utils.make_uuid()[:12],
            ALIST_DOMAIN=self.get_nginx_domain(),
            ALIST_EXPOSE_PORT=Config.Alias(type=int) | 0,
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_container("Alist", "folderSync", "", self.load_port_url("ALIST_EXPOSE_PORT", https=False)),
            self.expose_public("Alist", "folderSync", "", self.load_nginx_url("ALIST_DOMAIN")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.get_config("ALIST_DOMAIN"),
            self.get_path("nginx.conf"),
        )
