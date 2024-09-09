/**
 * -*- coding: utf-8 -*-
 * time: 2024/4/01 22:54
 * author: 臧成龙
 * JID: jzangc
 */

import { BasicColumn, FormSchema } from '@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';
import { rules } from '@/utils/helper/validator';
import { getList } from '@/views/fuadmin/system/post/post.api';
import { getList as getRoleList } from '@/views/fuadmin/system/role/role.api';
import { useI18n } from '@/hooks/web/useI18n';

const { t } = useI18n();

export const columns: BasicColumn[] = [
  {
    title: 'id',
    dataIndex: 'id',
    resizable: true,
    width: 80,
  },
  {
    title: t('common.account.accountText'),
    dataIndex: 'username',
    resizable: true,
    width: 110,
  },
  {
    title: t('common.account.userNameText'),
    dataIndex: 'name',
    resizable: true,
    width: 150,
  },
  {
    title: t('common.account.avatarText'),
    dataIndex: 'avatar',
    resizable: true,
    width: 110,
  },
  {
    title: t('common.account.emailText'),
    dataIndex: 'email',
    resizable: true,
    width: 160,
  },
  {
    title: t('common.statusText'),
    dataIndex: 'is_active',
    resizable: true,
    width: 100,
    customRender: ({ record }) => {
      const status = record.is_active;
      const enable = ~~status === 1;
      const color = enable ? 'success' : 'error';
      const text = enable ? t('common.enableText') : t('common.disableText');
      return h(Tag, { color: color }, () => text);
    },
  },
  // {
  //   title: t('common.createDateText'),
  //   dataIndex: 'sys_create_datetime',
  //   width: 180,
  // },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'name',
    label: t('common.account.userNameText'),
    component: 'Input',
    colProps: { span: 6 },
  },
  {
    field: 'mobile',
    label: t('common.account.mobileText'),
    component: 'Input',
    colProps: { span: 6 },
  },
];

export const accountFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: 'id',
    component: 'Input',
    show: false,
  },
  {
    field: 'password',
    label: 'password',
    component: 'Input',
    show: false,
  },
  {
    field: 'username',
    label: t('common.account.accountText'),
    component: 'Input',
    required: true,
  },
  {
    field: 'name',
    label: t('common.account.userNameText'),
    component: 'Input',
    required: true,
  },

  {
    field: 'mobile',
    label: t('common.account.mobileText'),
    component: 'Input',
    rules: rules.rule('phone', false),
  },
  {
    field: 'email',
    label: t('common.account.emailText'),
    component: 'Input',
    rules: rules.rule('email', false),
  },
  {
    field: 'role',
    label: t('common.account.userRoleText'),
    component: 'TableSelect',
    componentProps: {
      fieldNames: {
        label: 'name',
        value: 'id',
      },
      api: getRoleList,
      columns: [
        {
          title: t('common.post.nameText'),
          dataIndex: 'name',
          width: 150,
        },
        {
          title: t('common.post.codeText'),
          dataIndex: 'code',
          width: 150,
        },
      ],
      searchFormSchema: [
        {
          field: 'name',
          label: t('common.post.nameText'),
          component: 'Input',
          colProps: { span: 8 },
        },
      ],
      mode: 'multiple',
    },
  },
  {
    field: 'post',
    label: t('common.account.userPostText'),
    component: 'TableSelect',
    componentProps: {
      fieldNames: {
        label: 'name',
        value: 'id',
      },
      api: getList,
      columns: [
        {
          title: t('common.post.nameText'),
          dataIndex: 'name',
          width: 150,
        },
        {
          title: t('common.post.codeText'),
          dataIndex: 'code',
          width: 150,
        },
      ],
      searchFormSchema: [
        {
          field: 'name',
          label: t('common.post.nameText'),
          component: 'Input',
          colProps: { span: 8 },
        },
      ],
      mode: 'multiple',
    },
  },
  {
    field: 'dept',
    label: t('common.account.userDeptText'),
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'name',
        value: 'id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'gender',
    label: t('common.account.genderText'),
    component: 'RadioButtonGroup',
    defaultValue: 1,
    componentProps: {
      options: [
        { label: t('common.account.maleText'), value: 1 },
        { label: t('common.account.femaleText'), value: 0 },
      ],
    },
  },
  {
    field: 'is_active',
    label: t('common.statusText'),
    component: 'RadioButtonGroup',
    defaultValue: true,
    componentProps: {
      options: [
        { label: t('common.enableText'), value: true },
        { label: t('common.disableText'), value: false },
      ],
    },
    required: true,
  },

  {
    field: 'avatar',
    label: t('common.account.avatarText'),
    slot: 'avatar',
  },
];
