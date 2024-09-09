/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/26 23:54
 * author: 臧成龙
 * JID: jzangc
 */
import { BasicColumn, FormSchema } from '@/components/Table';
import { useI18n } from '@/hooks/web/useI18n';

const { t } = useI18n();

export const columnsTableDesign: BasicColumn[] = [
  {
    title: 'Column Name',
    dataIndex: 'column_name',
    width: 100,
    resizable: true,
    editRow: true,
  },
  {
    title: 'Data Type',
    dataIndex: 'data_type',
    width: 100,
    resizable: true,
    editRow: true,
    editComponent: 'Select',
    editComponentProps: {
      options: [
        {
          label: 'Varchar',
          value: 'varchar',
        },
        {
          label: 'Integer',
          value: 'int',
        },
        {
          label: 'Bigint',
          value: 'bigint',
        },
        {
          label: 'Float',
          value: 'float',
        },
        {
          label: 'Datetime',
          value: 'datetime',
        },
        {
          label: 'Boolean',
          value: 'bool',
        },
        {
          label: 'Text',
          value: 'text',
        },
        {
          label: 'Json',
          value: 'json',
        },
        // {
        //   label: 'Decimal',
        //   value: 'decimal',
        // },
      ],
      style: {
        width: '100%',
      },
    },
  },
  {
    title: 'Max Length',
    dataIndex: 'max_length',
    width: 100,
    resizable: true,
    editRow: true,
  },
  {
    title: 'Allow Null',
    dataIndex: 'is_nullable',
    width: 100,
    resizable: true,
    editRow: true,
    editComponent: 'Checkbox',
  },
  {
    title: 'Primary Key',
    dataIndex: 'is_primary_key',
    width: 100,
    resizable: true,
    editRow: true,
    editComponent: 'Checkbox',
    editDynamicDisabled: true,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'table_name',
    label: '表名',
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
    label: t('common.post.nameText'),
    required: true,
    component: 'Input',
  },
  {
    field: 'code',
    label: t('common.post.codeText'),
    required: true,
    component: 'Input',
  },
  // {
  //   field: 'field',
  //   component: 'DictSelect',
  //   label: '字段',
  //   componentProps: {
  //     dictCode: 'status',
  //   },
  // },
  {
    field: 'status',
    label: t('common.statusText'),
    component: 'RadioButtonGroup',
    defaultValue: 1,
    componentProps: {
      options: [
        { label: t('common.enableText'), value: 1 },
        { label: t('common.disableText'), value: 0 },
      ],
    },
  },
  {
    field: 'sort',
    label: t('common.sortText'),
    component: 'InputNumber',
    required: true,
    defaultValue: 1,
  },
];
