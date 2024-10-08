# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from sqlalchemy import (
    Boolean,
    Column,
    String,
)

from common.fu_model import CoreModel, UUIDStr


class Dept(CoreModel):
    __tablename__ = "sys_dept"

    name = Column(String(64), nullable=False, comment="Department Name")
    owner = Column(String(32), nullable=True, comment="Department Owner")
    phone = Column(String(32), nullable=True, comment="Department Phone")
    email = Column(String(32), nullable=True, comment="Department Email")
    status = Column(Boolean, default=True, comment="Department Status")
    parent_id = Column(UUIDStr, nullable=True, comment="Department Parent")