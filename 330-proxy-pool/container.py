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
            PROXY_POOL_TAG="latest",
            PROXY_POOL_DOMAIN=self.get_nginx_domain(),
            PROXY_POOL_EXPOSE_PORT=Config.Alias(type=int, default=0),
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_public("Proxy Pool", "tools", "代理池", self.load_nginx_url("PROXY_POOL_DOMAIN")),
            self.expose_container("Proxy Pool", "tools", "代理池", self.load_port_url("PROXY_POOL_EXPOSE_PORT", https=False)),
        ]

    def on_starting(self):
        self.write_nginx_conf(
            self.get_config("PROXY_POOL_DOMAIN"),
            self.get_source_path("nginx.conf"),
        )
