#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from common.fu_model import CoreModel


class DictItem(CoreModel):
    __tablename__ = "sys_dict_item"

    icon = Column(String(100), comment="数据字典项ICON")
    label = Column(String(100), comment="数据字典项名称")
    value = Column(String(100), comment="数据字典项值")
    status = Column(Boolean, default=True, comment="数据字典项状态")
    dict_id = Column(
        ForeignKey("sys_dict.id", ondelete="SET NULL"), comment="数据字典ID"
    )