from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page, Params
from fastapi_pagination.customization import (
    CustomizedPage,
    UseParams,
)

T = TypeVar("T")


class PaginationParams(Params):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(10, ge=1, le=100, alias="pageSize", description="Page size")


FuPage = CustomizedPage[
    Page[T],
    UseParams(PaginationParams)
]
