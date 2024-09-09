#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
from pydantic import BaseModel, Field
from common.fu_schema import FuSchema, FuFilters


class LogOperationFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")
    code: str | None = Field(default=None, alias="code")


class LogOperationBase(BaseModel):
    request_username: str | None = Field(None)
    request_modular: str | None = Field(None)
    request_path: str | None = Field(None)
    request_body: str | None = Field(None)
    request_method: str | None = Field(None)
    request_msg: str | None = Field(None)
    request_ip: str | None = Field(None)
    request_browser: str | None = Field(None)
    response_code: str | None = Field(None)
    request_os: str | None = Field(None)
    json_result: str | None = Field(None)
    status: bool


class LogOperationIn(LogOperationBase):
    pass


class LogOperationOut(LogOperationBase, FuSchema):

    class Config:
        from_attributes = True
