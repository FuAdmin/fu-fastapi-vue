from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class ButtonFilters(FuFilters):
    menu_id: str | None = Field(default=None, alias="menu_id")


class ButtonBase(BaseModel):
    name: str = Field(default=None, alias="name")
    code: str = Field(default=None, alias="code")
    sort: int = Field(default=None, alias="sort")
    method: int | None = Field(default=None, alias="method")
    api: str | None = Field(default=None, alias="api")
    menu_id: str | None = Field(default=None, alias="menu_id")


class ButtonIn(ButtonBase):
    pass


class ButtonOut(ButtonBase, FuSchema):

    class Config:
        from_attributes = True