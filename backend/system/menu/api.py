from fastapi import APIRouter, Depends, Request
from fastapi_async_sqlalchemy import db
from sqlalchemy import select
from common.fu_async_crud import create, delete, update, retrieve
from common.fu_auth import get_user_by_token
from common.fu_schema import IdSchema
from common.utils.list_to_tree import list_to_tree, list_to_route
from .model import Menu
from .schema import MenuFilters, MenuOut, MenuIn
from ..role.model import role_menu_association

router = APIRouter(tags=["Menu"])


@router.post("/menu", response_model=IdSchema)
async def create_menu(data: MenuIn):
    instance = await create(data, Menu)
    return instance


@router.delete("/menu/{menu_id}", response_model=IdSchema)
async def delete_menu(menu_id: str):
    instance = await delete(menu_id, Menu)
    return instance


@router.put("/menu/{menu_id}", response_model=IdSchema)
async def update_menu(menu_id: str, data: MenuIn):
    instance = await update(menu_id, data, Menu)
    return instance


@router.get("/menu", response_model=list[dict])
async def list_menu_tree(params: MenuFilters = Depends()):
    instance_list = await retrieve(Menu, MenuOut, "sort", False, filters=params)
    menu_list = [item.dict() for item in instance_list]
    # 将查询集转换成树形结构
    menu_tree = list_to_tree(menu_list)
    return menu_tree


@router.get("/menu/route/tree", response_model=list[dict])
async def route_menu_tree(request: Request):
    user = await get_user_by_token(request, relations_fields_obj=True)

    result = await db.session.execute(
        select(Menu).filter(Menu.status == True).order_by(Menu.sort)
    )
    instance_list = result.scalars().all()

    if not user.is_superuser:
        role_ids = [item.id for item in user.role]
        role_menu_result = await db.session.execute(
            select(role_menu_association.c.menu_id).where(
                role_menu_association.c.role_id.in_(role_ids)
            )
        )
        menu_ids = role_menu_result.scalars().all()
        instance_list = [item for item in instance_list if item.id in menu_ids]

    menu_list = [item.to_dict() for item in instance_list]
    menu_tree = list_to_route(menu_list)
    return menu_tree
