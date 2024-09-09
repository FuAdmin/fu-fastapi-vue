<template>
  <BasicDrawer v-bind="$attrs" @register="registerDrawerMenu" :title="getTitle" width="50%">
    <Tabs v-model:activeKey="activeKey" type="card">
      <TabPane key="1" tab="菜单按钮">
        <BasicTable @register="registerTable">
          <template #tableTitle>
            <Space>
              <a-button type="primary" @click="handleCreate"> {{ t('common.addText') }} </a-button>
              <a-button color="success" @click="quickAddVisible = true">
                {{ t('common.quickAddText') }}
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
                ]"
              />
            </template>
          </template>
        </BasicTable>
      </TabPane>
      <!--      <TabPane key="2" tab="列表字段">-->
      <!--        <BasicTable @register="registerColumnTable">-->
      <!--          <template #tableTitle>-->
      <!--            <Space style="height: 40px">-->
      <!--              <a-button type="primary" @click="handleColumnCreate">-->
      <!--                {{ t('common.addText') }}-->
      <!--              </a-button>-->
      <!--              <a-button-->
      <!--                type="primary"-->
      <!--                v-auth="['demo:delete']"-->
      <!--                preIcon="ant-design:delete-outlined"-->
      <!--                @click="handleColumnBulkDelete"-->
      <!--              >-->
      <!--                {{ t('common.delText') }}-->
      <!--              </a-button>-->
      <!--              <a-button color="success" @click="handleQuickImport">-->
      <!--                {{ t('common.quickImport') }}-->
      <!--              </a-button>-->
      <!--            </Space>-->
      <!--          </template>-->
      <!--          <template #bodyCell="{ column, record }">-->
      <!--            <template v-if="column.key === 'action'">-->
      <!--              <TableAction-->
      <!--                :actions="[-->
      <!--                  {-->
      <!--                    type: 'primary',-->
      <!--                    icon: 'clarity:note-edit-line',-->
      <!--                    onClick: handleColumnEdit.bind(null, record),-->
      <!--                  },-->
      <!--                  {-->
      <!--                    icon: 'ant-design:delete-outlined',-->
      <!--                    type: 'primary',-->
      <!--                    color: 'error',-->
      <!--                    popConfirm: {-->
      <!--                      title: t('common.delHintText'),-->
      <!--                      confirm: handleColumnDelete.bind(null, record.id),-->
      <!--                    },-->
      <!--                  },-->
      <!--                ]"-->
      <!--              />-->
      <!--            </template>-->
      <!--          </template>-->
      <!--        </BasicTable>-->
      <!--      </TabPane>-->
    </Tabs>
    <MenuButtonDrawer @register="registerDrawer" @success="handleSuccess" />
    <MenuColumnFieldDrawer @register="registerColumnDrawer" @success="handleColumnSuccess" />
    <MenuColumnQuickDrawer @register="registerQuickDrawer" @success="handleQuickSuccess" />
    <Modal
      v-model:open="quickAddVisible"
      :title="t('common.account.inputApi')"
      @ok="handleQuickAdd"
    >
      <Input v-model:value="prefixApi" addon-before="/api/" />
    </Modal>
  </BasicDrawer>
