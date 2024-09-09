/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/11 22:12
 * author: 臧成龙
 * QQ: 939589097
 */
import { BasicColumn, FormSchema } from '@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';
import { useI18n } from '@/hooks/web/useI18n';

const { t } = useI18n();

const methodOptions = [
  { label: 'GET', value: 0 },
  { label: 'POST', value: 1 },
  { label: 'PUT', value: 2 },
  { label: 'DELETE', value: 3 },
];

export const columns: BasicColumn[] = [
  {
    title: t('common.button.nameText'),
    dataIndex: 'name',
    width: 50,
    align: 'left',
    resizable: true,
  },
  {
    title: t('common.button.codeText'),
    dataIndex: 'code',
    width: 70,
    align: 'left',
    resizable: true,
  },
  {
    title: t('common.button.methodText'),
    dataIndex: 'method',
    width: 50,
    align: 'left',
    resizable: true,
    customRender: ({ record }) => {
      const method = record.method;
      let color = '';
      let text = '';
      switch (method) {
        case 0:
          color = 'processing';
          text = 'GET';
          break;
        case 1:
          color = 'success';
          text = 'POST';
          break;
        case 2:
          color = 'warning';
          text = 'PUT';
          break;
        case 3:
          color = 'error';
          text = 'DELETE';
          break;
      }
      return h(Tag, { color: color }, () => text);
    },
  },
  {
    title: t('common.button.apiText'),
    dataIndex: 'api',
    width: 100,
    align: 'left',
    resizable: true,
  },
  {
    title: t('common.createDateText'),
    dataIndex: 'sys_create_datetime',
    width: 120,
    ifShow: false,
  },
  {
    title: t('common.remarkText'),
    dataIndex: 'sys_remark',
    ifShow: false,
  },
];

// @ts-ignore
// @ts-ignore
export const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: 'id',
    component: 'Input',
    show: false,
  },
  {
    field: 'name',
    label: t('common.button.nameText'),
    component: 'Input',
    required: true,
  },
  {
    field: 'code',
    label: t('common.button.codeText'),
    required: true,
    component: 'Input',
    show: true,
  },

  {
    field: 'method',
    label: t('common.button.methodText'),
    component: 'Select',
    componentProps: {
      options: methodOptions,
    },
    required: true,
  },

  {
    field: 'api',
    label: t('common.button.apiText'),
    required: true,
    component: 'Input',
  },
  {
    field: 'sort',
    label: t('common.sortText'),
    component: 'InputNumber',
    defaultValue: 1,
    required: true,
  },
  {
    label: t('common.remarkText'),
    field: 'sys_remark',
    component: 'InputTextArea',
  },
];
