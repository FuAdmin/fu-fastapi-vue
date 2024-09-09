# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from datetime import datetime
from pydantic import BaseModel, Field


class FuSchema(BaseModel):
    id: str
    # sys_creator: str | None
    # sys_modifier: str | None
    sys_create_datetime: datetime | None = None
    sys_update_datetime: datetime | None = None
    sys_flag: bool | None = None
    sort: int | None = None


class ImportSchema(BaseModel):
    path: str


class IdSchema(BaseModel):
    id: str


class FuFilters(BaseModel):
    sys_creator: str | None = Field(None)


def response_success(data="success"):
    return {"detail": data}