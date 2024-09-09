<template>
  <div>
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <Space style="height: 40px">
          <a-button
            type="primary"
            v-auth="['post:add']"
            preIcon="ant-design:plus-outlined"
            @click="handleCreate"
          >
            {{ t('common.addText') }}
          </a-button>
          <a-button
            type="primary"
            color="error"
            v-auth="['post:delete']"
            preIcon="ant-design:delete-outlined"
            @click="handleBulkDelete"
          >
            {{ t('common.delText') }}
          </a-button>
          <a-button
            type="primary"
            color="success"
            v-auth="['post:export']"
            preIcon="carbon:cloud-download"
            @click="handleExportData"
            :loading="exportLoading"
          >
            {{ t('common.exportText') }}
          </a-button>
          <BasicUpload
            :maxSize="20"
            :maxNumber="1"
            @change="handleChange"
            class="my-5"
            type="warning"
            :text="t('common.importText')"
            v-auth="['post:import']"
          />
        </Space>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <TableAction
            :actions="[
              {
                type: 'primary',
                icon: 'clarity:note-edit-line',
                auth: ['post:update'],
                onClick: handleEdit.bind(null, record),
              },
              {
                icon: 'ant-design:delete-outlined',
                type: 'primary',
                color: 'error',
                auth: ['post:delete'],
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
    <ButtonDrawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts" setup>
  import { BasicTable, useTable, TableAction } from '@/components/Table';
  import { useDrawer } from '@/components/Drawer';
  import ButtonDrawer from './PostDrawer.vue';
  import { BasicUpload } from '@/components/Upload';
  import {
    deleteItem,
    getList,
    exportData,
    importData,
    deleteBatchItem,
  } from '@/views/fuadmin/system/post/post.api';
  import { columns, searchFormSchema } from '@/views/fuadmin/system/post/post.data';
  import { message, Space } from 'ant-design-vue';
  import { useMessage } from '@/hooks/web/useMessage';
  import { downloadByData } from '@/utils/file/download';
  import { useI18n } from '@/hooks/web/useI18n';
  import { ref } from 'vue';

  defineOptions({ name: 'PostManagement' });
  const { t } = useI18n();
  const [registerDrawer, { openDrawer }] = useDrawer();
  const { createConfirm } = useMessage();
  const exportLoading = ref(false);
  const [registerTable, { reload, getSelectRows }] = useTable({
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
    rowSelection: {
      type: 'checkbox',
    },
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
          const ids = getSelectRows().map((item) => item.id);
          await deleteBatchItem({ ids });
          message.success(t('common.successText'));
          await reload();
        },
      });
    }
  }

  async function handleChange(list: string[]) {
    console.log(list[0]);
    await importData({ path: list[0] });
    message.success(`导入成功`);
    await reload();
  }

  async function handleExportData() {
    try {
      exportLoading.value = true;
      const response = await exportData();
      const data = response.data;
      downloadByData(data, '岗位数据.xlsx');
    } finally {
      exportLoading.value = false;
    }
  }

  function handleSuccess() {
    message.success(t('common.successText'));
    reload();
  }
</script>
