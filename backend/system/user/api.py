# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from typing import List

from fastapi import Depends, APIRouter, Request, HTTPException, Query
from fastapi_async_sqlalchemy import db
from sqlalchemy import select
from common.fu_auth import get_user_by_token, set_password_hash
from common.fu_async_crud import create, retrieve, delete, update, get_instance_by_id

from common.fu_pagination import FuPage
from common.fu_schema import IdSchema
from .model import User
from .schema import UserOut, UserIn, RePasswordIn, UserFilters, UserBase

router = APIRouter(tags=["User"])


@router.post("/user", response_model=IdSchema)
async def create_user(data: UserIn):
    validate_fields = ["username", "email", "mobile"]
    instance = await create(data, User, validate_fields)
    return instance


@router.delete("/user/{user_id}", response_model=IdSchema)
async def delete_user(user_id: str):
    instance = await delete(user_id, User)
    return instance


@router.put("/user/{user_id}", response_model=IdSchema)
async def update_user(user_id: str, data: UserIn):
    validate_fields = ["username", "email", "mobile"]
    instance = await update(user_id, data, User, validate_fields)
    return instance


@router.get("/user")
async def query_users(
    dept_id__in: List[str] = Query(None, alias="dept_ids[]"),
    params: UserFilters = Depends(),
) -> FuPage[UserOut]:
    params.dept_id__in = dept_id__in
    instance_list = await retrieve(User, UserOut, filters=params)
    return instance_list


@router.put("/user/reset/password/{user_id}", response_model=IdSchema)
async def reset_password(user_id: str):
    result = await db.session.execute(select(User).filter(User.id == user_id))
    instance = result.scalar_one_or_none()
    if instance is None:
        raise HTTPException(404, "User Not Found")
    instance.password = set_password_hash("123456")
    await db.session.commit()
    return instance


@router.post("/user/set/password", response_model=UserOut)
async def repassword(data: RePasswordIn, request: Request):
    request_user = await get_user_by_token(request)
    request_user_id = request_user.id
    update_id = data.id
    if request_user_id == update_id:

        result = await db.session.execute(select(User).filter(User.id == update_id))
        instance = result.scalar_one_or_none()
        if instance is None:
            raise HTTPException(404, "User Not Found")
        instance.password = set_password_hash(data.password)
        await db.session.commit()
        return instance
    else:
        HTTPException(403, "NO Permission")


@router.get("/user/{user_id}", response_model=UserBase)
async def get_user(user_id: str):
    user = await get_instance_by_id(user_id, User, False)
    return user