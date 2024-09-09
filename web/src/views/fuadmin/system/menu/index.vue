<template>
  <div>
    <BasicTable @register="registerTable" @fetch-success="onFetchSuccess">
      <template #tableTitle>
        <Space style="height: 40px">
          <a-button type="primary" preIcon="ant-design:plus-outlined" @click="handleCreate">
            {{ t('common.addText') }}
          </a-button>
        </Space>
      </template>
      <template #toolbar>
        <a-button type="primary" @click="expandAll">{{ t('common.expandText') }}</a-button>
        <a-button type="primary" @click="collapseAll">{{ t('common.collapseText') }}</a-button>
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
                type: 'primary',
                color: 'error',
                icon: 'ant-design:delete-outlined',
                popConfirm: {
                  title: t('common.delHintText'),
                  confirm: handleDelete.bind(null, record.id),
                },
              },
              {
                type: 'primary',
                color: 'success',
                icon: 'ant-design:plus-square-outlined',
                onClick: handleCreate.bind(null, record.id),
              },
              {
                type: 'primary',
                color: 'warning',
                tooltip: t('common.menuButtonText'),
                icon: 'ant-design:inbox-outlined',
                onClick: addButton.bind(null, record),
                ifShow: record.type === 1,
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <MenuDrawer @register="registerDrawer" @success="handleSuccess" />
    <AddMenuButton @register="registerAddButtonDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts">
  import { defineComponent, nextTick } from 'vue';

  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { getMenuList, deleteItem } from '/@/views/fuadmin/system/menu/menu.api';
  import { useDrawer } from '/@/components/Drawer';
  import MenuDrawer from './MenuDrawer.vue';
  import AddMenuButton from './add_button/index.vue';
  // import { useRouter } from 'vue-router';
  import { Space } from 'ant-design-vue';

  import { columns, searchFormSchema } from './menu.data';
  import { useI18n } from '/@/hooks/web/useI18n';

  export default defineComponent({
    name: 'MenuManagement',
    components: { BasicTable, MenuDrawer, TableAction, AddMenuButton, Space },
    setup() {
      const { t } = useI18n();
      const [registerDrawer, { openDrawer }] = useDrawer();
      const [registerAddButtonDrawer, { openDrawer: openAddButtonDrawer }] = useDrawer();
      // const { push } = useRouter();

      const [registerTable, { reload, expandAll, collapseAll }] = useTable({
        api: getMenuList,
        columns,
        formConfig: {
          labelWidth: 120,
          schemas: searchFormSchema,
        },
        isTreeTable: true,
        pagination: false,
        striped: false,
        useSearchForm: true,
        showTableSetting: true,
        bordered: true,
        showIndexColumn: false,
        canResize: false,
        tableSetting: { fullScreen: true },
        actionColumn: {
          align: 'left',
          width: 150,
          title: t('common.operationText'),
          dataIndex: 'action',
          fixed: undefined,
        },
      });

      function handleCreate(id?: string) {
        if (typeof id === 'string') {
          openDrawer(true, {
            isUpdate: false,
            parent_id: id,
          });
        } else {
          openDrawer(true, {
            isUpdate: false,
          });
        }
      }

      function handleEdit(record: Recordable) {
        openDrawer(true, {
          record,
          isUpdate: true,
        });
      }

      function addButton(record: Recordable) {
        // push({ name: 'AddMenuButton', params: { id: id } });
        openAddButtonDrawer(true, record);
      }

      async function handleDelete(id: number) {
        await deleteItem(id);
        await reload();
      }

      function handleSuccess() {
        reload();
      }

      function onFetchSuccess() {
        // 演示默认展开所有表项
        nextTick(expandAll);
      }

      return {
        registerTable,
        registerDrawer,
        handleCreate,
        handleEdit,
        handleDelete,
        handleSuccess,
        onFetchSuccess,
        expandAll,
        collapseAll,
        addButton,
        registerAddButtonDrawer,
        t,
      };
    },
  });
</script>
