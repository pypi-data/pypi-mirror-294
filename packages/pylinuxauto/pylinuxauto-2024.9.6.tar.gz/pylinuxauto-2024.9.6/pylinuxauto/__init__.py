import os
from typing import Union, List

os.environ["DISPLAY"] = ":0"
from pylinuxauto.attr import Attr
from pylinuxauto.attr.dogtail.tree import Node
from pylinuxauto.ui import UI
from pylinuxauto.mousekey.mkmixin import MouseKeyChainMixin
from pylinuxauto.image.image_base import ImageBase
from pylinuxauto.mousekey import *
from pylinuxauto.screenshot import *
from pylinuxauto.file import *
from pylinuxauto.sleepx import sleep


def is_child_find_element_by_attr(appname, child_name):
    return Attr(appname=appname).obj.is_child(child_name=child_name)


def find_element_children_by_attr(appname, child_name):
    return Attr(appname=appname).obj.child(child_name=child_name).children


def window_sizes_by_ui(appname: str, config_path: str):
    from pylinuxauto.ui.ui_base import ButtonCenter
    return ButtonCenter(appname=appname, config_path=config_path).window_sizes()


def window_center_by_ui(appname: str, config_path: str):
    from pylinuxauto.ui.ui_base import ButtonCenter
    return ButtonCenter(appname=appname, config_path=config_path).window_center()


def btn_size_by_ui(appname: str, config_path: str, btn_name: str):
    from pylinuxauto.ui.ui_base import ButtonCenter
    return ButtonCenter(appname=appname, config_path=config_path).btn_size(btn_name)


def find_element_by_attr_name(
        *,
        appname: str = "",
        name: str = "",
        role_name: str = "",
        description: str = "",
        label: str = "",
        recursive: bool = True,
        retry: bool = False,
        debugName: str = None,
        showingOnly=None
) -> Node:
    return Attr().find_element_by_attr_name(
        appname=appname,
        name=name,
        role_name=role_name,
        description=description,
        label=label,
        recursive=recursive,
        retry=retry,
        debugName=debugName,
        showingOnly=showingOnly
    )


def find_element_by_attr_path(attr_path) -> Node:
    return Attr().find_element_by_attr_path(attr_path=attr_path)


def find_elements_to_the_end_by_attr(ele_name: str, appname: str = None):
    return Attr(appname=appname).find_elements_to_the_end(ele_name)


def find_element_by_image(
        *images,
        rate: Union[float, int] = None,
        multiple: bool = False,
        picture_abspath: str = None,
        screen_bbox: List[int] = None,
        network_retry: int = None,
        pause: [int, float] = None,
        timeout: [int, float] = None,
        max_match_number: int = None,
) -> MouseKeyChainMixin:
    from pylinuxauto.image import Image
    return Image().find_element_by_image(
        *images,
        rate=rate,
        multiple=multiple,
        picture_abspath=picture_abspath,
        screen_bbox=screen_bbox,
        network_retry=network_retry,
        pause=pause,
        timeout=timeout,
        max_match_number=max_match_number,
    )


def get_during(
        image_path: str,
        screen_time: Union[float, int],
        rate: float = None,
        pause: Union[int, float] = None,
        max_range: int = 10000,
):
    """
    在一段时间内截图多张图片进行识别，其中有一张图片识别成功即返回结果;
    适用于气泡类的断言，比如气泡在1秒内消失，如果用常规的图像识别则有可能无法识别到；
    :param image_path: 要识别的模板图片；
    :param screen_time: 截取屏幕图片的时间，单位秒；
    :param rate: 识别率；
    :param pause: 截取屏幕图片的间隔时间，默认不间隔；
    """
    return ImageBase().get_during(
        image_path=image_path,
        screen_time=screen_time,
        rate=rate,
        pause=pause,
        max_range=max_range
    )


def find_element_by_ocr(
        *target_strings,
        picture_abspath: str = None,
        similarity: [int, float] = 0.6,
        return_default: bool = False,
        return_first: bool = False,
        lang: str = "ch",
        network_retry: int = None,
        pause: [int, float] = None,
        timeout: [int, float] = None,
        max_match_number: int = None,
        bbox: dict = None,
) -> MouseKeyChainMixin:
    from pylinuxauto.ocr import OCR
    return OCR().find_element_by_ocr(
        *target_strings,
        picture_abspath=picture_abspath,
        similarity=similarity,
        return_default=return_default,
        return_first=return_first,
        lang=lang,
        network_retry=network_retry,
        pause=pause,
        timeout=timeout,
        max_match_number=max_match_number,
        bbox=bbox,
    )


def find_element_by_ui(
        btn_name,
        appname,
        config_path,
        number=-1,
        pause=1,
        retry=1,
        offset_x=None,
        multiplier_x=None,
        offset_y=None,
        multiplier_y=None,
) -> MouseKeyChainMixin:
    from pylinuxauto.ui import UI
    return UI().find_element_by_ui(
        btn_name,
        appname,
        config_path,
        number=number,
        pause=pause,
        retry=retry,
        offset_x=offset_x,
        multiplier_x=multiplier_x,
        offset_y=offset_y,
        multiplier_y=multiplier_y,
    )
