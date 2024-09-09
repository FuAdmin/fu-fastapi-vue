import uuid
from datetime import datetime

import psycopg2

from common.utils.dabase.type_mapping import PostgresQueryType, PostgresCreateType
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT


class FuPostgres:
    def __init__(self, dbname=DATABASE_NAME):
        self.conn = psycopg2.connect(
            dbname=DATABASE_NAME if dbname is None else dbname,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()

    # 可选: 使用上下文管理器
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_all_schemas(self):
        # 创建游标
        # 查询所有 schema
        query = """
            SELECT schema_name, schema_owner
            FROM information_schema.schemata;
        """

        # 执行查询
        self.cursor.execute(query)

        # 获取查询结果
        schemas = self.cursor.fetchall()

        # 将结果转换为字典列表
        schema_dicts = [
            {"schema_name": schema[0], "schema_owner": schema[1]}
            for schema in schemas if schema[0] not in ('information_schema', 'pg_catalog', 'pg_toast')
        ]

        return schema_dicts

    def get_all_tables(self, schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        # 查询所有表
        query = f"""
            SELECT table_name, table_schema
            FROM information_schema.tables
            WHERE table_schema = '{schema_name}';
        """

        # 执行查询
        self.cursor.execute(query)

        # 获取查询结果
        tables = self.cursor.fetchall()

        # 将结果转换为字典列表
        table_dicts = [
            {"table_name": table[0], "table_schema": table[1]}
            for table in tables
        ]

        return table_dicts

    def get_all_db(self):
        # 查询所有表
        query = f"""
            SELECT datname
            FROM pg_database where datistemplate = false;
        """

        # 执行查询
        self.cursor.execute(query)

        # 获取查询结果
        dbs = self.cursor.fetchall()

        # 将结果转换为字典列表
        db_dicts = [
            {"db_name": db[0]}
            for db in dbs if db[0] != 'postgres'
        ]

        return db_dicts

    def get_table_structure(self, table_name, schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        # 查询表结构
        query = f"""
            SELECT 
                column_name, 
                data_type, 
                is_nullable, 
                character_maximum_length,
                table_schema,
                table_name
            FROM 
                information_schema.columns
            WHERE 
                table_name = '{table_name}' AND 
                table_schema = '{schema_name}'
            ORDER BY 
                ordinal_position;
        """

        # 查询主键约束
        primary_key_query = f"""
                SELECT 
                    kcu.column_name
                FROM 
                    information_schema.table_constraints AS tc
                JOIN 
                    information_schema.key_column_usage AS kcu
                ON 
                    tc.constraint_name = kcu.constraint_name
                WHERE 
                    tc.constraint_type = 'PRIMARY KEY' AND
                    tc.table_name = '{table_name}' AND 
                    tc.table_schema = '{schema_name}'
                ORDER BY 
                    kcu.ordinal_position;
            """

        # 执行查询
        self.cursor.execute(query)
        # 获取查询结果
        columns = self.cursor.fetchall()

        # 查询主键约束
        self.cursor.execute(primary_key_query)
        primary_keys = self.cursor.fetchall()

        # 将结果转换为字典列表
        column_dicts = [
            {
                "column_name": col[0],
                "data_type": col[1],
                "is_nullable": col[2],
                "max_length": col[3],
                "table_schema": col[4],
                "table_name": col[5]
            }
            for col in columns
        ]
        # 添加其他信息
        for col_dict in column_dicts:
            col_dict["is_primary_key"] = col_dict["column_name"] in [pk[0] for pk in primary_keys]
            col_dict["is_nullable"] = col_dict["is_nullable"] == 'YES'
            col_dict["data_type"] = PostgresQueryType.get(col_dict["data_type"])

        return column_dicts

    def add_new_column(self, table_name, column_name, data_type, is_nullable, max_length,
                       schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        sql = f"""
        ALTER TABLE {schema_name}.{table_name} 
        ADD {column_name} {PostgresCreateType.get(data_type)}{'(' + str(max_length) + ')' if data_type == 'varchar' else ''} {'NOT NULL' if not is_nullable else ''}
        """

        # 执行SQL
        self.cursor.execute(sql)

    def update_column(self, table_name, column_name, data_type, is_nullable, max_length,
                      schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        if column_name == 'id':
            return
        sql = f"""
        ALTER TABLE {schema_name}.{table_name} 
        ALTER COLUMN {column_name} TYPE {PostgresCreateType.get(data_type)}{'(' + str(max_length) + ')' if data_type == 'varchar' else ''}
        """
        # 执行SQL
        self.cursor.execute(sql)

        if not is_nullable:
            sql = f"""
            ALTER TABLE {schema_name}.{table_name}
            ALTER COLUMN {column_name} SET NOT NULL
            """
            self.cursor.execute(sql)
        else:
            sql = f"""
            ALTER TABLE {schema_name}.{table_name}
            ALTER COLUMN {column_name} DROP NOT NULL
            """
            self.cursor.execute(sql)

    def delete_column(self, table_name, column_name, schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        sql = f"""
        ALTER TABLE {schema_name}.{table_name} 
        DROP COLUMN {column_name}
        """
        self.cursor.execute(sql)

    def preview_data(self, table_name, schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        sql = f"""
        SELECT * FROM {schema_name}.{table_name} LIMIT 20
        """
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        # 整理成列表字典
        data_list = [dict(zip([col[0] for col in self.cursor.description], row)) for row in data]
        return data_list

    def create_table(self, table_name, table_structure, schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name

        # 构建 SQL 语句
        # 构建 SQL 语句
        columns = ['id VARCHAR(36) PRIMARY KEY', 'sys_create_datetime TIMESTAMP NOT NULL', 'sys_update_datetime TIMESTAMP NOT NULL']
        for column in table_structure:
            col_def = f"{column['column_name']} {column['data_type']}"
            if column['data_type'] == 'varchar':
                col_def += f"({column['max_length']})"
            if column['is_nullable']:
                col_def += " NULL"
            else:
                col_def += " NOT NULL"
            if 'constraint' in column:
                col_def += f" {column['constraint']}"
            if 'default' in column:
                col_def += f" DEFAULT {column['default']}"
            columns.append(col_def)
        columns_str = ',\n'.join(columns)
        sql = f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                    {columns_str}
                );
                """
        self.cursor.execute(sql)

    def insert_data(self, table_name, data, schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        data = [data] if isinstance(data, dict) else data
        keys = data[0].keys()
        for item in data:
            if set(item.keys()) != set(keys):
                raise ValueError("All dictionaries must have the same keys.")

        # 构建 SQL 语句
        columns = ', '.join(keys)
        placeholders = ', '.join(['%s'] * (len(keys) + 3))  # 加上三个额外的占位符
        query = f"""
            INSERT INTO {schema_name}.{table_name} (id, sys_create_datetime, sys_update_datetime, {columns}) 
            VALUES ({placeholders});
        """

        # 准备数据
        values_list = [
            (str(uuid.uuid4()), datetime.now(), datetime.now(), *tuple(item.values()))
            for item in data
        ]

        # 执行 SQL 语句
        self.cursor.executemany(query, values_list)

    def select_data(self, table_name, condition=None, limit=None, offset=None,
                    is_like=True, order_by=(('sys_update_datetime',), 'DESC'), schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name

        # 构建 SQL 语句
        query = f"SELECT * FROM {schema_name}.{table_name}"
        count_query = f"SELECT COUNT(*) FROM {schema_name}.{table_name}"
        params = []

        if condition:
            # 将字典转换为 SQL WHERE 子句
            where_clause_parts = []
            for key, value in condition.items():
                if value is None or value == '':
                    continue
                if isinstance(value, str) and is_like:
                    where_clause_parts.append(f"{key} LIKE %s")
                    params.append(f"%{value}%")  # 添加模糊查询的百分号
                else:
                    where_clause_parts.append(f"{key} = %s")
                    params.append(value)
            if where_clause_parts:
                where_clause = ' AND '.join(where_clause_parts)
                query += f" WHERE {where_clause}"
        query += " ORDER BY " + ", ".join(order_by[0]) + " " + order_by[1]

        if limit:
            query += f" LIMIT {limit}"

        if limit:
            query += f" OFFSET {offset}"

        cur = self.cursor

        # 执行 SQL 语句
        cur.execute(count_query)
        count = cur.fetchone()[0]

        # 执行 SQL 语句
        cur.execute(query, params)
        columns = [desc[0] for desc in cur.description]
        # 获取结果并转换为字典
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        return rows, count

    def update_data(self, table_name, data, condition, is_like=False, schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        # 构建 SQL 语句
        data.pop('id', None)
        data.pop('sys_create_datetime', None)
        data.pop('key', None)
        data['sys_update_datetime'] = datetime.now()

        set_clause = ', '.join([f"{k} = %s" for k in data])
        query = f"UPDATE {schema_name}.{table_name} SET {set_clause}"
        # 将字典转换为 SQL WHERE 子句
        params = []
        where_clause_parts = []
        for key, value in condition.items():
            if value is None or value == '':
                continue
            if isinstance(value, str) and is_like:
                where_clause_parts.append(f"{key} LIKE %s")
                params.append(f"%{value}%")  # 添加模糊查询的百分号
            else:
                where_clause_parts.append(f"{key} = %s")
                params.append(value)
        if where_clause_parts:
            where_clause = ' AND '.join(where_clause_parts)
            query += f" WHERE {where_clause}"

        params = [*list(data.values()), *params]
        # 执行 SQL 语句
        self.cursor.execute(query, params)

    def delete_data(self, table_name, condition, is_like=False, schema_name='public'):
        schema_name = 'public' if schema_name is None else schema_name
        # 构建 SQL 语句
        query = f"DELETE FROM {schema_name}.{table_name}"
        # 将字典转换为 SQL WHERE 子句
        params = []
        where_clause_parts = []
        for key, value in condition.items():
            if value is None or value == '':
                continue
            if isinstance(value, str) and is_like:
                where_clause_parts.append(f"{key} LIKE %s")
                params.append(f"%{value}%")  # 添加模糊查询的百分号
            else:
                where_clause_parts.append(f"{key} = %s")
            params.append(value)
        if where_clause_parts:
            where_clause = ' AND '.join(where_clause_parts)
            query += f" WHERE {where_clause}"
        # 执行 SQL 语句
        self.cursor.execute(query, params)
