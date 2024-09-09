# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class DictItemFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")
    code: str | None = Field(default=None, alias="code")


class DictItemBase(BaseModel):
    icon: str
    label: str
    value: str
    status: bool
    dict_id: str


class DictItemIn(DictItemBase):
    pass


class DictItemOut(DictItemBase, FuSchema):

    class Config:
        from_attributes = True