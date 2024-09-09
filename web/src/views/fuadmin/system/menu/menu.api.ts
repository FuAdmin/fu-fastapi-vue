/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/15 22:12
 * author: 臧成龙
 * JID: jzangc
 */
import { defHttp } from '@/utils/http/axios';
import { getMenuListResultModel } from '@/api/sys/model/menuModel';

enum MenuApi {
  prefix = '/api/system/menu',
  GetMenuList = '/api/system/menu',
  GetMenuRoute = '/api/system/menu/route/tree',
}

/**
 * 获取菜单
 */

export const getMenuList = (params={}) => {
  return defHttp.get({ url: MenuApi.GetMenuList, params });
};

export const getMenuRoute = () => {
  return defHttp.get<getMenuListResultModel>({ url: MenuApi.GetMenuRoute });
};

/**
 * 根据Parent Id获取菜单
 */

export const getMenuListByParent = (params) => {
  return defHttp.get({ url: MenuApi.GetMenuList + '/by/parent_id/' + params.parent_id });
};

/**
 * 保存或更新
 */

export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    return defHttp.put({ url: MenuApi.prefix + '/' + params.id, params });
  } else {
    console.log(params);
    return defHttp.post({ url: MenuApi.prefix, params });
  }
};

/**
 * 删除
 */

export const deleteItem = (id) => {
  return defHttp.delete({ url: MenuApi.prefix + '/' + id });
};
