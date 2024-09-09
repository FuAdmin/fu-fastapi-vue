
PostgresQueryType = {
    'character varying': 'varchar',
    'character': 'char',
    'text': 'text',
    'integer': 'int',
    'bigint': 'bigint',
    'smallint': 'smallint',
    'numeric': 'numeric',
    'real': 'real',
    'double precision': 'double',
    'boolean': 'bool',
    'timestamp with time zone': 'datetime',
    'date': 'date',
    'json': 'json',
    'bit': 'bit',
    'float': 'float',
    'decimal': 'decimal',
}
PostgresCreateType = {
    'varchar': 'VARCHAR',
    'char': 'CHAR',
    'text': 'TEXT',
    'int': 'INTEGER',
    'bigint': 'BIGINT',
    'smallint': 'SMALLINT',
    'numeric': 'NUMERIC',
    'real': 'REAL',
    'float': 'FLOAT',
    'double': 'DOUBLE PRECISION',
    'bool': 'BOOLEAN',
    'datetime': 'TIMESTAMP WITH TIME ZONE',
}

MySqlQueryType = {
    'varchar': 'varchar',
    'char': 'char',
    'longtext': 'text',
    'json': 'json',
    'int': 'int',
    'bigint': 'bigint',
    'smallint': 'smallint',
    'numeric': 'numeric',
    'double': 'double',
    'datetime': 'datetime',
    'date': 'date',
    'tinyint': 'bool'
}

MySqlCreateType = {
    'varchar': 'varchar',
    'char': 'char',
    'text': 'longtext',
    'json': 'json',
    'int': 'int',
    'bigint': 'bigint',
    'smallint': 'smallint',
    'numeric': 'numeric',
    'double': 'double',
    'datetime': 'datetime',
    'date': 'date',
    'bool': 'tinyint'
}
