/**
 * -*- coding: utf-8 -*-
 * time: 2024/5/28 23:34
 * author: 臧成龙
 * JID: jzangc
 */
import { BasicColumn, FormSchema } from '@/components/Table';
import { useI18n } from '@/hooks/web/useI18n';

const { t } = useI18n();

export const columns: BasicColumn[] = [
  {
    title: t('common.account.avatarText'),
    dataIndex: 'avatar',
    resizable: true,
    width: 110,
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
];

export const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: 'id',
    component: 'Input',
    show: false,
  },
  {
    field: 'user_ids',
    label: 'Select User',
    component: 'TableUser',
    componentProps: {
      mode: 'multiple',
    },
    required: true,
  },
];
