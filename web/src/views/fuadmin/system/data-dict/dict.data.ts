/**
 * -*- coding: utf-8 -*-
 * time: 2024/4/29 01:37
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
    title: t('common.dict.nameText'),
    dataIndex: 'name',
    width: 200,
    resizable: true,
  },
  {
    title: t('common.dict.codeText'),
    dataIndex: 'code',
    width: 180,
    resizable: true,
  },
  {
    title: t('common.sortText'),
    dataIndex: 'sort',
    width: 100,
    resizable: true,
  },
  {
    title: t('common.statusText'),
    dataIndex: 'status',
    width: 100,
    customRender: ({ record }) => {
      const status = record.status;
      const enable = ~~status === 1;
      const color = enable ? 'success' : 'error';
      const text = enable ? t('common.enableText') : t('common.disableText');
      return h(Tag, { color: color }, () => text);
    },
    resizable: true,
  },
  {
    title: t('common.createDateText'),
    dataIndex: 'sys_create_datetime',
    width: 180,
    resizable: true,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'name',
    label: t('common.dict.nameText'),
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
    field: 'name',
    label: t('common.dict.nameText'),
    required: true,
    component: 'Input',
  },
  {
    field: 'code',
    label: t('common.dict.codeText'),
    required: true,
    component: 'Input',
  },
  {
    field: 'status',
    label: t('common.statusText'),
    component: 'RadioButtonGroup',
    required: true,
    defaultValue: true,
    componentProps: {
      options: [
        { label: t('common.enableText'), value: true },
        { label: t('common.disableText'), value: false },
      ],
    },
  },
  {
    field: 'sort',
    label: t('common.sortText'),
    component: 'InputNumber',
    required: true,
  },
  {
    label: t('common.remarkText'),
    field: 'remark',
    component: 'InputTextArea',
  },
];
