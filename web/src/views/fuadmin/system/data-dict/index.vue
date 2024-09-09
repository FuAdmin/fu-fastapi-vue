<template>
  <div>
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <Space style="height: 40px">
          <a-button
            type="primary"
            preIcon="ant-design:plus-outlined"
            @click="handleCreate"
            v-auth="['dict:add']"
          >
            {{ t('common.addText') }}
          </a-button>
          <a-button
            type="primary"
            color="error"
            preIcon="ant-design:delete-outlined"
            v-auth="['dict:delete']"
            @click="handleBulkDelete"
          >
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
                tooltip: t('common.updateText'),
                onClick: handleEdit.bind(null, record),
                auth: ['dict:update'],
              },
              {
                type: 'primary',
                icon: 'ant-design:delete-outlined',
                color: 'error',
                tooltip: t('common.delText'),
                popConfirm: {
                  title: t('common.delHintText'),
                  confirm: handleDelete.bind(null, record.id),
                },
                auth: ['dict:delete'],
              },
              {
                type: 'primary',
                color: 'success',
                tooltip: t('common.dictConfigText'),
                icon: 'ant-design:setting-outlined',
                onClick: addDictItem.bind(null, record.id),
                auth: ['dict:update'],
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <DictDrawer @register="registerDrawer" @success="handleSuccess" />
    <AddDictItem @register="registerAddDictItemDrawer" />
  </div>
</template>
<script lang="ts" setup>
  import { BasicTable, useTable, TableAction } from '@/components/Table';
  import { useDrawer } from '@/components/Drawer';
  import DictDrawer from './DictDrawer.vue';
  import AddDictItem from './dict_item/index.vue';

  import { deleteItem, getList } from './dict.api';
  import { columns, searchFormSchema } from './dict.data';
  import { message, Space } from 'ant-design-vue';
  import { useMessage } from '@/hooks/web/useMessage';
  import { useI18n } from '@/hooks/web/useI18n';

  const { t } = useI18n();
  const [registerDrawer, { openDrawer }] = useDrawer();
  const [registerAddDictItemDrawer, { openDrawer: openAddDictItemDrawer }] = useDrawer();
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
    tableSetting: { fullScreen: true },
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

  function addDictItem(id: number) {
    openAddDictItemDrawer(true, {
      id,
    });
  }

  async function handleDelete(id: number) {
    await deleteItem(id);
    message.success(t('common.successText'));
    await reload();
  }

  function handleBulkDelete() {
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
