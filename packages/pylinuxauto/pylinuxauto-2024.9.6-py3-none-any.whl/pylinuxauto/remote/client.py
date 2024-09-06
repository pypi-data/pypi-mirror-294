#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib
from xmlrpc.client import ServerProxy

from pylinuxauto.config import config
from pylinuxauto.remote.guard import guard_rpc


def client(ip, port):
    return ServerProxy(f"http://{ip}:{port}", allow_none=True)


@guard_rpc(f"{os.path.splitext(pathlib.Path(__file__).name)[0]}_{config.HOST_IP}")
def _rpc_gui_client(
        user=None,
        ip=None,
        password=None,
        auto_restart=False,
        project_abspath=None
):
    return client(ip=ip, port=config.RPC_PORT)