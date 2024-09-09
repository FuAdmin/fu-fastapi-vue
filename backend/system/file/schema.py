# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel, Field
from common.fu_schema import FuSchema, FuFilters


class FileFilters(FuFilters):
    file_name__like: str | None = Field(default=None, alias="name")


class FileBase(BaseModel):
    file_name: str
    save_name: str
    size: int
    url: str


class FileIn(BaseModel):
    name: str = Field(None, alias="name")
    url: str = Field(None, alias="url")


class FileOut(FileBase, FuSchema):

    class Config:
        from_attributes = True


class UploadFileIn(BaseModel):
    folder: str = Field("", alias="folder")