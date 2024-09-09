from typing import Any, Dict, List, Optional, Type
from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from pydantic import BaseModel
from sqlalchemy import select, and_
from fastapi.responses import FileResponse
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from common.fu_model import CoreModel, get_relation_fields
from common.fu_schema import FuFilters
from common.utils.excel_utils import dict_to_excel


def query_filter(
        filters: Dict[str, Any],
        query: Any,
        model: Type[CoreModel],
) -> Any:
    """
    应用基于提供的过滤器字典对SQLAlchemy查询进行过滤。

    :param filters: 过滤条件字典，键为字段名或带有操作符的字段名，值为过滤值。
    :param query: 要应用过滤器的SQLAlchemy查询对象。
    :param model: SQLAlchemy模型类。
    :return: 过滤后的查询对象。
    """
    if len(filters) == 0:
        return query
    for key, value in filters.items():
        if "__" not in key:
            query = query.filter(getattr(model, key) == value)
        else:
            # 解析过滤条件
            field, op = key.split("__")

            # 获取字段属性
            field_attr = getattr(model, field)

            # 根据操作符构建过滤条件
            if op == "like":
                query = query.filter(field_attr.like("%" + value + "%"))
            elif op == "eq":
                query = query.filter(field_attr == value)
            elif op == "ne":
                query = query.filter(field_attr != value)
            elif op == "in":
                query = query.filter(field_attr.in_(value))
            elif op == "not_in":
                query = query.filter(~field_attr.in_(value))
            elif op == "is_null":
                query = query.filter(field_attr.is_(None))
            elif op == "is_not_null":
                query = query.filter(field_attr.isnot(None))
            elif op == "is_empty":
                query = query.filter(field_attr == "")
            elif op == "is_not_empty":
                query = query.filter(field_attr != "")
            elif op == "startswith":
                query = query.filter(field_attr.startswith(value))
    return query


# 定义一个异步函数create，用于在数据库中创建新记录
async def create(
        data: dict | BaseModel,  # 输入数据，可以是字典或Pydantic模型
        model: Type[CoreModel],  # 指定的SQLAlchemy模型类
        validate_fields: Optional[List[str]] = None,  # 需要验证的字段列表（可选）
        session: Optional[AsyncSession] = None,  # 数据库会话对象（可选）
) -> Any:
    """
    在数据库中创建新记录。

    :param data: 包含用于创建新记录的数据的字典 或 Pydantic对象。
    :param model: SQLAlchemy模型类。
    :param validate_fields: 可选的，在创建记录之前验证的字段列表, 列如[{"post", Post}]。
    :param session: 数据库会话对象， 默认为空时使用全局对象
    :return: 创建的实例。
    """
    if session is None:
        session = db.session
    # 如果输入数据 `data` 不是字典类型，则将其转换为字典
    if not isinstance(data, dict):
        data = data.dict(exclude_none=True)
    # 如果未提供 `validate_fields`，则默认为空列表
    if validate_fields is None:
        validate_fields = []
    # 验证指定字段的数据
    await validate_by_field(validate_fields, data, model, session=session)
    # 获取模型类中的relation字段
    many_to_many_relations, _, relations = get_relation_fields(model)
    # 如果存在多对多关系
    if many_to_many_relations is not None:
        # 移除多对多字段以避免直接在主模型中创建时引发错误
        remove_many_to_many_fields = {
            key: item
            for key, item in data.items()
            if key not in many_to_many_relations.keys()
        }
        # 使用剩余数据创建模型实例
        instance = model(**remove_many_to_many_fields)
        # 处理多对多关系
        for key, many_model in many_to_many_relations.items():
            if key in data:
                # 获取多对多字段的值
                many_to_many_field_values = data.pop(key)
                # 查询多对多关系中的相关记录
                result = await session.execute(
                    select(many_model).filter(
                        many_model.id.in_(many_to_many_field_values)
                    )
                )
                # 获取查询结果
                many_model_list = result.scalars().all()
                # 设置多对多关系
                setattr(instance, key, many_model_list)
        # 将实例添加到数据库会话
        session.add(instance)
    else:
        # 使用数据创建模型实例
        instance = model(**data)
        # 将实例添加到数据库会话
        session.add(instance)
    # 提交会话，使数据持久化
    await session.commit()
    # 刷新实例以确保获取最新的数据
    await session.refresh(instance)

    # 返回创建的实例
    return instance


