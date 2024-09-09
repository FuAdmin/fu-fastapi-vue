# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from fastapi import Depends, APIRouter
from common.fu_async_crud import retrieve

from common.fu_pagination import FuPage
from .model import LogLogin
from .schema import LogLoginOut, LogLoginFilters

router = APIRouter(tags=["LogLogin"])


@router.get("/login_log")
async def query_login_logs(params: LogLoginFilters = Depends()) -> FuPage[LogLoginOut]:
    instance_list = await retrieve(LogLogin, LogLoginOut, filters=params)
    return instance_list