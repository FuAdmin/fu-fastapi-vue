from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class DictFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")
    code: str | None = Field(default=None, alias="code")


class DictBase(BaseModel):
    name: str
    code: str
    status: bool
    sort: int


class DictIn(DictBase):
    pass


class DictOut(DictBase, FuSchema):

    class Config:
        from_attributes = True
