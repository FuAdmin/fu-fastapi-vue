# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
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