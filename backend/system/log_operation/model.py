# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
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