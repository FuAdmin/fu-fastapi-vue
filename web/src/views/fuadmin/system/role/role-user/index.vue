<template>
  <BasicDrawer v-bind="$attrs" @register="registerDrawerMenu" :title="getTitle" width="50%">
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <a-button type="primary" @click="handleCreate"> {{ t('common.addText') }} </a-button>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'avatar'">
          <template v-if="column.key === 'avatar'">
            <Avatar :size="25" :src="record.avatar" />
          </template>
        </template>
        <template v-if="column.key === 'action'">
          <TableAction
            :actions="[
              {
                icon: 'ant-design:delete-outlined',
                type: 'primary',
                color: 'error',
                popConfirm: {
                  title: t('common.delHintText'),
                  confirm: handleDelete.bind(null, record.id),
                },
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <DictItemDrawer @register="registerDrawer" @success="handleSuccess" />
  </BasicDrawer>
</template>
<script lang="ts" setup>
  import { ref, unref } from 'vue';
  import { Avatar } from 'ant-design-vue';
  import { BasicTable, useTable, TableAction } from '@/components/Table';
  import { BasicDrawer, useDrawer, useDrawerInner } from '@/components/Drawer';
  import { getUserListByRoleCode, removeUserFromRole } from './api';
  import { columns } from './data';
  import DictItemDrawer from './Drawer.vue';
  import { useI18n } from '@/hooks/web/useI18n';

  const { t } = useI18n();
  const [registerDrawer, { openDrawer }] = useDrawer();
  const roleId = ref('');
  const [registerDrawerMenu] = useDrawerInner(async (data) => {
    roleId.value = data.id;
    await reload();
  });
  const getTitle = '用户';

  const [registerTable, { reload }] = useTable({
    api: getUserListByRoleCode,
    searchInfo: { role_id: roleId },
    columns,
    showTableSetting: true,
    bordered: true,
    immediate: false,
    showIndexColumn: false,
    actionColumn: {
      width: 50,
      title: t('common.operationText'),
      dataIndex: 'action',
      fixed: 'right',
    },
  });

  function handleCreate() {
    openDrawer(true, {
      isUpdate: false,
      roleId: unref(roleId),
    });
  }

  async function handleDelete(id: number) {
    await removeUserFromRole({ user_id: id, role_id: unref(roleId) });
    await reload();
  }

  function handleSuccess() {
    reload();
  }
</script>
