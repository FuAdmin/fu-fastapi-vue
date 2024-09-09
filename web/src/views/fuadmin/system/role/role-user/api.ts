/**
 * -*- coding: utf-8 -*-
 * time: 2022/4/28 21:11
 * author: 臧成龙
 * JID: jzangc
 */
import { defHttp } from '/@/utils/http/axios';

enum DeptApi {
  prefix = '/api/system/role/users/by/role_id',
}

/**
 * 获取
 */

export const getList = (params) => {
  return defHttp.get({ url: DeptApi.prefix, params });
};

export const getUserListByRoleCode = (params) => {
  return defHttp.get({ url: DeptApi.prefix, params });
};

/**
 * 保存
 */

export const addUserToRole = (params) => {
  return defHttp.post({ url: DeptApi.prefix, params });
};

/**
 * 删除
 */

export const removeUserFromRole = (params) => {
  return defHttp.delete({ url: DeptApi.prefix, params });
};
