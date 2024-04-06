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
from linktools.cli import subcommand
from linktools.container import BaseContainer, ExposeLink
from linktools.decorator import cached_property


class Container(BaseContainer):

    @property
    def dependencies(self) -> [str]:
        return ["nginx"]

    @cached_property
    def configs(self):
        return dict(
            GITLAB_TAG="latest",
            GITLAB_DOMAIN=self.get_nginx_domain(),
            GITLAB_SSH_PORT=Config.Prompt(default=3001, type=int, cached=True),
            GITLAB_ROOT_PASSWORD=Config.Prompt(default="xxx123456xxxx", type=str, cached=True),  # gitlab默认root密码
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_public("Gitlab", "git", "代码仓库管理", self.load_nginx_url("GITLAB_DOMAIN")),
        ]

    @subcommand("fix", help="fix permissions")
    def on_exec_fix(self):
        self.manager.create_docker_process("exec", "gitlab", "update-permissions").check_call()
        self.manager.create_docker_process("restart", "gitlab").check_call()

    def on_starting(self):
        self.write_nginx_conf(
            self.manager.config.get("GITLAB_DOMAIN"),
            self.get_path("nginx.conf"),
        )

    def on_started(self):
        self.manager.create_docker_process("exec", "gitlab", "chown", "-R", "git:git", "/var/opt/gitlab").check_call()
        self.manager.create_docker_process("exec", "gitlab", "chmod", "-R", "777", "/var/opt/gitlab").check_call()
        # self.manager.create_docker_process("exec", "gitlab", "update-permissions").check_call()
        # self.manager.create_docker_process("restart", "gitlab").check_call()
