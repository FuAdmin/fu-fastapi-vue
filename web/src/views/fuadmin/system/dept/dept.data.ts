/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/3 22:12
 * author: 臧成龙
 * QQ: 939589097
 */
import { BasicColumn, FormSchema } from '@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';
import { useI18n } from '@/hooks/web/useI18n';

const { t } = useI18n();

export const columns: BasicColumn[] = [
  {
    title: t('common.dept.nameText'),
    dataIndex: 'name',
    width: 160,
    align: 'left',
  },
  {
    title: t('common.dept.phoneText'),
    dataIndex: 'phone',
    width: 180,
  },
  {
    title: t('common.dept.mailText'),
    dataIndex: 'email',
    width: 180,
  },
  {
    title: t('common.statusText'),
    dataIndex: 'status',
    width: 80,
    customRender: ({ record }) => {
      const status = record.status;
      const enable = ~~status === 1;
      const color = enable ? 'success' : 'error';
      const text = enable ? t('common.enableText') : t('common.disableText');
      return h(Tag, { color: color }, () => text);
    },
  },
  {
    title: t('common.createDateText'),
    dataIndex: 'sys_sys_create_datetime',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'name',
    label: t('common.dept.nameText'),
    component: 'Input',
    colProps: { span: 6 },
  },
];

export const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: 'id',
    component: 'Input',
    show: false,
  },
  {
    field: 'parent_id',
    label: t('common.dept.parentText'),
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'name',
        value: 'id',
      },
      getPopupContainer: () => document.body,
    },
  },

  {
    field: 'name',
    label: t('common.dept.nameText'),
    component: 'Input',
    required: true,
  },
  {
    field: 'phone',
    label: t('common.dept.phoneText'),
    component: 'Input',
  },
  {
    field: 'email',
    label: t('common.dept.mailText'),
    component: 'Input',
  },
  {
    field: 'status',
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
    field: 'sort',
    label: t('common.sortText'),
    defaultValue: 1,
    component: 'InputNumber',
    required: true,
  },
];
