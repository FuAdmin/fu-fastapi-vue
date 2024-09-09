import re
from calendar import timegm
from datetime import datetime, timedelta
from typing import Union, Optional

from fastapi import FastAPI, HTTPException, status, Request
from fastapi_async_sqlalchemy import db
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import selectinload

from common.fu_model import get_relation_fields
from config import (
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ACCESS_SECRET_KEY,
    WHITE_LIST,
    IS_DEMO,
)
from system.button.model import Button
from system.login.schema import LoginOut, UserInfoOut
from system.role.model import role_button_association
from system.user.model import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def set_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    result = await db.session.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()
    login_status = True
    if user is None:
        login_status = False
    else:
        if not verify_password(password, user.password):
            login_status = False
    if not login_status:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await generate_token(user)


async def generate_token(user):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user = UserInfoOut(username=user.username, id=user.id, name=user.name)
    access_token = await create_token(
        data=user.dict(),
        secret_key=ACCESS_SECRET_KEY,
        expires_delta=access_token_expires,
    )
    expire_time = timegm((datetime.utcnow() + access_token_expires).utctimetuple())
    return LoginOut(
        id=user.id,
        token=access_token,
        access_token=access_token,
        username=user.username,
        name=user.name,
        expireTime=expire_time,
    )


async def create_token(
    data: dict, secret_key: str, expires_delta: Union[timedelta, None] = None
):
    to_encode = data.copy()
    to_encode["id"] = str(to_encode["id"])
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_by_token(
    request: Request,
    data=None,
    relations_fields_obj: bool = False,
):
    payload = await decode_token(request, data)
    query = select(User).filter(User.id == payload["id"])
    if relations_fields_obj:
        _, _, relations = get_relation_fields(User)
        relation_fields = list(relations.keys())
        selection = [selectinload(getattr(User, field)) for field in relation_fields]
        query = query.options(*selection)
    result = await db.session.execute(query)
    user = result.scalar_one_or_none()

    return user


async def decode_token(request, data=None) -> dict:
    try:

        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        secret_key = ACCESS_SECRET_KEY

        payload = jwt.decode(
            token, secret_key, algorithms=[ALGORITHM], options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            401, "Time Out, Please Login"
        )  # 如果抛出过期异常，则Token已过期
    except jwt.JWTError:
        raise HTTPException(
            401, "Invalid Tokens"
        )  # 其他无效Token的情况，包括但不限于过期


METHOD = {
    "GET": 0,
    "POST": 1,
    "PUT": 2,
    "DELETE": 3,
}


class FuOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str):
        super().__init__(
            tokenUrl=tokenUrl,
            scheme_name=None,
            scopes=None,
            description=None,
            auto_error=True,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        path: str = request.get("path")
        if path in WHITE_LIST:
            return None
        authorization: str = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        else:

            user = await get_user_by_token(
                request, data=None, relations_fields_obj=True
            )
            method = request.get("method")
            if IS_DEMO and method != "GET":
                raise HTTPException(403, "演示环境")
            if not user.is_superuser:
                # 正则表达式，捕获UUID前的字符串和UUID本身
                pattern = r"(.*?)([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})"
                # 使用lambda函数来构建新的字符串，保留前缀并替换UUID为:id
                path_with_placeholder = re.sub(
                    pattern, lambda m: m.group(1) + ":id", path
                )
                if path in WHITE_LIST:
                    return token
                else:
                    role_ids = [item.id for item in user.role]
                    result = await db.session.execute(
                        select(role_button_association.c.button_id).where(
                            role_button_association.c.role_id.in_(role_ids)
                        )
                    )
                    button_ids = result.scalars().all()

                    result = await db.session.execute(
                        select(Button).filter(
                            Button.id.in_(button_ids),
                            Button.api == path_with_placeholder,
                            Button.method == METHOD[method],
                        )
                    )
                    result = result.scalar_one_or_none()
                    if result is not None:
                        return token
                    else:
                        raise HTTPException(403, "No Permission")
            else:
                return token