# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from sqlalchemy import Column, String, Boolean, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from common.fu_model import CoreModel, Base

role_menu_association = Table(
    "sys_role_menu",
    Base.metadata,
    Column("role_id", ForeignKey("sys_role.id")),
    Column("menu_id", ForeignKey("sys_menu.id")),
)

role_button_association = Table(
    "sys_role_button",
    Base.metadata,
    Column("role_id", ForeignKey("sys_role.id")),
    Column("button_id", ForeignKey("sys_button.id")),
)


class Role(CoreModel):
    __tablename__ = "sys_role"

    name = Column(String(64), unique=True, comment="角色名称")
    code = Column(String(64), unique=True, comment="角色代码")
    status = Column(Boolean, default=True, comment="角色状态")
    data_range = Column(Integer, default=0, comment="数据范围")

    menu = relationship(
        "Menu",
        secondary=role_menu_association,
        back_populates="role",
    )

    button = relationship(
        "Button",
        secondary=role_button_association,
        back_populates="role",
    )

    user = relationship(
        "User",
        secondary="sys_user_role",
        back_populates="role",
    )