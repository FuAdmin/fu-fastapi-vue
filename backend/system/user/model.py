from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Text,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from common.fu_model import CoreModel, Base, UUIDStr

user_role_association = Table(
    "sys_user_role",
    Base.metadata,
    Column("user_id", ForeignKey("sys_user.id")),
    Column("role_id", ForeignKey("sys_role.id")),
)

user_post_association = Table(
    "sys_user_post",
    Base.metadata,
    Column("user_id", ForeignKey("sys_user.id")),
    Column("post_id", ForeignKey("sys_post.id")),
)


class User(CoreModel):
    __tablename__ = "sys_user"

    username = Column(String(255), unique=True, index=True, comment="User Account")
    is_superuser = Column(Boolean, default=False, comment="Is Super User")
    email = Column(String(255), unique=True, index=True, comment="User Email")
    mobile = Column(String(11), unique=True, index=True, comment="User Mobile")
    avatar = Column(Text, comment="User Avatar")
    name = Column(String(255), comment="User Name")
    gender = Column(Integer, default=1, comment="User Gender")
    password = Column(String(255), comment="User Password")
    dept_id = Column(UUIDStr, nullable=True, comment="User Department")

    role = relationship("Role", secondary=user_role_association, back_populates="user")

    post = relationship("Post", secondary=user_post_association, back_populates="user")