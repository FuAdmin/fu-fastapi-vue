<template>
  <div>
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <Space style="height: 40px">
          <a-button type="primary" preIcon="ant-design:plus-outlined" @click="handleCreate">
            {{ t('common.addText') }}
          </a-button>
          <a-button color="error" preIcon="ant-design:delete-outlined" @click="handleBulkDelete">
            {{ t('common.delText') }}
          </a-button>
        </Space>
      </template>

      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <TableAction
            :actions="[
              {
                type: 'primary',
                icon: 'clarity:note-edit-line',
                onClick: handleEdit.bind(null, record),
              },
              {
                icon: 'ant-design:delete-outlined',
                type: 'primary',
                color: 'error',
                popConfirm: {
                  title: t('common.delHintText'),
                  confirm: handleDelete.bind(null, record.id),
                },
              },
              {
                type: 'primary',
                color: 'success',
                label: t('common.role.user'),
                onClick: handleUser.bind(null, record),
              },
              {
                type: 'primary',
                color: 'warning',
                onClick: handlePermission.bind(null, record),
                label: t('common.role.permissionMng'),
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <RoleDrawer @register="registerDrawer" @success="handleSuccess" />
    <PermissionDrawer @register="registerPermissionDrawer" @success="handleSuccess" />
    <RoleUser @register="registerRoleUserDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts" setup>
  import { BasicTable, useTable, TableAction } from '@/components/Table';

  import { useDrawer } from '@/components/Drawer';
  import RoleDrawer from './RoleDrawer.vue';
  import PermissionDrawer from './PermissionDrawer/index.vue';
  import RoleUser from './role-user/index.vue';

  import { columns, searchFormSchema } from './role.data';
  import { getList, deleteItem } from '@/views/fuadmin/system/role/role.api';
  import { message, Space } from 'ant-design-vue';
  import { useMessage } from '@/hooks/web/useMessage';
  import { useI18n } from '@/hooks/web/useI18n';

  const { t } = useI18n();

  const [registerDrawer, { openDrawer }] = useDrawer();
  const [registerPermissionDrawer, { openDrawer: openPermissionDrawer }] = useDrawer();
  const [registerRoleUserDrawer, { openDrawer: openRoleUserDrawer }] = useDrawer();

  const { createConfirm } = useMessage();
  const [registerTable, { reload, getSelectRows }] = useTable({
    api: getList,
    columns,
    formConfig: {
      labelWidth: 80,
      schemas: searchFormSchema,
    },
    rowSelection: {
      type: 'checkbox',
    },
    useSearchForm: true,
    showTableSetting: true,
    tableSetting: {
      fullScreen: true,
    },
    bordered: true,
    showIndexColumn: false,
    actionColumn: {
      width: 150,
      title: t('common.operationText'),
      dataIndex: 'action',
      fixed: undefined,
    },
  });

  function handleCreate() {
    openDrawer(true, {
      isUpdate: false,
    });
  }

  function handleEdit(record: Recordable) {
    openDrawer(true, {
      record,
      isUpdate: true,
    });
  }

  function handlePermission(record: Recordable) {
    openPermissionDrawer(true, record);
  }

  function handleUser(record: Recordable) {
    openRoleUserDrawer(true, record);
  }

  async function handleDelete(id: number) {
    await deleteItem(id);
    message.success(t('common.successText'));
    await reload();
  }

  async function handleBulkDelete() {
    if (getSelectRows().length == 0) {
      message.warning(t('common.batchDelHintText'));
    } else {
      createConfirm({
        iconType: 'warning',
        title: t('common.hintText'),
        content: t('common.delHintText'),
        async onOk() {
          for (const item of getSelectRows()) {
            await deleteItem(item.id);
          }
          message.success(t('common.successText'));
          await reload();
        },
      });
    }
  }

  function handleSuccess() {
    reload();
  }
</script>