</template>
<script setup lang="ts">
  import { ref, unref } from 'vue';

  import { BasicTable, useTable, TableAction } from '@/components/Table';
  import { Tabs, TabPane, Space, message, Modal, Input } from 'ant-design-vue';
  import { BasicDrawer, useDrawer, useDrawerInner } from '@/components/Drawer';
  import { createOrUpdate, deleteItem, getList } from './menu_button.api';
  import {
    deleteItem as deleteColumnItem,
    getList as getColumnList,
  } from './menu_column_field.api';

  import { columns } from './menu_button.data';

  import { columns as columnColumns } from './menu_column_field.data';

  import MenuButtonDrawer from '@/views/fuadmin/system/menu/add_button/MenuButtonDrawer.vue';
  import { useI18n } from '@/hooks/web/useI18n';
  import MenuColumnFieldDrawer from '@/views/fuadmin/system/menu/add_button/MenuColumnFieldDrawer.vue';
  import MenuColumnQuickDrawer from '@/views/fuadmin/system/menu/add_button/MenuColumnQuickDrawer.vue';
  import { useMessage } from '@/hooks/web/useMessage';

  const { t } = useI18n();
  const activeKey = ref('1');
  const [registerDrawer, { openDrawer }] = useDrawer();
  const [registerColumnDrawer, { openDrawer: openColumnDrawer }] = useDrawer();
  const [registerQuickDrawer, { openDrawer: openQuickDrawer }] = useDrawer();
  const { createConfirm } = useMessage();
  const quickAddVisible = ref(false);
  const menuId = ref(0);
  const prefixApi = ref('');
  const path = ref();
  const [registerDrawerMenu] = useDrawerInner(async (data) => {
    menuId.value = data.id;
    path.value = data.path;
    await reload();
  });
  const getTitle = '添加按钮和列';

  const [registerTable, { reload }] = useTable({
    api: getList,
    columns,
    showTableSetting: true,
    bordered: true,
    showIndexColumn: false,
    searchInfo: {
      menu_id: menuId,
    },
    actionColumn: {
      width: 50,
      title: t('common.operationText'),
      dataIndex: 'action',
      fixed: 'right',
    },
  });

  const [registerColumnTable, { reload: reloadColumn, getSelectRows }] = useTable({
    api: getColumnList,
    columns: columnColumns,
    showTableSetting: true,
    bordered: true,
    showIndexColumn: true,
    searchInfo: {
      menu_id: menuId,
    },
    rowSelection: {
      type: 'checkbox',
    },
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
      menuId: unref(menuId),
    });
  }

  async function handleQuickAdd() {
    console.log(path.value);
    const lastSlashIndex = prefixApi.value.lastIndexOf('/');
    const name = prefixApi.value.substring(lastSlashIndex + 1)
    const payload = [
      {
        name: name + ' add',
        code: name + ':add',
        method: 1,
        api: '/api/' + prefixApi.value,
        sort: 1,
        menu_id: menuId.value,
      },
      {
        name: name + ' delete',
        code: name + ':delete',
        method: 3,
        api: '/api/' + prefixApi.value + '/:id',
        sort: 2,
        menu_id: menuId.value,
      },
      {
        name: name + ' update',
        code: name + ':update',
        method: 2,
        api: '/api/' + prefixApi.value + '/:id',
        sort: 3,
        menu_id: menuId.value,
      },
      {
        name: name + ' query',
        code: name + ':query',
        method: 0,
        api: '/api/' + prefixApi.value,
        sort: 4,
        menu_id: menuId.value,
      },
      {
        name: name + ' import',
        code: name + ':import',
        method: 1,
        api: '/api/' + prefixApi.value + '/import/data',
        sort: 5,
        menu_id: menuId.value,
      },
      {
        name: name + ' export',
        code: name + ':export',
        method: 1,
        api: '/api/' + prefixApi.value + '/export/data',
        sort: 6,
        menu_id: menuId.value,
      },
    ];
    await Promise.all([
      createOrUpdate(payload[0]),
      createOrUpdate(payload[1]),
      createOrUpdate(payload[2]),
      createOrUpdate(payload[3]),
      createOrUpdate(payload[4]),
      createOrUpdate(payload[5]),
    ]);
    quickAddVisible.value = false;
    await reload();
    message.success(t('sys.api.operationSuccess'));
  }

  function handleEdit(record: Recordable) {
    openDrawer(true, {
      record,
      isUpdate: true,
      menuId: unref(menuId),
    });
  }

  async function handleDelete(id: number) {
    await deleteItem(id);
    await reload();
  }

  function handleSuccess() {
    reload();
  }

  function handleColumnCreate() {
    openColumnDrawer(true, {
      isUpdate: false,
      menuId: unref(menuId),
    });
  }

  function handleColumnEdit(record: Recordable) {
    openColumnDrawer(true, {
      record,
      isUpdate: true,
      menuId: unref(menuId),
    });
  }

  async function handleColumnDelete(id: number) {
    await deleteColumnItem(id);
    await reloadColumn();
  }

  async function handleColumnBulkDelete() {
    if (getSelectRows().length == 0) {
      message.warning(t('common.batchDelHintText'));
    } else {
      createConfirm({
        iconType: 'warning',
        title: t('common.hintText'),
        content: t('common.delHintText'),
        async onOk() {
          for (const item of getSelectRows()) {
            await handleColumnDelete(item.id);
          }
          message.success(t('common.successText'));
        },
      });
    }
    await reloadColumn();
  }

  function handleColumnSuccess() {
    reloadColumn();
  }

  function handleQuickImport() {
    openQuickDrawer(true, {
      path: unref(path),
      menuId: unref(menuId),
    });
  }

  function handleQuickSuccess() {
    reloadColumn();
  }
</script>
