# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class DeptFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")


class DeptBase(BaseModel):
    name: str
    owner: str | None = None
    phone: str | None = None
    email: str | None = None
    status: bool = True
    parent_id: str | None = None


class DeptIn(DeptBase):
    pass


class DeptOut(DeptBase, FuSchema):

    class Config:
        from_attributes = True