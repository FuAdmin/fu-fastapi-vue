# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class ButtonFilters(FuFilters):
    menu_id: str | None = Field(default=None, alias="menu_id")


class ButtonBase(BaseModel):
    name: str = Field(default=None, alias="name")
    code: str = Field(default=None, alias="code")
    sort: int = Field(default=None, alias="sort")
    method: int | None = Field(default=None, alias="method")
    api: str | None = Field(default=None, alias="api")
    menu_id: str | None = Field(default=None, alias="menu_id")


class ButtonIn(ButtonBase):
    pass


class ButtonOut(ButtonBase, FuSchema):

    class Config:
        from_attributes = True