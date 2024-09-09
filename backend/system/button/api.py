from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from common.fu_async_crud import create, delete, update, retrieve, export_data

from common.fu_pagination import FuPage
from common.fu_schema import ImportSchema, IdSchema
from .model import Button
from .schema import ButtonOut, ButtonIn, ButtonFilters

router = APIRouter(tags=["Button"])


@router.post("/button", response_model=IdSchema)
async def create_button(data: ButtonIn):
    validate_fields = ["name", "code"]
    instance = await create(data, Button, validate_fields)
    return instance


@router.delete("/button/{button_id}", response_model=IdSchema)
async def delete_button(button_id: str):
    instance = await delete(button_id, Button)
    return instance


@router.put("/button/{button_id}", response_model=IdSchema)
async def update_button(button_id: str, data: ButtonIn):
    validate_fields = ["name", "code"]
    instance = await update(button_id, data, Button, validate_fields)
    return instance


@router.get("/button")
async def query_buttons(params: ButtonFilters = Depends()) -> FuPage[ButtonOut]:
    instance_list = await retrieve(Button, ButtonOut, filters=params)
    return instance_list


@router.get("/button/export/data")
async def export_button():
    export_fields = ["name", "code", "sort"]
    return await export_data(Button, ButtonOut, export_fields)
