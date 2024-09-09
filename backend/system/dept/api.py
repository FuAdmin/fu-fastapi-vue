from fastapi import APIRouter, Depends
from common.fu_async_crud import create, delete, update, retrieve
from common.fu_schema import IdSchema

from common.utils.list_to_tree import list_to_tree
from .model import Dept
from .schema import DeptFilters, DeptOut, DeptIn

router = APIRouter(tags=["Dept"])


@router.post("/dept", response_model=IdSchema)
async def create_dept(data: DeptIn):
    instance = await create(data, Dept)
    return instance


@router.delete("/dept/{dept_id}", response_model=IdSchema)
async def delete_dept(dept_id: str):
    instance = await delete(dept_id, Dept)
    return instance


@router.put("/dept/{dept_id}", response_model=IdSchema)
async def update_dept(dept_id: str, data: DeptIn):
    instance = await update(dept_id, data, Dept)
    return instance


@router.get("/dept/list/tree", response_model=list[dict])
async def list_dept_tree(params: DeptFilters = Depends()):
    instance_list = await retrieve(Dept, DeptOut, is_pagination=False, filters=params)
    dept_list = [item.dict() for item in instance_list]
    # 将查询集转换成树形结构
    dept_tree = list_to_tree(dept_list)
    return dept_tree
