from pydantic import BaseModel, Field

from common.fu_schema import FuSchema, FuFilters


class RoleFilters(FuFilters):
    name__like: str | None = Field(default=None, alias="name")
    code: str | None = Field(default=None, alias="code")


class RoleBase(BaseModel):
    name: str
    code: str
    status: bool = Field(default=True)
    menu: list | None = Field(default=None)
    button: list | None = Field(default=None)


class RoleIn(RoleBase):
    pass


class RoleOut(RoleBase, FuSchema):

    class Config:
        from_attributes = True


class UserRoleIn(FuFilters):
    role_id: str = Field(default=None, alias="role_id")


class RoleUserOut(BaseModel):
    name: str | None = Field(default=None, alias="name")
    id: str
    username: str | None
    avatar: str | None = Field(default=None, alias="avatar")
    email: str | None = Field(default=None, alias="email")


class RoleUserIn(BaseModel):
    role_id: str | None
    user_ids: list | None = []
    user_id: str | None = None