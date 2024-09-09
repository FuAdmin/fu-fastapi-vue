from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from common.fu_model import CoreModel
from system.role.model import role_button_association


class Button(CoreModel):
    __tablename__ = "sys_button"

    name = Column(String(64), unique=True, comment="岗位名称")
    code = Column(String(64), unique=True, comment="岗位代码")
    api = Column(String(200), comment="接口地址")
    method = Column(Integer, comment="请求方式")
    menu_id = Column(ForeignKey("sys_menu.id", ondelete="SET NULL"), comment="菜单ID")

    # 定义多对一关系
    menu = relationship("Menu", back_populates="button")

    # 定义多对多关系
    role = relationship(
        "Role",
        secondary=role_button_association,
        back_populates="button",
    )