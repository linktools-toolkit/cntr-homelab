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
from linktools.container import BaseContainer
from linktools.decorator import cached_property


class Container(BaseContainer):

    @cached_property
    def configs(self):
        return dict(
            ALI_DDNS_DOMAIN=Config.Alias("ROOT_DOMAIN", default=Config.Prompt(cached=True)),
            ALI_DDNS_ROOT_DOMAIN=Config.Alias("ROOT_DOMAIN", default=Config.Prompt(cached=True)),
            ALI_DDNS_KEY=Config.Alias("Ali_Key", default=Config.Prompt(cached=True)),
            ALI_DDNS_SECRET=Config.Alias("Ali_Secret", default=Config.Prompt(cached=True)),
            ALI_DDNS_CHECKLOCAL=False,
            ALI_DDNS_IPV4NETS="",
            ALI_DDNS_IPV6NETS="",
        )
