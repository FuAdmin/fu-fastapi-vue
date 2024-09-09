from fastapi import FastAPI, Depends
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_pagination import add_pagination
from starlette.middleware.authentication import AuthenticationMiddleware

from common.fu_auth import FuOAuth2PasswordBearer
from common.fu_middleware import LogOperationMiddleware, JWTAuthBackend
from config import DATABASE_URL
from system.router import system_router


my_oauth2_scheme = FuOAuth2PasswordBearer(tokenUrl="api/system/oauth2_login")

app = FastAPI(dependencies=[Depends(my_oauth2_scheme)])

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=DATABASE_URL,
    engine_args={  # engine arguments example
        "echo": True,  # print all SQL statements
        "pool_pre_ping": True,  # feature will normally emit SQL equivalent to “SELECT 1” each time a connection is checked out from the pool
        "pool_size": 100,  # number of connections to keep open at a time
        "max_overflow": 300,  # number of connections to allow to be opened above pool_size
        "pool_recycle": 3600,
    },
)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
app.add_middleware(LogOperationMiddleware)
add_pagination(app)


app.include_router(prefix="/api", router=system_router)