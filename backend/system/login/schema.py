# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel


class LoginOut(BaseModel):
    id: str
    token: str
    access_token: str
    expireTime: int
    username: str
    name: str


class LoginIn(BaseModel):
    username: str = None
    password: str = None


class UserInfoOut(BaseModel):
    username: str = None
    name: str = None
    avatar: str | None = None
    id: str = None