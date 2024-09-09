#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 9/23/2024 10:51 PM
# author: 臧成龙
# QQ: 939589097
import os
from datetime import datetime

from fastapi import Depends, APIRouter, UploadFile, Form
from starlette.responses import FileResponse

from common.fu_async_crud import (
    create,
    delete,
    update,
    retrieve,
    export_data,
    get_instance_by_id,
)

from common.fu_pagination import FuPage
from common.fu_schema import ImportSchema, IdSchema
from config import STATIC_URL, BASE_DIR
from .model import File
from .schema import FileOut, FileIn, FileFilters, UploadFileIn

router = APIRouter(tags=["File"])


@router.delete("/file/{file_id}", response_model=IdSchema)
async def delete_file(file_id: str):
    instance = await delete(file_id, File)
    return instance


@router.put("/file/{file_id}", response_model=IdSchema)
async def update_file(file_id: str, data: FileIn):
    instance = await update(file_id, data, File)
    return instance


@router.get("/file")
async def query_files(params: FileFilters = Depends()) -> FuPage[FileOut]:
    instance_list = await retrieve(File, FileOut, filters=params)
    return instance_list


@router.post("/upload", response_model=FileOut)
async def upload(file: UploadFile, folder: str | None = Form(default="")):
    binary_data = file.file.read()
    current_date = datetime.now().strftime("%Y%m%d%H%M%S%f")
    current_ymd = datetime.now().strftime("%Y%m%d")
    file_name = current_date + "_" + file.filename
    return await local_save(binary_data, folder, current_ymd, file, file_name)


@router.post("/download")
async def download(data: FileIn):
    file_path = str(BASE_DIR) + "/" + data.url
    return FileResponse(file_path)


@router.get("/file/get/{file_id}")
async def get_file(file_id: str):
    file_instance = await get_instance_by_id(file_id, File)
    file_path = str(BASE_DIR) + "/" + file_instance.url
    return FileResponse(file_path)


@router.get("/image/{image_id}")
async def get_image(image_id: str):
    file_instance = await get_instance_by_id(image_id, File)
    file_path = str(BASE_DIR) + "/" + file_instance.url
    return FileResponse(file_path, media_type="image/png")


async def local_save(binary_data, folder, current_ymd, file, file_name):
    file_path = os.path.join(str(BASE_DIR), STATIC_URL, folder, current_ymd)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_url = os.path.join(str(file_path), file_name)
    with open(file_url, "wb") as f:
        f.write(binary_data)
    data = {
        "file_name": file.filename,
        "size": file.size,
        "save_name": file_name,
        "url": os.path.join(STATIC_URL, folder, current_ymd, file_name),
    }
    instance = await create(data, File)
    return instance
