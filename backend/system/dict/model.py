# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from sqlalchemy import Column, String, Boolean
from common.fu_model import CoreModel


class Dict(CoreModel):
    __tablename__ = "sys_dict"

    name = Column(String(100), unique=True, comment="数据字典名称")
    code = Column(String(100), unique=True, comment="数据字典代码")
    status = Column(Boolean, default=True, comment="数据字典状态")
    remark = Column(String(2000), comment="数据字典备注")