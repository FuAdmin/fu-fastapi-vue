# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class MenuFilters(FuFilters):
    title__like: str | None = Field(default=None, alias="title")


class MenuBase(BaseModel):
    parent_id: str | None = Field(default=None)
    icon: str = Field(default=None)
    title: str = Field(default=None)
    is_embed_link: bool = Field(default=None)
    frame_src: str | None = Field(default=None)
    type: int = Field(default=None)
    path: str | None = Field(default=None)
    redirect: str | None = Field(default=None)
    component: str | None = Field(default=None)
    name: str | None = Field(default=None)
    status: bool = Field(default=None)
    keep_alive: bool = Field(default=None)
    hide_menu: bool = Field(default=None)
    template_id: str | None = Field(default=None)
    button: list | None = Field(default=None)


class MenuIn(MenuBase):
    pass


class MenuOut(MenuBase, FuSchema):

    class Config:
        from_attributes = True