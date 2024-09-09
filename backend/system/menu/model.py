# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from common.fu_model import CoreModel, UUIDStr
from system.button.model import Button

from system.role.model import role_menu_association


class Menu(CoreModel):
    __tablename__ = "sys_menu"

    parent_id = Column(UUIDStr, nullable=True, comment="Parent Menu Id")
    icon = Column(String(64), default="ant-design:book-outlined", comment="Menu Icon")
    title = Column(String(64), comment="Menu Title")
    is_embed_link = Column(Boolean, default=False, comment="Embed Link")
    frame_src = Column(String(2550), nullable=True, comment="Frame Src")
    type = Column(Integer, comment="Type of Menu")
    path = Column(String(2550), nullable=True, comment="Route Path")
    redirect = Column(String(128), nullable=True, comment="Redirect Path")
    component = Column(String(128), nullable=True, comment="Component Path")
    name = Column(String(50), nullable=True, comment="Component Name")
    status = Column(Boolean, default=True, nullable=True, comment="Menu Status")
    keep_alive = Column(Boolean, default=False, nullable=True, comment="Keep Alive")
    hide_menu = Column(Boolean, default=False, nullable=True, comment="Hide Menu")
    template_id = Column(UUIDStr, nullable=True, comment="Template Id")

    # 定义一对多关系
    button = relationship(Button, back_populates="menu")

    # 定义多对多关系
    role = relationship(
        "Role",
        secondary=role_menu_association,
        back_populates="menu",
    )