async def batch_create(
        data_list: List[dict] | List[BaseModel],  # 输入数据，可以是字典或Pydantic模型
        model: Type[CoreModel],  # 指定的SQLAlchemy模型类
        session: Optional[AsyncSession] = None,  # 数据库会话对象（可选）
) -> Any:
    """
    在数据库中批量创建新记录。

    :param data_list: List包含用于创建新记录的数据的字典 或 Pydantic对象。
    :param model: SQLAlchemy模型类。
    :param session: 数据库会话对象， 默认为空时使用全局对象
    :return: 创建的实例。
    """
    if session is None:
        session = db.session
    instance_list = []
    for data in data_list:
        # 如果输入数据 `data` 不是字典类型，则将其转换为字典
        if not isinstance(data, dict):
            data = data.dict(exclude_none=True)

        # 使用数据创建模型实例
        instance = model(**data)
        instance_list.append(instance)
    # 将实例添加到数据库会话
    session.add_all(instance_list)
    # 提交会话，使数据持久化
    await session.commit()
    return len(instance_list)


async def delete(
        del_id: str,
        model: Type[CoreModel],
) -> Any:
    """
    通过ID从数据库中删除记录。

    :param del_id: 要删除的记录的ID。
    :param model: SQLAlchemy模型类。
    :return: 删除的实例。
    """
    result = await db.session.execute(select(model).filter(model.id == del_id))
    instance = result.scalar_one_or_none()
    if instance is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.session.delete(instance)
    await db.session.commit()
    return instance


async def update(
        update_id: str,
        data: dict | BaseModel,
        model: Type[CoreModel],
        validate_fields: Optional[List[str]] = None,
) -> Any:
    """
    更新数据库中的现有记录。

    :param update_id: 要更新的记录的ID。
    :param data: 包含更新数据的字典 或 pydantic对象。
    :param model: SQLAlchemy模型类。
    :param validate_fields: 可选的，在更新记录之前验证的字段列表。
    :return: 更新的实例。
    """
    # 将data转换为字典，以便于后续操作
    if not isinstance(data, dict):
        data = data.dict(exclude_none=True)

    # 获取模型类中的relation字段
    many_to_many_relations, _, relations = get_relation_fields(model)
    relation_fields = list(relations.keys())
    selection = [selectinload(getattr(model, field)) for field in relation_fields]

    # 查询要更新的实例
    result = await db.session.execute(
        select(model).options(*selection).filter(model.id == update_id)
    )
    instance = result.scalar_one_or_none()

    # 如果实例不存在，则抛出404错误
    if instance is None:
        raise HTTPException(status_code=404, detail="Instance not found")

    # 如果未提供验证字段，则默认为空列表
    if validate_fields is None:
        validate_fields = []

    # 验证要更新的字段
    await validate_by_field(validate_fields, data, model, update_id)

    if many_to_many_relations is not None:
        # 移除多对多字段以避免直接在主模型中创建时引发错误
        remove_many_to_many_fields = {
            key: item
            for key, item in data.items()
            if key not in many_to_many_relations.keys()
        }
        # 处理多对多关系
        for key, many_model in many_to_many_relations.items():
            if key in data:
                # 获取多对多字段的值
                many_to_many_field_values = data.pop(key)
                # 查询多对多关系中的相关记录
                result = await db.session.execute(
                    select(many_model).filter(
                        many_model.id.in_(many_to_many_field_values)
                    )
                )
                # 获取查询结果
                many_model_list = result.scalars().all()
                # 设置多对多关系
                setattr(instance, key, many_model_list)

        # 更新实例的属性值
        for attr, value in remove_many_to_many_fields.items():
            setattr(instance, attr, value)
    else:
        # 更新实例的属性值
        for attr, value in data.items():
            setattr(instance, attr, value)

    # 提交数据库会话以保存更新
    await db.session.commit()

    await db.session.refresh(instance, relation_fields)

    # 返回更新后的实例
    return instance


