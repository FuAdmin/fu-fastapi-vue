#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
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
