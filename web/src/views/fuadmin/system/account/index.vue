<template>
  <PageWrapper dense contentClass="flex">
    <DeptTree class="w-1/5 xl:w-1/6" @select="handleSelect" />
    <BasicTable @register="registerTable" class="w-4/5 xl:w-5/6" :searchInfo="searchInfo">
      <template #tableTitle>
        <Space style="height: 40px">
          <a-button type="primary" preIcon="ant-design:plus-outlined" @click="handleCreate">
            {{ t('common.addText') }}
          </a-button>

          <a-button type="error" preIcon="ant-design:delete-outlined" @click="handleBulkDelete">
            {{ t('common.delText') }}
          </a-button>
        </Space>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'avatar'">
          <template v-if="column.key === 'avatar'">
            <Avatar :size="40" :src="record.avatar" />
          </template>
        </template>

        <template v-if="column.key === 'action'">
          <TableAction
            :actions="[
              {
                type: 'primary',
                icon: 'clarity:note-edit-line',
                disabled: record.id === 1,
                onClick: handleEdit.bind(null, record),
              },
              {
                icon: 'ant-design:delete-outlined',
                type: 'primary',
                color: 'error',
                disabled: record.id === 1,
                popConfirm: {
                  title: t('common.delHintText'),
                  confirm: handleDelete.bind(null, record.id),
                },
              },
              {
                type: 'primary',
                icon: 'ant-design:key-outlined',
                color: 'warning',
                tooltip: t('common.account.resetPassword'),
                disabled: record.id === 1,
                popConfirm: {
                  title: t('common.account.resetPasswordHit'),
                  confirm: rePassword.bind(null, record.id),
                },
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <AccountModal @register="registerDrawer" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts" setup>
  import { reactive, ref } from 'vue';

  import { BasicTable, useTable, TableAction } from '@/components/Table';
  import { PageWrapper } from '@/components/Page';

  import { useDrawer } from '@/components/Drawer';
  import AccountModal from './AccountDrawer.vue';
  import DeptTree from './DeptTree.vue';
  import { columns, searchFormSchema } from './account.data';
  import { useGo } from '@/hooks/web/usePage';
  import { getList, deleteItem, resetPassword } from './account.api';
  import { message, Space, Avatar } from 'ant-design-vue';
  import { useMessage } from '@/hooks/web/useMessage';
  import { useI18n } from '@/hooks/web/useI18n';

  const { t } = useI18n();
  const go = useGo();
  const [registerDrawer, { openDrawer }] = useDrawer();
  const { createConfirm } = useMessage();
  const searchInfo = reactive<Recordable>({});
  const [registerTable, { reload, updateTableDataRecord, getSelectRows }] = useTable({
    api: getList,
    rowKey: 'id',
    columns,
    formConfig: {
      labelWidth: 80,
      schemas: searchFormSchema,
      autoSubmitOnEnter: true,
    },
    useSearchForm: true,
    tableSetting: { fullScreen: true },
    showTableSetting: true,
    bordered: true,
    handleSearchInfoFn(info) {
      return info;
    },
    rowSelection: {
      type: 'checkbox',
      getCheckboxProps(record: Recordable) {
        // Demo: 第一行（id为0）的选择框禁用
        if (record.id === 1) {
          return { disabled: true };
        } else {
          return { disabled: false };
        }
      },
    },
    actionColumn: {
      width: 200,
      title: t('common.operationText'),
      dataIndex: 'action',
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
    await reload();
  }

  async function rePassword(id: number) {
    await resetPassword(id);
    message.success(t('common.successText'));
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

  function handleSuccess({ isUpdate, values }) {
    if (isUpdate) {
      // 演示不刷新表格直接更新内部数据。
      // 注意：updateTableDataRecord要求表格的rowKey属性为string并且存在于每一行的record的keys中
      const result = updateTableDataRecord(values.id, values);
      console.log(result);
    } else {
      reload();
    }
    message.success(t('sys.api.operationSuccess'));
  }

  function handleSelect(dept_ids) {
    searchInfo.dept_ids = dept_ids;
    reload();
  }

  function handleView(record: Recordable) {
    go('/system/account_detail/' + record.id);
  }
</script>
