#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
from pylinuxauto.remote.client import _rpc_gui_client
from pylinuxauto.remote.rpc_method import RpcMethods



class RpcGui:

    def __init__(
            self,
            user,
            ip,
            password,
            project_abspath,
            auto_restart=False,
    ):
        self.user = user
        self.ip = ip
        self.password = password
        self.project_abspath = project_abspath
        self.auto_restart = auto_restart

    @property
    def rgui(self) -> RpcMethods:
        return _rpc_gui_client(
            user=self.user,
            ip=self.ip,
            password=self.password,
            auto_restart=self.auto_restart,
            project_abspath=self.project_abspath
        )


