### 1. 安装依赖包
```bash
pip install -r requirements.txt
````
### 2. 修改配置文件
在config目录下的`dev_env.py`中配置数据库信息
```python
# 数据库类型 MYSQL/SQLSERVER/SQLITE3/POSTGRESQL
DATABASE_TYPE = "MYSQL"
# 数据库地址
DATABASE_HOST = "127.0.0.1"
# 数据库端口
DATABASE_PORT = 3306
# 数据库用户名
DATABASE_USER = "fuadmin"
# 数据库密码
DATABASE_PASSWORD = "fuadmin"
# 数据库名
DATABASE_NAME = "fu-fastapi-vue"
```
### 3. 设置迁移环境
#### 3.1 在alembic下创建`versions`文件夹
#### 3.2 在根目录的alembic.ini文件里修改数据库的信息,跟`dev_env.py`保持一致
```python
# sqlalchemy.url = postgresql://fuadmin:fuadmin@127.0.0.1:5432/fu-admin-fast-api
sqlalchemy.url =  mysql://fuadmin:fuadmin@127.0.0.1:3306/fu-admin-fast-api
```




### 4.迁移数据库
#### 4.1 创建迁移脚本
```bash
alembic revision --autogenerate -m "initial migration"
```

#### 4.2 创建表
```bash
alembic upgrade head
```
#### 4.3 执行SQL脚本根据不同的数据库

---

### 其他关于alembic命令
回滚迁移
```bash
alembic downgrade -1
```

查看迁移历史
```bash
alembic history
```

删除迁移
```bash
alembic downgrade base
```
常用命令总结

```
alembic revision: 生成新的迁移脚本。
alembic upgrade: 升级数据库到指定版本。
alembic downgrade: 降级数据库到指定版本。
alembic heads: 显示当前可用的最新版本。
alembic branches: 显示分支点。
alembic current: 显示当前数据库版本
```