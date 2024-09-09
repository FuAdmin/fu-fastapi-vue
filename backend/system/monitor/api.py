# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from fastapi import APIRouter

from common.utils.system import System

router = APIRouter(tags=["Monitor"])


@router.get("/monitor")
def monitor():
    info = System().GetSystemAllInfo()
    return info