# 定义一个异步函数retrieve，用于从数据库中检索记录，支持可选的分页和过滤器功能
async def retrieve(
        model: Type[CoreModel],
        out_schema: Type[BaseModel],
        order_by: str = "-sys_update_datetime",
        is_pagination: bool = True,
        filters: FuFilters = FuFilters(),
        relations_fields_obj: bool = False,
) -> List[Any]:
    """
    从数据库中检索记录，可以根据需求选择性地应用分页和过滤器。

    :param model: SQLAlchemy 模型类，用于指定要查询的数据表。
    :param out_schema: Pydantic 模型类，用于序列化输出结果。
    :param order_by: 字符串形式的排序字段名，默认为 '-sys_update_datetime' 表示按 'sys_update_datetime' 降序排列。
    :param is_pagination: 布尔值，指示是否启用分页功能，默认为 True。
    :param filters: 过滤条件对象，默认为 FuFilters 类的一个实例。
    :param relations_fields_obj: 关联字段类型，False返回为ID，True为对象
    :return: 如果启用了分页，则返回分页后的查询结果；否则返回所有查询到的记录。
    """

    # 将过滤器对象转换为字典形式，并排除键值对中的 None 值
    filters_dict = filters.dict(exclude_none=True)

    # 获取模型类中的relation字段
    _, _, relations = get_relation_fields(model)
    relation_fields = list(relations.keys())
    # 根据是否需要分页来决定如何执行查询
    if is_pagination:
        # 判断排序方式（升序/降序），并根据分页需求执行查询
        if order_by[0] == "-":  # 如果排序字段名以 '-' 开头，则进行降序排序
            order_by = order_by[1:]  # 去掉 '-' 符号
            # 使用 paginate 函数执行分页查询，并按指定字段降序排列
            instance_list = await paginate(
                db.session,
                query_filter(  # 应用过滤条件
                    filters_dict, select(model), model  # 构建查询语句
                ).order_by(
                    getattr(model, order_by).desc()  # 指定降序排序
                ),
            )
        else:  # 否则进行升序排序
            # 使用 paginate 函数执行分页查询，并按指定字段升序排列
            instance_list = await paginate(
                db.session,
                query_filter(  # 应用过滤条件
                    filters_dict, select(model), model  # 构建查询语句
                ).order_by(
                    getattr(model, order_by).asc()  # 指定升序排序
                ),
            )

        # 遍历查询结果，处理多对多字段
        if not relations_fields_obj:
            for item in instance_list.items:
                for field in relation_fields:
                    if hasattr(item, field):
                        setattr(
                            item,
                            field,
                            [many_model.id for many_model in getattr(item, field)],
                        )
    else:  # 如果不需要分页，则直接查询所有记录
        # 构建查询语句，加载多对多字段
        selection = [selectinload(getattr(model, field)) for field in relation_fields]
        instance = select(model).options(*selection)

        # 根据排序方式执行查询
        if order_by[0] == "-":  # 降序排序
            order_by = order_by[1:]
            instance_list = query_filter(  # 应用过滤条件
                filters_dict, instance, model
            ).order_by(
                getattr(model, order_by).desc()  # 指定降序排序
            )
        else:  # 升序排序
            instance_list = query_filter(  # 应用过滤条件
                filters_dict, instance, model
            ).order_by(
                getattr(model, order_by).asc()  # 指定升序排序
            )

        # 执行查询并获取所有记录
        result = await db.session.execute(instance_list)
        instance_list = result.scalars().all()

        # 处理多对多字段，并将 ORM 对象转换为 Pydantic 模型
        convert_list = []
        for item in instance_list:
            # 转换为 Pydantic 模型
            item = out_schema.from_orm(item)
            if not relations_fields_obj:
                for field in relation_fields:
                    if hasattr(item, field):
                        setattr(
                            item,
                            field,
                            [many_model.id for many_model in getattr(item, field)],
                        )
            convert_list.append(item)
        instance_list = convert_list

    # 返回最终查询结果
    return instance_list


