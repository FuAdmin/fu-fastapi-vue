from fastapi import Depends, APIRouter
from common.fu_async_crud import create, delete, update, retrieve, export_data

from common.fu_pagination import FuPage
from common.fu_schema import ImportSchema, IdSchema
from .model import Dict
from .schema import DictOut, DictIn, DictFilters

router = APIRouter(tags=["Dict"])


@router.post("/dict", response_model=IdSchema)
async def create_dict(data: DictIn):
    validate_fields = ["name", "code"]
    instance = await create(data, Dict, validate_fields)
    return instance


@router.delete("/dict/{dict_id}", response_model=IdSchema)
async def delete_dict(dict_id: str):
    instance = await delete(dict_id, Dict)
    return instance


@router.put("/dict/{dict_id}", response_model=IdSchema)
async def update_dict(dict_id: str, data: DictIn):
    validate_fields = ["name", "code"]
    instance = await update(dict_id, data, Dict, validate_fields)
    return instance


@router.get("/dict")
async def query_dicts(params: DictFilters = Depends()) -> FuPage[DictOut]:
    instance_list = await retrieve(Dict, DictOut, order_by="sort", filters=params)
    return instance_list


@router.get("/dict/export/data")
async def export_dict():
    export_fields = ["name", "code", "sort"]
    return await export_data(Dict, DictOut, export_fields)
