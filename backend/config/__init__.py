# dev, uat, prd
from sqlalchemy import URL
from pathlib import Path

ENV = "uat"

if ENV == "dev":
    from config.dev_env import *
if ENV == "uat":
    from config.uat_env import *
if ENV == "prd":
    from config.prd_env import *

# 项目的根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 放文件的目录
STATIC_URL = "static/"

# 是否开启登录日志
ENABLE_LOGIN_LOG = True

# jwt的相关配置
ACCESS_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

WHITE_LIST = [
    "/api/system/oauth2_login",
    "/api/system/login",
    "/api/system/logout",
    "/api/system/userinfo",
    "/api/system/permCode",
    "/api/system/menu/route/tree",
    "/api/system/user/*",
    "/api/system/user/set/repassword",
    "/api/system/sys_config",
]

# 数据库连接的配置
if DATABASE_TYPE == "POSTGRESQL":
    DRIVER_NAME = "postgresql+asyncpg"
elif DATABASE_TYPE == "MYSQL":
    DRIVER_NAME = "mysql+aiomysql"
else:
    DRIVER_NAME = "sqlite+aiosqlite"

DATABASE_URL = URL.create(
    drivername=DRIVER_NAME,
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME,
)