async def get_instance_by_id(query_id, model, is_query_relation: bool = True):
    query = select(model).filter(model.id == query_id)
    if is_query_relation:
        _, _, relations = get_relation_fields(model)
        relation_fields = list(relations.keys())
        selection = [selectinload(getattr(model, field)) for field in relation_fields]
        query = query.options(*selection)
    result = await db.session.execute(query)
    instance = result.scalar_one_or_none()
    # 如果实例不存在，则抛出404错误
    if instance is None:
        raise HTTPException(status_code=404, detail="Instance not found")

    return instance


async def get_instance_by_field(query: tuple, model):
    _, _, relations = get_relation_fields(model)
    relation_fields = list(relations.keys())
    selection = [selectinload(getattr(model, field)) for field in relation_fields]
    result = await db.session.execute(
        select(model).options(*selection).filter(getattr(model, query[0]) == query[1])
    )
    instance_list = result.scalars().all()
    return instance_list


async def export_data(model, scheme, export_fields) -> FileResponse:
    """
    导出数据为Excel文件。

    参数:
    - request: HttpRequest对象，表示客户端请求。
    - model: Django模型类，指定要导出数据的模型。
    - scheme: 表示数据转换规则的对象，用于将ORM对象转换为字典。
    - export_fields: 包含要导出的字段名的列表。

    返回值:
    - FileResponse对象，提供下载Excel文件。
    """

    title_dict = {}
    # 根据export_fields列表获取字段的显示名称
    for field in export_fields:
        comment = getattr(model, field).comment
        title_dict[field] = comment

    instance = await retrieve(model, scheme, is_pagination=False)
    list_data = []
    # 将查询集中的每一项转换为指定格式的字典
    for qs_item in instance:
        qs_item = scheme.from_orm(qs_item)
        dict_data = {}
        for item, value in title_dict.items():
            dict_data[value] = getattr(qs_item, item)
        list_data.append(dict_data)

    file_url = dict_to_excel(list_data)
    # 返回供下载的文件响应
    return FileResponse(file_url)


async def validate_by_field(
        fields: List[str],
        data: Dict[str, Any],
        model: Type[CoreModel],
        update_id: Optional[str] = None,
        session: Optional[AsyncSession] = None,
) -> None:
    """
    验证某些字段在数据库已经存在。

    :param db: SQLAlchemy会话。用于执行数据库查询。
    :param fields: 要验证的字段列表。这些字段的值需要在数据库中是唯一的。
    :param data: 包含要验证的数据的字典。字典的键应与fields列表中的字段名相对应。
    :param model: SQLAlchemy模型类。表示数据库中的一个表，用于查询。
    :param update_id: 可选的，排除于验证之外的ID（用于更新）。如果提供，该ID对应的记录将不会被包含在冲突检查中。
    :return: None。该函数不返回任何内容，但如果发现冲突，则会引发异常。
    """
    if session is None:
        session = db.session
    # 遍历需要验证的字段列表
    for item in fields:
        # 从模型类中获取相应的字段
        field = getattr(model, item)
        # 从数据字典中获取该字段的值
        value = data.get(item)
        # 如果有提供ID，查询时排除该ID对应的记录
        if update_id is None:
            result = await session.execute(select(model).filter(field == value))
            instance = result.scalar_one_or_none()
        else:
            result = await session.execute(
                select(model).filter(and_(field == value, model.id != update_id))
            )
            instance = result.scalar_one_or_none()
        # 如果查询到了记录（即值冲突），抛出HTTP异常
        if instance is not None:
            raise HTTPException(
                status_code=422, detail=f"{item} '{value}' already existed"
            )