# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
from fastapi import Depends, APIRouter
from common.fu_async_crud import create, delete, update, retrieve, export_data

from common.fu_pagination import FuPage
from common.fu_schema import ImportSchema, IdSchema
from .model import Post
from .schema import PostOut, PostIn, PostFilters

router = APIRouter(tags=["Post"])


@router.post("/post", response_model=IdSchema)
async def create_post(data: PostIn):
    validate_fields = ["name", "code"]
    instance = await create(data, Post, validate_fields)
    return instance


@router.delete("/post/{post_id}", response_model=IdSchema)
async def delete_post(post_id: str):
    instance = await delete(post_id, Post)
    return instance


@router.put("/post/{post_id}", response_model=IdSchema)
async def update_post(post_id: str, data: PostIn):
    validate_fields = ["name", "code"]
    instance = await update(post_id, data, Post, validate_fields)
    return instance


@router.get("/post")
async def query_posts(params: PostFilters = Depends()) -> FuPage[PostOut]:
    instance_list = await retrieve(Post, PostOut, filters=params)
    return instance_list


@router.get("/post/export/data")
async def export_post():
    export_fields = ["name", "code", "sort"]
    return await export_data(Post, PostOut, export_fields)