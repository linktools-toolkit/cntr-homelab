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

import random
import string

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
            ONLYOFFICE_SERVER_DOMAIN=self.get_nginx_domain("onlyoffice"),
            ONLYOFFICE_SERVER_EXPOSE_PORT=None,
            ONLYOFFICE_SERVER_JWT_SECRET=Config.Prompt(default="".join(random.sample(string.ascii_letters + string.digits, 12)), cached=True),
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        port = self.manager.config.get("ONLYOFFICE_SERVER_EXPOSE_PORT", type=int, default=0)
        return [
            self.expose_container("onlyoffice-document-server", "MicrosoftOffice", "", self.load_port_url(port, https=False)),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.manager.config.get("ONLYOFFICE_SERVER_DOMAIN"),
            self.get_path("nginx.conf"),
        )
