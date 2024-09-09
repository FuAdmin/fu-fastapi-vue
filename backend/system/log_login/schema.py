# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel, Field
from common.fu_schema import FuSchema, FuFilters


class LogLoginFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")
    code: str | None = Field(default=None, alias="code")


class LogLoginBase(BaseModel):
    username: str | None = Field(None)
    ip: str | None = Field(None)
    agent: str | None = Field(None)
    browser: str | None = Field(None)
    os: str | None = Field(None)
    continent: str | None = Field(None)
    country: str | None = Field(None)
    province: str | None = Field(None)
    city: str | None = Field(None)
    district: str | None = Field(None)
    isp: str | None = Field(None)
    area_code: str | None = Field(None)
    country_english: str | None = Field(None)
    country_code: str | None = Field(None)
    longitude: str | None = Field(None)
    latitude: str | None = Field(None)
    login_type: int | None = Field(None)


class LogLoginIn(LogLoginBase):
    pass


class LogLoginOut(LogLoginBase, FuSchema):

    class Config:
        from_attributes = True