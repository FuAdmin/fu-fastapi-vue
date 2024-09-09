#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
from fastapi import Depends, APIRouter
from common.fu_async_crud import create, delete, update, retrieve, export_data

from common.fu_pagination import FuPage
from common.fu_schema import ImportSchema, IdSchema
from .model import DictItem
from .schema import DictItemOut, DictItemIn, DictItemFilters

router = APIRouter(tags=["DictItem"])


@router.post("/dict_item", response_model=IdSchema)
async def create_dict_item(data: DictItemIn):
    validate_fields = ["label", "value"]
    instance = await create(data, DictItem, validate_fields)
    return instance


@router.delete("/dict_item/{dict_item_id}", response_model=IdSchema)
async def delete_dict_item(dict_item_id: str):
    instance = await delete(dict_item_id, DictItem)
    return instance


@router.put("/dict_item/{dict_item_id}", response_model=IdSchema)
async def update_dict_item(dict_item_id: str, data: DictItemIn):
    validate_fields = ["label", "value"]
    instance = await update(dict_item_id, data, DictItem, validate_fields)
    return instance


@router.get("/dict_item")
async def query_dict_items(params: DictItemFilters = Depends()) -> FuPage[DictItemOut]:
    instance_list = await retrieve(DictItem, DictItemOut, filters=params)
    return instance_list
