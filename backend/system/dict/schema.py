# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class DictFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")
    code: str | None = Field(default=None, alias="code")


class DictBase(BaseModel):
    name: str
    code: str
    status: bool
    sort: int


class DictIn(DictBase):
    pass


class DictOut(DictBase, FuSchema):

    class Config:
        from_attributes = True