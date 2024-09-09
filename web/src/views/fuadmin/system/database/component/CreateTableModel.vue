<template>
  <BasicModal
    v-bind="$attrs"
    destroyOnClose
    @ok="handleSave"
    @register="registerModal"
    title="创建表"
    width="65%"
    :footer="false"
  >
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <Form name="basic" :model="tableInfo" :rules="formRules">
          <FormItem label="表名" name="table_name">
            <Input v-model:value="tableInfo.table_name" addon-before="custom_" />
          </FormItem>
          <Alert
            size="small"
            closable
            message="默认主键为id，系统会自动添加，在这里只需添加业务字段。"
            class="alert-tips"
            type="info"
            show-icon
          />
        </Form>
      </template>
      <template #toolbar>
        <Space>
          <Tooltip placement="top">
            <template #title>新增</template>
            <a-button type="link" :icon="h(AppstoreAddOutlined)" @click="handleAdd" />
          </Tooltip>
          <Tooltip placement="top">
            <template #title>保存</template>
            <a-button type="link" :icon="h(SaveOutlined)" @click="handleSave" />
          </Tooltip>
        </Space>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <TableAction :actions="createActions(record)" />
        </template>
      </template>
    </BasicTable>
    <!--      <BasicForm @register="registerCreateTable" />-->
  </BasicModal>
</template>

<script setup lang="ts">
  import { message, Space, Tooltip, Form, FormItem, Input, Alert } from 'ant-design-vue';
  import { AppstoreAddOutlined, SaveOutlined } from '@ant-design/icons-vue';
  import { validateLowercaseInput } from '@/utils/formRule';
  import { Rule } from 'ant-design-vue/lib/form';
  import { reactive, h } from 'vue';
  import { columnsTableDesign } from '../data';
  import { ActionItem, BasicTable, EditRecordRow, TableAction, useTable } from '@/components/Table';
  import BasicModal from '@/components/Modal/src/BasicModal.vue';
  import { useModalInner } from '@/components/Modal';
  import { createTable } from '@/views/fuadmin/system/database/current_db/api';

  const emit = defineEmits(['success', 'register']);

  const formRules: Record<string, Rule[]> = {
    table_name: [
      { required: true, message: '请输入表名' },
      { validator: validateLowercaseInput, trigger: 'change' },
    ],
  };

  const tableInfo = reactive({
    table_name: '',
  });

  const [registerTable, { getDataSource, reload, setTableData, deleteTableDataRecord }] = useTable({
    showIndexColumn: false,
    striped: false,
    useSearchForm: false,
    columns: columnsTableDesign,
    showTableSetting: false,
    bordered: false,
    actionColumn: {
      width: 50,
      title: 'Operation',
      dataIndex: 'action',
    },
    size: 'small',
    resizeHeightOffset: 30,
    pagination: false,
  });

  const [registerModal, { closeModal }] = useModalInner(async () => {
    setTableData([]);
    // setModalProps({ confirmLoading: false });
  });

  function createActions(record: EditRecordRow): ActionItem[] {
    return [
      {
        color: 'error',
        icon: 'ant-design:delete-outlined',
        popConfirm: {
          title: '是否删除？',
          confirm: handleDelete.bind(null, record),
        },
      },
    ];
  }
  async function handleSave() {
    try {
      const payload = getDataSource();
      tableInfo.table_name = 'custom_' + tableInfo.table_name;
      await createTable({ ...tableInfo, data: payload });
      closeModal();
      emit('success');
    } catch (e) {
      message.error('Failed', e);
    } finally {
      await reload();
    }
  }

  async function handleDelete(record: EditRecordRow) {
    deleteTableDataRecord(record.key);
  }

  function handleAdd() {
    const data = getDataSource();
    const addRow: EditRecordRow = {
      editable: true,
      isNew: true,
      key: `${Date.now()}`,
    };
    data.push(addRow);
  }
</script>

<style scoped lang="less"></style>
