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
from typing import Iterable
from urllib.parse import urlparse

from linktools import Config
from linktools.decorator import cached_property
from linktools_cntr import BaseContainer, ExposeLink


class Container(BaseContainer):

    @property
    def dependencies(self) -> Iterable[str]:
        return ["homelab"]

    @cached_property
    def configs(self):

        def get_term_url(config: Config):
            try:
                url = config.get("FNOS_LOCAL_URL")
                parsed = urlparse(url)
                return f"http://{parsed.hostname}:5122"
            except:
                return ""

        return dict(
            FNOS_DOMAIN=self.get_nginx_domain("fn"),
            FNOS_TERM_DOMAIN=self.get_nginx_domain("fntermx"),

            FNOS_LOCAL_URL="http://10.10.10.1:5666",
            FNOS_LOCAL_TERM_URL=Config.Lazy(get_term_url),
        )

    @cached_property
    def exposes(self) -> Iterable[ExposeLink]:
        return [
            self.expose_public("fnOS", "nas", "飞牛系统", self.load_nginx_url("FNOS_DOMAIN")),
            self.expose_private("fnOS", "nas", "飞牛系统", self.load_config_url("FNOS_LOCAL_URL")),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            domain=self.get_config("FNOS_DOMAIN"),
            url=self.get_config("FNOS_LOCAL_URL"),
        )
        self.write_nginx_conf(
            domain=self.get_config("FNOS_TERM_DOMAIN"),
            url=self.get_config("FNOS_LOCAL_TERM_URL"),
        )
