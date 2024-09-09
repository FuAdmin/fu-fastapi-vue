#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from common.fu_model import CoreModel, UUIDStr
from system.user.model import user_post_association


class File(CoreModel):
    __tablename__ = "sys_file"

    file_name = Column(String(255), comment="实际名称")
    save_name = Column(String(255), comment="存储名称")
    file_type = Column(String(50), comment="文件类型")
    url = Column(String(255), comment="文件路径")
    size = Column(BigInteger, comment="大小")
    md5sum = Column(UUIDStr, comment="文件md5")