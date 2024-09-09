#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097

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