# Fu FastApi-Vue

[![img](https://img.shields.io/badge/license-Apache%202.0-dark)](https://gitee.com/fuadmin/fu-admin/blob/master/LICENSE) [![img](https://img.shields.io/badge/python-%3E=3.10.x-green.svg)](https://python.org/) [![PyPI - Django Version badge](https://img.shields.io/badge/FastApi-0.112.1-blue)](https://docs.djangoproject.com/zh-hans/4.0.4/) [![img](https://img.shields.io/badge/node-%3E%3D%2018.0.0-brightgreen)](https://nodejs.org/zh-cn/) [![img](https://gitee.com/fuadmin/fu-fastapi-vue/badge/star.svg?theme=dark)](https://gitee.com/fuadmin/fu-admin) [![GitHub stars](https://img.shields.io/github/stars/FuAdmin/fu-fastapi-vue.svg?theme=dark&label=Github)](https://github.com/FuAdmin/fu-fastapi-vue)

## 🔥 Fast Api版

- 官方文档：[http://124.222.210.96](http://124.222.210.96)(待完善)

- FastApi 专业版预览：[http://124.222.210.96:7070](http://124.222.210.96:7070)（需要授权）

- FastApi 开源版预览：[http://124.222.210.96:9090](http://124.222.210.96:9090)（免费开源）

## 🌟Django Ninja版

- Django 开源版预览：[http://124.222.210.96:8080](https://gitee.com/link?target=http%3A%2F%2F124.222.210.96%3A8080)（免费开源）
- Django Pro版预览：[http://124.222.210.96:6060](https://gitee.com/link?target=http%3A%2F%2F124.222.210.96%3A6060)（需要授权）



## 为什么使用 FastApi 和 Vue3

💡 **「FastApi」**

- **性能:** FastAPI 是一个现代的、快速（高性能）的 web 框架，基于 Python 3.7+ 的类型提示。非常高的性能，接近于 NodeJS 或 Go 语言编写的 API，并且比传统的 Python 框架如 Flask 或 Django 更快。

- **易用性:** 它易于学习和使用，提供了简洁的语法结构，使得开发者能够快速地构建API。

- **内置的数据验证:** FastAPI 自动从请求中解析和验证数据，这减少了手动处理这些任务的需求。

- **文档:** FastAPI 自动生成 API 文档（使用如 OpenAPI 和 JSON Schema），这使得开发者和用户可以轻松地了解如何使用 API。

- **异步编程支持:** FastAPI 支持异步请求处理，这在处理 I/O 密集型任务时非常有用，比如数据库查询或文件读取。


💡 **「Vue3 」**

- **最火的框架：**国内最火的前端框架之一。
- **性能提升：**运行速度是 vue2 的 1.5 倍。
- **体积更小：**按需编译体积 vue2 要更小。
- **类型推断：**更好的支持 ts 这个也是趋势。
- **高级给予：**暴露了更底层的 API 和提供更先进的内置组件。
- **组合 API：**能够更好的组织逻辑，封装逻辑，复用逻辑

## 平台简介

- 🧑‍🤝‍🧑 前端采用[VbenAdmin](https://vvbin.cn/doc-next) 、[Vue3](https://cn.vuejs.org/)、[Ant Design Vue](https://www.antdv.com/docs/vue/getting-started-cn)。
- 👭 后端采用 Python 语言和强大的[FastAPI](https://fastapi.tiangolo.com/zh/)。
- 👬 支持加载动态权限菜单，多方式轻松权限控制。
- 💡 Django 项目移步[FuAdmin](https://gitee.com/fuadmin/fu-admin)
- 💏 特别鸣谢：[VbenAdmin](https://github.com/vbenjs/vue-vben-admin) 、[Ant Design Vue](https://github.com/vueComponent/ant-design-vue)、[GoView](https://mtruning.club/)
- 💡 特别感谢[jetbrains](https://www.jetbrains.com/) 为本开源项目提供免费的 IntelliJ IDEA 授权。


## 交流

- Fu FastAdmin-Vue 交流群：
- QQ群: 2153011070

## 源码地址

|        | 项目地址                                                     |
| ------ | ------------------------------------------------------------ |
| github | [FuAdmin/fu-fastapi-vue (github.com)](https://github.com/FuAdmin/fu-fastapi-vue) |
| 码云   | https://gitee.com/fuadmin/fu-admin                           |

## 内置功能

1. 👨‍⚕️ 菜单管理：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。
2. 🧑‍⚕️ 部门管理：配置系统组织机构（公司、部门、角色）。
3. 👩‍⚕️ 角色管理：角色菜单权限分配、数据权限分配、设置角色按部门进行数据范围权限划分。
4. 🧑‍🎓 权限权限：授权角色的权限范围。
5. 👨‍🎓 用户管理：用户是系统操作者，该功能主要完成系统用户配置。
6. 🧑‍🔧 数据字典：对系统中经常使用的一些较为固定的数据进行维护。
7. 🧑‍🔧 分类字典：对系统中经常使用的一些树形数据进行维护。
8. 📁 附件管理：对平台上所有文件、图片等进行统一管理。
9. 🗓️ 操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。

## 准备工作

```
Python >= 3.10.0 (推荐3.10+版本)
nodejs >= 18.0 (推荐最新)
Mysql >= 8.0 (可选，默认数据库sqlite3，推荐8.0版本)
```

## 前端 ♝

必须使用pnpm，项目提供了`pnpm-lock.yaml`，使用其他包管理器，容易出现版本依赖问题。

```bash
# 进入项目目录
cd fu-fastapi-vue/web

# 安装依赖
pnpm install --registry=https://registry.npmmirror.com

# 启动服务
pnpm dev
# 浏览器访问 https://localhost:8080
# .env 文件中可配置启动端口等参数
# 构建生产环境
# pnpm build
```

## 后端 💈

```bash
1. 安装依赖包
pip install -r requirements.txt

2. 修改配置文件
在config目录下的dev_env.py中配置数据库信息

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

3 在根目录的alembic.ini文件里修改数据库的信息,跟dev_env.py保持一致
# sqlalchemy.url = postgresql://fuadmin:fuadmin@127.0.0.1:5432/fu-admin-fast-api
sqlalchemy.url =  mysql://fuadmin:fuadmin@127.0.0.1:3306/fu-admin-fast-api

4 创建迁移脚本
alembic revision --autogenerate -m "initial migration"

5 创建表
alembic upgrade head

6 执行SQL脚本根据不同的数据库
```

### 访问项目

- 文档访问地址：[https://localhost:3000/api/docs](https://localhost:8080/api/docs) (默认为此地址，如有修改请按照配置文件)
- 账号：`superadmin` 密码：`123456`

## 演示图 ✅



## Docker构建

请参考文档[Docker构建](docker/README.md)

