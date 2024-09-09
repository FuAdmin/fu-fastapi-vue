from fastapi import Depends, APIRouter, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_async_sqlalchemy import db
from sqlalchemy import select

from common.fu_async_crud import retrieve
from common.fu_auth import authenticate_user, get_user_by_token, generate_token
from common.fu_schema import response_success
from common.utils.request_util import save_login_log
from system.button.model import Button
from system.button.schema import ButtonOut
from system.login.schema import LoginOut, LoginIn, UserInfoOut
from system.role.model import role_button_association

router = APIRouter(tags=["Login"])


@router.post("/login", response_model=LoginOut)
async def login(request: Request, background_tasks: BackgroundTasks, data: LoginIn):
    instance = await authenticate_user(data.username, data.password)
    background_tasks.add_task(save_login_log, request, instance)
    return instance


@router.post("/oauth2_login", response_model=LoginOut)
async def oauth2_login(form_data: OAuth2PasswordRequestForm = Depends()):
    instance = await authenticate_user(form_data.username, form_data.password)
    return instance


@router.get("/logout", response_model=dict)
async def logout(request: Request):
    return response_success()


@router.get("/userinfo", response_model=UserInfoOut)
async def userinfo(request: Request):
    user = await get_user_by_token(request)
    return user


@router.get("/permCode", response_model=list[str])
async def permission_code(request: Request):
    user = await get_user_by_token(request, relations_fields_obj=True)
    if not user.is_superuser:
        role_ids = [item.id for item in user.role]
        result = await db.session.execute(
            select(role_button_association.c.button_id).where(
                role_button_association.c.role_id.in_(role_ids)
            )
        )
        button_ids = result.scalars().all()

        button_result = await db.session.execute(
            select(Button).where(Button.id.in_(button_ids))
        )
        buttons = button_result.scalars().all()
    else:
        buttons = await retrieve(Button, ButtonOut, is_pagination=False)
    button_codes = [button.code for button in buttons]
    return button_codes