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
import json
import os.path
from pathlib import Path, PurePosixPath

from filelock import FileLock
from linktools import Config, utils
from linktools.cli import subcommand, subcommand_argument
from linktools.decorator import cached_property
from linktools.rich import choose, confirm
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
            DSM_DISK_FMT="qcow2",
            DSM_DISK_SIZE="6G",
        )

    @cached_property
    def exposes(self) -> [ExposeLink]:
        return [
            self.expose_public("DSM", "nas", "群晖系统", self.load_nginx_url("DSM_DOMAIN")),
            self.expose_private("DSM", "nas", "群晖系统", self.load_port_url("DSM_EXPOSE_PORT", https=False)),
        ]

    # @property
    # def mount_paths(self):
    #     result = []
    #     with self._config_lock:
    #         config = self._load_config()
    #         mount_paths = config.setdefault("mount_paths", {})
    #         for mount_path in mount_paths.values():
    #             result.append(mount_path)
    #     return result
    #
    # @subcommand("ls", help="list dsm storage path")
    # def on_list_file(self):
    #     with self._config_lock:
    #         config = self._load_config()
    #         mount_paths = config.setdefault("mount_paths", {})
    #         for mount_path in mount_paths.values():
    #             self.logger.info(mount_path)
    #
    # @subcommand("add", help="add dsm storage path")
    # @subcommand_argument("src", help="host path")
    # @subcommand_argument("dest", help="dsm path")
    # @subcommand_argument("-p", "--permission", choices=("ro", "rw"))
    # def on_add_file(self, src: str, dest: str, permission: str = "rw"):
    #     src_path = Path(os.path.expanduser(src)).absolute()
    #     dest_path = PurePosixPath("/storage", dest).as_posix()
    #     if not os.path.exists(src_path):
    #         self.logger.error(f"{src_path} not exists.")
    #         return
    #     with self._config_lock:
    #         config = self._load_config()
    #         mount_path = f"{src_path}:{dest_path}:{permission}"
    #         mount_paths = config.setdefault("mount_paths", {})
    #         if dest_path in mount_paths:
    #             if not confirm(f"{dest_path} is mounted: {mount_paths.get(dest_path)}, overwrite it?"):
    #                 self.logger.info(f"cancel")
    #                 return
    #         mount_paths[dest_path] = mount_path
    #         self._dump_config(config)
    #         self.logger.info(f"add {mount_path}")
    #
    # @subcommand("rm", help="remove dsm storage path")
    # def on_remove_file(self):
    #     with self._config_lock:
    #         config = self._load_config()
    #         mount_paths = config.setdefault("mount_paths", {})
    #         if not mount_paths:
    #             self.logger.error("not found any mount path")
    #             return
    #         dest_path = choose(
    #             "Choose mount path",
    #             choices=mount_paths
    #         )
    #         mount_path = mount_paths.pop(dest_path)
    #         self._dump_config(config)
    #         self.logger.info(f"remove {mount_path}")

    def on_starting(self):
        self.write_nginx_conf(
            domain=self.get_config("OMV_DOMAIN"),
            url="http://dsm:5000",
        )

    # @cached_property
    # def _config_lock(self):
    #     return FileLock(self.get_app_path("config.json", create_parent=True))
    #
    # @cached_property
    # def _config_path(self):
    #     return self.get_app_path("config.json.lock", create_parent=True)
    #
    # def _load_config(self):
    #     try:
    #         if os.path.exists(self._config_path):
    #             return json.loads(utils.read_file(self._config_path, text=True))
    #     except Exception as e:
    #         self.logger.warning(f"load {self} config error: {e}")
    #     return {}
    #
    # def _dump_config(self, config):
    #     utils.write_file(self._config_path, json.dumps(config))
