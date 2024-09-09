#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
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
