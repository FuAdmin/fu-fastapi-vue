from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class DeptFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")


class DeptBase(BaseModel):
    name: str
    owner: str | None = None
    phone: str | None = None
    email: str | None = None
    status: bool = True
    parent_id: str | None = None


class DeptIn(DeptBase):
    pass


class DeptOut(DeptBase, FuSchema):

    class Config:
        from_attributes = True