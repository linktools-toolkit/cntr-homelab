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
import uuid

from linktools import Config
from linktools.container import BaseContainer
from linktools.decorator import cached_property


class Container(BaseContainer):

    @property
    def dependencies(self) -> [str]:
        return ["nginx"]

    @cached_property
    def configs(self):
        return dict(
            XRAY_TAG="latest",
            XRAY_DOMAIN=self.get_nginx_domain(),
            XRAY_ID=Config.Prompt(default=str(uuid.uuid4()), cached=True),
            XRAY_PATH=Config.Prompt(default="/go/go/go/let/us/go", cached=True),
        )

    def on_starting(self):
        self.render_template(
            os.path.join(self.root_path, "config.json"),
            self.get_app_path("etc", "xray", "config.json", create_parent=True),
        )

        self.write_nginx_conf(
            self.manager.config.get("XRAY_DOMAIN"),
            self.get_path("nginx.conf"),
        )
