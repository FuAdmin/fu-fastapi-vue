#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
from sqlalchemy import Column, String, Text, Boolean
from common.fu_model import CoreModel


class LogOperation(CoreModel):
    __tablename__ = "sys_log_operation"

    request_username = Column(String(50), nullable=True, comment="请求用户")
    request_modular = Column(String(64), nullable=True, comment="请求模块")
    request_path = Column(String(400), nullable=True, comment="请求地址")
    request_body = Column(Text, nullable=True, comment="请求参数")
    request_method = Column(String(8), nullable=True, comment="请求方式")
    request_msg = Column(Text, nullable=True, comment="操作说明")
    request_ip = Column(String(32), nullable=True, comment="请求ip地址")
    request_browser = Column(String(64), nullable=True, comment="请求浏览器")
    response_code = Column(String(32), nullable=True, comment="响应状态码")
    request_os = Column(String(64), nullable=True, comment="操作系统")
    json_result = Column(Text, nullable=True, comment="返回信息")
    status = Column(Boolean, default=True, comment="响应状态")
