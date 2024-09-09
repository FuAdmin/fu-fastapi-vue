import uuid
from datetime import datetime

import MySQLdb

from common.utils.dabase.type_mapping import PostgresQueryType, PostgresCreateType, MySqlQueryType, MySqlCreateType
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT


class FuMySQL:
    def __init__(self, dbname=DATABASE_NAME):
        self.conn = MySQLdb.connect(
            db=DATABASE_NAME if dbname is None else dbname,
            user=DATABASE_USER,
            passwd=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        self.cursor = self.conn.cursor()

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()

    # 使用上下文管理器
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_all_tables(self):
        # 查询所有表
        query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{DATABASE_NAME}'
        """

        # 执行查询
        self.cursor.execute(query)

        # 获取查询结果
        tables = self.cursor.fetchall()

        # 将结果转换为字典列表
        table_dicts = [
            {"table_name": table[0]}
            for table in tables
        ]

        return table_dicts

    def get_all_db(self):
        # 查询所有数据库
        query = "SHOW DATABASES;"

        # 执行查询
        self.cursor.execute(query)

        # 获取查询结果
        dbs = self.cursor.fetchall()

        # 将结果转换为字典列表
        db_dicts = [
            {"db_name": db[0]}
            for db in dbs
        ]

        return db_dicts

    def get_table_structure(self, table_name):
        # 查询表结构
        query_columns = f"""
            SELECT 
                COLUMN_NAME, 
                DATA_TYPE, 
                IS_NULLABLE, 
                COLUMN_DEFAULT, 
                CHARACTER_MAXIMUM_LENGTH
            FROM 
                INFORMATION_SCHEMA.COLUMNS
            WHERE 
                TABLE_NAME = %s
                AND TABLE_SCHEMA = %s;
        """

        # 查询主键
        query_primary_key = f"""
            SELECT 
                COLUMN_NAME
            FROM 
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE 
                TABLE_NAME = %s
                AND TABLE_SCHEMA = %s
                AND CONSTRAINT_NAME = 'PRIMARY';
        """

        # 执行查询
        self.cursor.execute(query_columns, (table_name, DATABASE_NAME))
        columns = self.cursor.fetchall()

        # 获取主键
        self.cursor.execute(query_primary_key, (table_name, DATABASE_NAME))
        primary_keys = [row[0] for row in self.cursor.fetchall()]

        # 将结果转换为字典列表，并加入主键信息
        column_dicts = [
            {
                "column_name": col[0],
                "data_type": col[1],
                "is_nullable": col[2],
                "default_value": col[3],
                "max_length": col[4],
                "is_primary_key": col[0] in primary_keys
            }
            for col in columns
        ]

        for col_dict in column_dicts:
            col_dict["is_primary_key"] = col_dict["column_name"] in primary_keys
            col_dict["is_nullable"] = col_dict["is_nullable"] == 'YES'
            col_dict["data_type"] = MySqlQueryType.get(col_dict["data_type"])

        return column_dicts

    def add_new_column(self, table_name, column_name, data_type, is_nullable, max_length):
        sql = f"""
        ALTER TABLE `{DATABASE_NAME}`.{table_name} 
        ADD {column_name} {MySqlCreateType.get(data_type)}{'(' + str(max_length) + ')' if data_type == 'varchar' else ''} {'NOT NULL' if not is_nullable else 'NULL'}
        """

        # 执行SQL
        self.cursor.execute(sql)

    def update_column(self, table_name, column_name, data_type, is_nullable, max_length):
        if column_name == 'id':
            return
        sql = f"""
        ALTER TABLE `{DATABASE_NAME}`.{table_name} 
        MODIFY COLUMN {column_name} {MySqlCreateType.get(data_type)}{'(' + str(max_length) + ')' if data_type == 'varchar' else ''} {'NOT NULL' if not is_nullable else 'NULL'}
        """
        # 执行SQL
        self.cursor.execute(sql)

    def delete_column(self, table_name, column_name):
        sql = f"""
        ALTER TABLE `{DATABASE_NAME}`.{table_name} 
        DROP COLUMN {column_name}
        """
        self.cursor.execute(sql)

    def preview_data(self, table_name):
        sql = f"""
        SELECT * FROM `{DATABASE_NAME}`.{table_name} LIMIT 20
        """
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        # 整理成列表字典
        data_list = [dict(zip([col[0] for col in self.cursor.description], row)) for row in data]
        return data_list

    def create_table(self, table_name, table_structure):
        # 构建 SQL 语句
        columns = ['id VARCHAR(36) PRIMARY KEY', 'sys_create_datetime DATETIME NOT NULL',
                   'sys_update_datetime DATETIME NOT NULL']
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
        sql = f"""CREATE TABLE IF NOT EXISTS `{DATABASE_NAME}`.{table_name} (
                    {columns_str}
                );"""
        self.cursor.execute(sql)

    def insert_data(self, table_name, data):
        data = [data] if isinstance(data, dict) else data
        keys = data[0].keys()
        for item in data:
            if set(item.keys()) != set(keys):
                raise ValueError("All dictionaries must have the same keys.")

        # 构建 SQL 语句
        columns = ', '.join(keys)
        placeholders = ', '.join(['%s'] * (len(keys) + 3))  # 加上三个额外的占位符
        query = f"""
            INSERT INTO `{DATABASE_NAME}`.{table_name} (id, sys_create_datetime, sys_update_datetime, {columns}) 
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
                    is_like=True, order_by=(('sys_update_datetime',), 'DESC')):

        # 构建 SQL 语句
        query = f"SELECT * FROM `{DATABASE_NAME}`.{table_name}"
        count_query = f"SELECT COUNT(*) FROM `{DATABASE_NAME}`.{table_name}"
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

    def update_data(self, table_name, data, condition, is_like=False):
        # 构建 SQL 语句
        data.pop('id', None)
        data.pop('sys_create_datetime', None)
        data.pop('key', None)
        data['sys_update_datetime'] = datetime.now()

        set_clause = ', '.join([f"{k} = %s" for k in data])
        query = f"UPDATE `{DATABASE_NAME}`.{table_name} SET {set_clause}"
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

    def delete_data(self, table_name, condition, is_like=False):
        # 构建 SQL 语句
        query = f"DELETE FROM `{DATABASE_NAME}`.{table_name}"
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
