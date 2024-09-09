# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from fastapi import Depends, APIRouter
from common.fu_async_crud import retrieve

from common.fu_pagination import FuPage
from .model import LogOperation
from .schema import LogOperationOut, LogOperationFilters

router = APIRouter(tags=["LogOperation"])


@router.get("/operation_log")
async def query_login_logs(
    params: LogOperationFilters = Depends(),
) -> FuPage[LogOperationOut]:
    instance_list = await retrieve(LogOperation, LogOperationOut, filters=params)
    return instance_list