"""
Request工具类
"""

import json
from asyncio import sleep

import aiohttp
from user_agents import parse

import common
from common.fu_async_crud import create
from system.log_login.model import LogLogin


# import requests
# from django.conf import settings
# from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
# from django.urls.resolvers import ResolverMatch

# from common.fu_auth import get_user_by_token
# from system.models import LoginLog
# from user_agents import parse


# async def get_request_user(request):
#     user = await get_user_by_token(request)
#     return user


def get_request_ip(request):
    """
    获取请求IP
    :param request:
    :return:
    """
    ip = request.client.host
    return ip or "unknown"


def get_request_data(request):
    """
    获取请求参数
    :param request:
    :return:
    """
    request_data = getattr(request, "request_data", None)
    if request_data:
        return request_data
    data: dict = {**request.GET.dict(), **request.POST.dict()}
    if not data:
        try:
            body = request.body
            if body:
                data = json.loads(body)
        except Exception as e:
            pass
        if not isinstance(data, dict):
            data = {"data": data}
    return data


def get_request_path(request, *args, **kwargs):
    """
    获取请求路径
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    request_path = getattr(request, "request_path", None)
    if request_path:
        return request_path
    values = []
    for arg in args:
        if len(arg) == 0:
            continue
        if isinstance(arg, str):
            values.append(arg)
        elif isinstance(arg, (tuple, set, list)):
            values.extend(arg)
        elif isinstance(arg, dict):
            values.extend(arg.values())
    if len(values) == 0:
        return request.path
    path: str = request.path
    for value in values:
        path = path.replace("/" + value, "/" + "{id}")
    return path


def get_request_canonical_path(
    request,
):
    """
    获取请求路径
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    request_path = getattr(request, "request_canonical_path", None)
    if request_path:
        return request_path
    path: str = request.path
    resolver_match = request.resolver_match
    for value in resolver_match.args:
        path = path.replace(f"/{value}", "/{id}")
    for key, value in resolver_match.kwargs.items():
        if key == "pk":
            path = path.replace(f"/{value}", f"/{{id}}")
            continue
        path = path.replace(f"/{value}", f"/{{{key}}}")

    return path


def get_browser(
    request,
):
    """
    获取浏览器名
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    ua_string = request.headers.get("User-Agent", None)
    user_agent = parse(ua_string)
    return user_agent.get_browser()


def get_os(
    request,
):
    """
    获取操作系统
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    ua_string = request.headers.get("User-Agent", None)
    user_agent = parse(ua_string)
    return user_agent.get_os()


def get_verbose_name(queryset=None, view=None, model=None):
    """
    获取 verbose_name
    :param request:
    :param view:
    :return:
    """
    try:
        if queryset and hasattr(queryset, "model"):
            model = queryset.model
        elif view and hasattr(view.get_queryset(), "model"):
            model = view.get_queryset().model
        elif (
            view
            and hasattr(view.get_serializer(), "Meta")
            and hasattr(view.get_serializer().Meta, "model")
        ):
            model = view.get_serializer().Meta.model
        if model:
            return getattr(model, "_meta").verbose_name
        else:
            model = queryset.model._meta.verbose_name
    except Exception as e:
        pass
    return model if model else ""


async def get_ip_analysis(ip):
    """
    获取ip详细概略
    :param ip: ip地址
    :return:
    """
    data = {
        "continent": "",
        "country": "",
        "province": "",
        "city": "",
        "district": "",
        "isp": "",
        "area_code": "",
        "country_english": "",
        "country_code": "",
        "longitude": "",
        "latitude": "",
    }
    if ip != "unknown" and ip:
        if getattr(common, "ENABLE_LOGIN_LOG", True):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://ip.django-vue-admin.com/ip/analysis",
                    params={"ip": ip},
                ) as response:
                    res = response
                    # res = requests.get(
                    #     url="https://ip.django-vue-admin.com/ip/analysis",
                    #     params={"ip": ip},
                    #     verify=False,
                    # )

                    if res.status == 200:
                        res_data = await res.json()
                        if res_data.get("code") == 0:
                            data = res_data.get("data")
            return data
    return data


async def save_login_log(request, user):
    """
    保存登录日志
    :return:
    """
    ip = get_request_ip(request=request)
    analysis_data = await get_ip_analysis(ip)
    analysis_data["username"] = user.username
    analysis_data["ip"] = ip
    analysis_data["agent"] = str(parse(request.headers.get("User-Agent")))
    analysis_data["browser"] = get_browser(request)
    analysis_data["os"] = get_os(request)
    analysis_data["sys_creator_id"] = user.id
    await create(analysis_data, LogLogin)