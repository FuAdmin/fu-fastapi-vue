#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
from sqlalchemy import Column, String, Text, Integer
from common.fu_model import CoreModel


class LogLogin(CoreModel):
    __tablename__ = "sys_log_login"

    username = Column(String(32), nullable=True, comment="登录用户名")
    ip = Column(String(32), nullable=True, comment="登录ip")
    agent = Column(Text, nullable=True, comment="agent信息")
    browser = Column(String(200), nullable=True, comment="浏览器名")
    os = Column(String(200), nullable=True, comment="操作系统")
    continent = Column(String(50), nullable=True, comment="州")
    country = Column(String(50), nullable=True, comment="国家")
    province = Column(String(50), nullable=True, comment="省份")
    city = Column(String(50), nullable=True, comment="城市")
    district = Column(String(50), nullable=True, comment="县区")
    isp = Column(String(50), nullable=True, comment="运营商")
    area_code = Column(String(50), nullable=True, comment="区域代码")
    country_english = Column(String(50), nullable=True, comment="英文全称")
    country_code = Column(String(50), nullable=True, comment="简称")
    longitude = Column(String(50), nullable=True, comment="经度")
    latitude = Column(String(50), nullable=True, comment="纬度")
    login_type = Column(Integer, default=1, comment="登录类型")
