from fastapi import APIRouter
from .user.api import router as user_router
from .menu.api import router as menu_router
from .login.api import router as login_router
from .post.api import router as post_router
from .dept.api import router as dept_router
from .role.api import router as role_router
from .button.api import router as button_router
from .dict.api import router as dict_router
from .dict_item.api import router as dict_item_router
from .file.api import router as file_router
from .log_login.api import router as log_login_router
from .log_operation.api import router as log_operation_router
from .monitor.api import router as monitor_router


system_router = APIRouter(prefix="/system")

system_router.include_router(user_router)
system_router.include_router(menu_router)
system_router.include_router(login_router)
system_router.include_router(post_router)
system_router.include_router(dept_router)
system_router.include_router(role_router)
system_router.include_router(button_router)
system_router.include_router(dict_router)
system_router.include_router(dict_item_router)
system_router.include_router(file_router)
system_router.include_router(log_login_router)
system_router.include_router(log_operation_router)
system_router.include_router(monitor_router)