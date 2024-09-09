from typing import List

from fastapi import Depends, APIRouter
from fastapi_async_sqlalchemy import db
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from common.fu_async_crud import (
    create,
    delete,
    update,
    retrieve,
    export_data,
    get_instance_by_id,
)

from common.fu_pagination import FuPage
from common.fu_schema import ImportSchema, IdSchema, response_success
from .model import Role
from .schema import RoleOut, RoleIn, RoleFilters, UserRoleIn, RoleUserOut, RoleUserIn
from ..menu.model import Menu
from ..menu.schema import MenuOut
from ..user.model import User

router = APIRouter(tags=["Role"])


@router.post("/role", response_model=IdSchema)
async def create_role(data: RoleIn):
    validate_fields = ["name", "code"]
    instance = await create(data, Role, validate_fields)
    return instance


@router.delete("/role/{role_id}", response_model=IdSchema)
async def delete_role(role_id: str):
    instance = await delete(role_id, Role)
    return instance


@router.put("/role/{role_id}", response_model=IdSchema)
async def update_role(role_id: str, data: RoleIn):
    validate_fields = ["name", "code"]
    instance = await update(role_id, data, Role, validate_fields)
    return instance


@router.get("/role")
async def query_roles(params: RoleFilters = Depends()) -> FuPage[RoleOut]:
    instance_list = await retrieve(Role, RoleOut, filters=params)
    return instance_list


@router.get("/role/list/button")
async def list_menu_button_tree():
    menus = await retrieve(
        Menu, MenuOut, is_pagination=False, relations_fields_obj=True
    )
    result = []
    for item in menus:
        dict_item = item.dict()
        menu_button = [button_item.to_dict() for button_item in item.button]

        for button_item in menu_button:
            button_id_str = str(button_item["id"])
            button_item["id"] = f"b#{button_id_str}"
            button_item["parent_id"] = button_item.pop("menu_id")
            button_item["title"] = button_item.pop("name")

        result.extend(menu_button)
        result.append(dict_item)
    return get_button_or_column_or_entity_menu(result, "b#")


@router.get("/role/users/by/role_id", response_model=List[RoleUserOut])
async def get_users_by_role(params: UserRoleIn = Depends()):
    result = await db.session.execute(
        select(Role).options(selectinload(Role.user)).filter(Role.id == params.role_id),
    )
    role = result.scalar_one_or_none()
    users = role.user
    return users


@router.post("/role/users/by/role_id", response_model=IdSchema)
async def add_user_to_role(data: RoleUserIn):
    user_ids = data.user_ids
    instance = await update(data.role_id, {"user": user_ids}, Role)
    return instance


@router.delete("/role/users/by/role_id")
async def delete_user_in_role(data: RoleUserIn):
    user = await get_instance_by_id(data.user_id, User)
    role = await get_instance_by_id(data.role_id, Role)
    role.user.remove(user)
    await db.session.commit()
    return response_success()


def get_button_or_column_or_entity_menu(data, flag):
    return_data = []
    for i in data:
        m_id = i["id"]
        if flag in str(m_id):
            return_data.append(i)
            get_menu_by_parent(i["parent_id"], data, return_data)
    return return_data


def get_menu_by_parent(parent_id, data, return_data):
    for i in data:
        if parent_id == i["id"] and i not in return_data:
            return_data.append(i)
            get_menu_by_parent(i["parent_id"], data, return_data)
    if parent_id is None:
        return
