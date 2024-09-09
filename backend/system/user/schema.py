# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm

from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class UserFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")
    mobile__like: str | None = Field(default=None, alias="mobile")
    dept_id__in: str | None = Field(default=None, alias="dept_id")


class UserBase(BaseModel):
    username: str = Field(default=None, alias="username")
    email: str | None = Field(default=None, alias="email")
    mobile: str | None = Field(default=None, alias="mobile")
    avatar: str | None = Field(default=None, alias="avatar")
    name: str | None = Field(default=None, alias="name")
    gender: int | None = Field(default=0, alias="gender")
    dept_id: str | None = Field(default=None, alias="dept")


class UserIn(UserBase):
    post: list | None = Field(default=None, alias="post")
    role: list | None = Field(default=None, alias="role")
    password: str | None = Field(default=None, alias="password")


class UserOut(UserBase, FuSchema):
    post: list | None = Field(default=None, alias="post")
    role: list | None = Field(default=None, alias="role")

    class Config:
        from_attributes = True


class RePasswordIn(BaseModel):
    id: str
    password: str