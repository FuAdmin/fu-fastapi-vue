/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/25 22:12
 * author: 臧成龙
 * QQ: 939589097
 */
import { defHttp } from '@/utils/http/axios';

enum Api {
  prefix = '/api/system/role',
}

/**
 * 获取
 */

export const getList = (params) => {
  return defHttp.get({ url: Api.prefix, params });
};

export const getAllList = () => {
  return defHttp.get({ url: Api.prefix + '/all/list' });
};

/**
 * 获取菜单和按钮list
 */

// export const getMenuList = () => {
//   return defHttp.get({ url: Api.prefix + '/list/menu' });
// };

export const getMenuButtonList = () => {
  return defHttp.get({ url: Api.prefix + '/list/button' });
};

export const getMenuColumnList = () => {
  return defHttp.get({ url: Api.prefix + '/list/menu_column' });
};

export const getButtonByMenuId = (menu_id) => {
  return defHttp.get({ url: Api.prefix + '/list/button/' + menu_id });
};

/**
 * 保存或更新
 */

export const createOrUpdate = (params, isUpdate) => {
  if (isUpdate) {
    return defHttp.put({ url: Api.prefix + '/' + params.id, params });
  } else {
    return defHttp.post({ url: Api.prefix, params });
  }
};

/**
 * 删除
 */

export const deleteItem = (id) => {
  return defHttp.delete({ url: Api.prefix + '/' + id });
};

/**
 * 根据角色查询树信息
 */
export const queryTreeListForRole = () => defHttp.get({ url: Api.prefix });
/**
 * 查询角色权限
 */
export const queryRolePermission = (params) => defHttp.get({ url: Api.prefix, params });
/**
 * 保存角色权限
 */
export const saveRolePermission = (params) => defHttp.post({ url: Api.prefix, params });
/**
 * 查询角色数据规则
 */
export const queryDataRule = (params) =>
  defHttp.get(
    { url: `${Api.prefix}/${params.functionId}/${params.roleId}` },
    { isTransformResponse: false },
  );
/**
 * 保存角色数据规则
 */
export const saveDataRule = (params) => defHttp.post({ url: Api.prefix, params });
