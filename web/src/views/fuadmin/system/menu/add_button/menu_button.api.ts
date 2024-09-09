/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/13 21:31
 * author: 臧成龙
 * JID: jzangc
 */
import { defHttp } from '@/utils/http/axios';

enum DeptApi {
  prefix = '/api/system/button',
}

/**
 * 获取
 */

export const getList = (params) => {
  return defHttp.get({ url: DeptApi.prefix, params });
};

/**
 * 获取
 */

export const getAllList = () => {
  return defHttp.get({ url: DeptApi.prefix + '/get/all'});
};

/**
 * 保存或更新
 */

export const createOrUpdate = (params, isUpdate = false) => {
  if (isUpdate) {
    return defHttp.put({ url: DeptApi.prefix + '/' + params.id, params });
  } else {
    return defHttp.post({ url: DeptApi.prefix, params });
  }
};

/**
 * 删除
 */

export const deleteItem = (id) => {
  return defHttp.delete({ url: DeptApi.prefix + '/' + id });
};
