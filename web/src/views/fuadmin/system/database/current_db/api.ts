/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/22 23:43
 * author: 臧成龙
 * JID: jzangc
 */
import { defHttp } from '@/utils/http/axios';

enum DeptApi {
  prefix = '/api/database/',
}

export const getDBList = (params?: any) => {
  return defHttp.get({ url: DeptApi.prefix + 'db', params });
};

export const getSchemaList = (params?: any) => {
  return defHttp.get({ url: DeptApi.prefix + 'schema', params });
};

export const getTableList = (params?: any) => {
  return defHttp.get({ url: DeptApi.prefix + 'table', params });
};

export const getTableStructure = (params?: any) => {
  return defHttp.get({ url: DeptApi.prefix + 'structure', params });
};

export const saveTableStructure = (params) => {
  return defHttp.post({ url: DeptApi.prefix + 'structure/save', params });
};

export const createTable = (params) => {
  return defHttp.post({ url: DeptApi.prefix + 'create/table', params });
};

export const deleteItem = (id) => {
  return defHttp.delete({ url: DeptApi.prefix + '/' + id });
};

export const previewTableData = (params?: any) => {
  return defHttp.get({ url: DeptApi.prefix + 'preview/data', params });
};
