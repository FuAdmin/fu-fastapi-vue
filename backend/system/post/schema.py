# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel, Field
from common.fu_schema import FuSchema, FuFilters


class PostFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")
    code: str | None = Field(default=None, alias="code")


class PostBase(BaseModel):
    name: str
    code: str
    sort: int
    user: list | None = Field(default=None)


class PostIn(PostBase):
    pass


class PostOut(PostBase, FuSchema):

    class Config:
        from_attributes = True