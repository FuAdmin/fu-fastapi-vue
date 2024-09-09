/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/22 23:43
 * author: 臧成龙
 * JID: jzangc
 */
import { defHttp } from '@/utils/http/axios';

enum DeptApi {
  prefix = '/api/system/post',
}

export const getList = (params) => {
  return defHttp.get({ url: DeptApi.prefix, params });
};

export const getAllList = () => {
  return defHttp.get({ url: DeptApi.prefix + '/all/list' });
};

/**
 * 保存或更新
 */

export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    return defHttp.put({ url: DeptApi.prefix + '/' + params.id, params });
  } else {
    return defHttp.post({ url: DeptApi.prefix, params });
  }
};

export const importData = (params) => {
  return defHttp.post({ url: DeptApi.prefix + '/import/data', timeout: 20 * 60 * 1000, params });
};

export const exportData = () => {
  return defHttp.get(
    { url: DeptApi.prefix + '/export/data', timeout: 20 * 60 * 1000, responseType: 'blob' },
    { isReturnNativeResponse: true },
  );
};

/**
 * 删除
 */

export const deleteItem = (id) => {
  return defHttp.delete({ url: DeptApi.prefix + '/' + id });
};

/**
 * 删除
 */

export const deleteBatchItem = (params) => {
  return defHttp.delete({ url: DeptApi.prefix + '/batch/delete', params });
};
