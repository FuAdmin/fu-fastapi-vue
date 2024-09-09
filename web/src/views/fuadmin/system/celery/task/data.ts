/**
 * -*- coding: utf-8 -*-
 * time: 2022/4/26 23:41
 * author: 臧成龙
 * QQ: 939589097
 */
import { BasicColumn, FormSchema } from '@/components/Table';
import { h } from 'vue';
import { Tag } from 'ant-design-vue';
import { getCrontabData } from '@/views/fuadmin/system/celery/util';
import { useI18n } from '@/hooks/web/useI18n';

const { t } = useI18n();

export const columns: BasicColumn[] = [
  {
    title: t('common.task.taskText'),
    dataIndex: 'task',
    width: 200,
  },
  {
    title: t('common.task.nameText'),
    dataIndex: 'name',
    width: 180,
  },
  {
    title: t('common.task.crontabText'),
    dataIndex: 'crontab',
    width: 100,
    customRender: ({ record }) => {
      return getCrontabData(record.crontab);
    },
  },
  {
    title: t('common.statusText'),
    dataIndex: 'enabled',
    width: 100,
    customRender: ({ record }) => {
      const status = record.enabled;
      const color = status ? 'success' : 'error';
      const text = status ? t('common.enableText') : t('common.disableText');
      return h(Tag, { color: color }, () => text);
    },
  },
  {
    title: t('common.task.lastRunTimeText'),
    dataIndex: 'last_run_at',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'task',
    label: t('common.task.taskText'),
    component: 'Input',
    colProps: { span: 6 },
  },
  {
    field: 'name',
    label: t('common.task.nameText'),
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
    field: 'task',
    label: t('common.task.taskText'),
    required: true,
    component: 'Input',
  },
  {
    field: 'name',
    label: t('common.task.nameText'),
    required: true,
    component: 'Input',
  },
  {
    field: 'timezone',
    label: t('common.timeZoneText'),
    required: true,
    component: 'DictSelect',
    componentProps: {
      dictCode: 'timezone',
    },
  },
  {
    field: 'crontab',
    label: t('common.task.crontabText'),
    helpMessage: 'Crontab表达式',
    slot: 'taskCron',
    required: true,
  },
  {
    field: 'kwargs',
    label: 'Kwargs',
    helpMessage: '必须是Json 格式',
    component: 'InputTextArea',
  },
  {
    field: 'args',
    label: 'Args',
    helpMessage: '必须是Json 格式',
    component: 'InputTextArea',
  },
  {
    field: 'enabled',
    label: t('common.statusText'),
    component: 'RadioButtonGroup',
    defaultValue: true,
    componentProps: {
      options: [
        { label: t('common.enableText'), value: true },
        { label: t('common.disableText'), value: false },
      ],
    },
  },
];
