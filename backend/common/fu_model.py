# -*- coding: utf-8 -*-
# @QQ      : 939589097
# @Time    : 2024/9/14 00:13
# @Author  : 臧成龙
# @Software: PyCharm
import uuid

from sqlalchemy import Column, Integer, DateTime, func, Boolean, String, ForeignKey, CHAR, TypeDecorator
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# 防止将UUID的字符串自动转为UUID类型
class UUIDStr(TypeDecorator):
    impl = String(36)

    def process_bind_param(self, value, dialect):
        # 在插入数据库时，将 Python 的 uuid.UUID 转换为字符串
        if isinstance(value, uuid.UUID):
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        # 在从数据库获取数据时，保留字符串类型，不转换为 uuid.UUID
        return value


class CoreModel(Base):
    __abstract__ = True  # 声明为抽象基类

    # 主键ID，使用UUID类型，默认值由uuid.uuid4生成
    id = Column(UUIDStr, primary_key=True, default=uuid.uuid4, comment="唯一标识符")

    # 创建者ID，使用UUID类型
    sys_creator_id = Column(
        ForeignKey("sys_user.id", ondelete="SET NULL"),
        comment="创建者ID",
    )

    # 修改者ID，使用UUID类型
    sys_modifier_id = Column(
        ForeignKey("sys_user.id", ondelete="SET NULL"),
        comment="最后修改者ID",
    )

    # 创建时间，使用DateTime类型，默认值为当前时间
    sys_create_datetime = Column(DateTime, default=func.now(), comment="创建时间")

    # 更新时间，使用DateTime类型，默认值为当前时间，更新时也会自动更新为当前时间
    sys_update_datetime = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="最后更新时间"
    )

    # 生效时间，使用DateTime类型，默认值为当前时间，更新时也会自动更新为当前时间
    sys_effect_datetime = Column(
        DateTime, default=func.now(), onupdate=func.now(), comment="生效时间"
    )

    # 失效时间，使用DateTime类型，默认值为None
    sys_expire_datetime = Column(DateTime, default=None, comment="失效时间")

    # 标记，使用Boolean类型，默认值为True
    sys_flag = Column(Boolean, default=True, comment="标记")

    # 排序，使用Integer类型，默认值为1
    sort = Column(Integer, default=1, comment="排序")

    # 把SQLAlchemy查询对象转换成字典
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


exclude_fields = (
    "id",
    "sys_creator",
    "sys_update_datetime",
    "sys_create_datetime",
    "sys_effect_datetime",
    "sys_expire_datetime",
    "sys_flag",
)


# 获取 User 模型中的多对多字段
def get_relation_fields(model):
    many_to_many_relations = {}
    one_to_many_relations = {}
    for field_name, rel in model.__mapper__.relationships.items():
        if rel.secondary is not None:
            many_to_many_relations[field_name] = rel.mapper.class_

        else:
            one_to_many_relations[field_name] = rel.mapper.class_
    return (
        many_to_many_relations,
        one_to_many_relations,
        {**many_to_many_relations, **one_to_many_relations},
    )