<template>
  <div>
    <BasicTable @register="registerTable">
      <!--      <template #tableTitle>-->
      <!--        <Space style="height: 40px">-->
      <!--          <BasicUpload :maxSize="20" :maxNumber="10" @change="handleChange" class="my-5" />-->
      <!--        </Space>-->
      <!--      </template>-->
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <TableAction
            :actions="[
              {
                type: 'primary',
                icon: 'bi:eye',
                color: 'success',
                onClick: handleEdit.bind(null, record),
              },
              {
                type: 'primary',
                icon: 'ant-design:cloud-download-outlined',
                color: 'success',
                onClick: handleDownload.bind(null, record),
              },
            ]"
          />
        </template>
      </template>
    </BasicTable>
    <Drawer @register="registerDrawer" @success="handleSuccess" />
  </div>
</template>
<script lang="ts" setup>
  import { BasicTable, useTable, TableAction } from '@/components/Table';
  import { useDrawer } from '@/components/Drawer';
  import Drawer from './Drawer.vue';
  import { download, getList } from './api';
  import { columns, searchFormSchema } from './data';
  import { message } from 'ant-design-vue';
  import { downloadByData } from '@/utils/file/download';
  import { useI18n } from '@/hooks/web/useI18n';

  const [registerDrawer, { openDrawer }] = useDrawer();
  const { t } = useI18n();
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

  async function handleDownload(record: Recordable) {
    const response = await download(record);
    await downloadByData(response.data, record.name);
    // downloadByData('text content', 'testName.txt');
  }

  function handleSuccess() {
    message.success(t('common.successText'));
    reload();
  }
</script>
