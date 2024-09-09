#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
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
