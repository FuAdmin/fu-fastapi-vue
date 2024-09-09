<template>
  <div>
    <BasicTable @register="registerTable">
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <TableAction
            :actions="[
              {
                type: 'primary',
                icon: 'bi:eye',
                color: 'success',
                auth: ['post:update'],
                onClick: handleEdit.bind(null, record),
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <Drawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>
<script setup lang="ts">
  import { BasicTable, useTable, TableAction } from '@/components/Table';

  import { useDrawer } from '@/components/Drawer';
  import Drawer from './Drawer.vue';

  import { getList } from './api';
  import { columns, searchFormSchema } from './data';
  import { message } from 'ant-design-vue';
  import { useI18n } from '@/hooks/web/useI18n';

  defineOptions({ name: 'LoginLogManagement' });
  const { t } = useI18n();
  const [registerDrawer, { openDrawer }] = useDrawer();
  // const { createMessage } = useMessage();
  const [registerTable, { reload }] = useTable({
    api: getList,
    columns,
    formConfig: {
      labelWidth: 80,
      schemas: searchFormSchema,
    },
    useSearchForm: true,
    showTableSetting: true,
    tableSetting: { fullScreen: true },
    bordered: true,
    showIndexColumn: false,
    actionColumn: {
      width: 80,
      title: t('common.operationText'),
      dataIndex: 'action',
      fixed: undefined,
    },
  });

  function handleEdit(record: Recordable) {
    openDrawer(true, {
      record,
      isUpdate: true,
    });
  }

  function handleSuccess() {
    message.success(t('common.successText'));
    reload();
  }
</script>
