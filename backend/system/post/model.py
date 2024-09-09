# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from common.fu_model import CoreModel
from system.user.model import user_post_association


class Post(CoreModel):
    __tablename__ = "sys_post"

    name = Column(String(64), unique=True, comment="岗位名称")
    code = Column(String(64), unique=True, comment="岗位代码")

    user = relationship(
        "User",
        secondary=user_post_association,
        back_populates="post",
    )