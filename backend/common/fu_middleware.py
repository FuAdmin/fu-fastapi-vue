# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from typing import Optional

from fastapi import Request, HTTPException
from fastapi_async_sqlalchemy import db
from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
    SimpleUser,
    AuthenticationError,
)
from starlette.middleware.base import BaseHTTPMiddleware

from common.fu_async_crud import create
from common.fu_auth import get_user_by_token, decode_token
from common.utils.request_util import get_os, get_browser
from config import WHITE_LIST
from system.log_operation.model import LogOperation


class FuHeaderUser(SimpleUser):
    def __init__(self, username: str, user_id: str) -> None:
        super().__init__(username)
        self.user_id = user_id


# 认证后端
class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(
        self, request: Request
    ) -> Optional[tuple[AuthCredentials, SimpleUser]]:
        path: str = request.get("path")
        if path in WHITE_LIST:
            return None
        try:
            payload = await decode_token(request)
            username: str | None = payload.get("username", None)
            user_id: str | None = payload.get("id", None)
            if username is None:
                raise HTTPException(
                    status_code=401, detail="Invalid authentication credentials"
                )
            return AuthCredentials(["authenticated"]), FuHeaderUser(username, user_id)
        except Exception as e:
            raise AuthenticationError("Invalid authentication credentials") from e


class LogOperationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        path: str = request.get("path")
        if path in WHITE_LIST:
            return response
        user = request.user
        info = {
            "request_username": user.username,
            "request_ip": getattr(request, "request_ip", "unknown"),
            "request_method": request.method,
            "request_path": path,
            "sys_creator_id": user.user_id,
            "response_code": str(response.status_code),
            "request_os": get_os(request),
            "request_browser": get_browser(request),
            "status": (
                True
                if response.status_code
                in [
                    200,
                ]
                else False
            ),
        }
        async with db() as async_db:
            await create(info, LogOperation, session=async_db.session)
        return response