import re

import pytest

from pylinuxauto.config import config


def pytest_addoption(parser):
    parser.addoption("--slaves", action="store", default="", help="")


@pytest.fixture(scope="session")
def slaves(pytestconfig):
    _slaves = pytestconfig.getoption("slaves")
    s = []
    if _slaves:
        for slave in _slaves.split("/"):
            slave_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", slave)
            if slave_info:
                user, ip, password = slave_info[0]
                s.append(
                    {
                        "user": user,
                        "ip": ip,
                        "password": password or config.PASSWORD,
                    }
                )
    if not s:
        raise EnvironmentError("No slaves found, check -s/--slaves value")
    return s


@pytest.fixture(scope="session")
def pylinuxauto():
    import pylinuxauto as pla
    return pla


@pytest.fixture(scope="session")
def sleep():
    from pylinuxauto.sleepx import sleep as slp
    return slp
