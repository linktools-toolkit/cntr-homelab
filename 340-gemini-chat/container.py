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
            GEMINI_TAG="latest",
            GEMINI_DOMAIN=self.get_nginx_domain("gemini"),
            GEMINI_API_KEY=Config.Prompt(cached=True),
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_public("Gemini", "zodiacGemini", "Gemini机器人", self.load_nginx_url("GEMINI_DOMAIN")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.get_config("GEMINI_DOMAIN"),
            self.get_path("nginx.conf"),
        )
