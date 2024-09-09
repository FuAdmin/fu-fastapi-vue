<template>
  <div>
    <Row>
      <Col :span="6">
        <Card
          class="card-height"
          style="margin-right: 10px"
          v-loading="leftCardLoading"
          ref="leftCardRef"
        >
          <BasicTree
            :search="true"
            :load-data="onLoadData"
            :height="leftTreeHeight"
            show-icon
            :blockNode="true"
            ref="asyncTreeRef"
            :treeData="tree"
            @select="handleSelect"
          >
            <template #title="{ key: treeKey, title }">
              <Tooltip :title="title" placement="right">
                <Dropdown :trigger="['contextmenu']">
                  <span>{{ title }}</span>
                  <template #overlay>
                    <Menu @click="({ key: menuKey }) => onContextMenuClick(treeKey, menuKey)">
                      <MenuItem v-if="treeKey === 'custom_table'" :icon="h(PlusOutlined)" key="1"
                        >创建表</MenuItem
                      >
                      <!--                      <MenuItem-->
                      <!--                        v-if="!(treeKey === 'system_table' || treeKey === 'custom_table')"-->
                      <!--                        :icon="h(DeleteOutlined, { style: { color: '#c73838' } })"-->
                      <!--                        key="2"-->
                      <!--                        >删除表</MenuItem-->
                      <!--                      >-->
                    </Menu>
                  </template>
                </Dropdown>
              </Tooltip>
            </template>
          </BasicTree>
        </Card>
      </Col>
      <Col :span="18">
        <Card class="card-height" v-loading="rightCardLoading">
          <Result status="404" v-if="showBlank" sub-title="请在左侧选择一张表" />
          <Tabs
            v-model:activeKey="activeKey"
            v-if="!showBlank"
            class="tabs-style"
            @change="tabsChange"
          >
            <TabPane key="1" tab="设计表结构" force-render>
              <BasicTable @register="registerTable">
                <template #tableTitle>
                  <Input
                    style="width: 30%"
                    disabled
                    v-model:value="tableInfo.table_name"
                    addon-before="表名"
                  />
                </template>
                <template #toolbar>
                  <Space>
                    <Tooltip placement="top">
                      <template #title>新增</template>
                      <a-button
                        :disabled="!tableInfo.table_name.startsWith('custom_')"
                        type="link"
                        :icon="h(AppstoreAddOutlined)"
                        @click="handleAdd"
                      />
                    </Tooltip>
                    <Tooltip placement="top">
                      <template #title>保存</template>
                      <a-button
                        :disabled="!tableInfo.table_name.startsWith('custom_')"
                        type="link"
                        :icon="h(SaveOutlined)"
                        @click="handleSave"
                      />
                    </Tooltip>
                  </Space>
                </template>
                <template #bodyCell="{ column, record }">
                  <template v-if="column.key === 'action'">
                    <TableAction :actions="createActions(record)" />
                  </template>
                </template>
              </BasicTable>
              <!--              <a-button block type="dashed" @click="handleAdd"> 新增 </a-button>-->
            </TabPane>
            <!--            <TabPane key="2" tab="表详细信息">Content of Tab Pane 1</TabPane>-->
            <TabPane key="2" tab="预览表数据">
              <BasicTable @register="registerTableData">
                <template #tableTitle>
                  <Input
                    style="width: 30%"
                    disabled
                    v-model:value="tableInfo.table_name"
                    addon-before="表名"
                  />
                </template>
              </BasicTable>
            </TabPane>
          </Tabs>
        </Card>
      </Col>
    </Row>
    <CreateTableModel @register="registerCreateModal" @success="handleCreateTableSuccess" />
  </div>
</template>
<script lang="ts" setup>
  import {
    Card,
    Col,
    message,
    Row,
    Space,
    TabPane,
    Tabs,
    Result,
    Dropdown,
    Menu,
    MenuItem,
    Input,
  } from 'ant-design-vue';
  import { BasicTree, TreeActionType } from '@/components/Tree';
  import { h, nextTick, onMounted, onUnmounted, reactive, ref, unref } from 'vue';
  import { ActionItem, BasicTable, EditRecordRow, TableAction, useTable } from '@/components/Table';
  import type { Nullable } from '@vben/types';
  import { getTableList, getTableStructure, previewTableData, saveTableStructure } from './api';
  import { columnsTableDesign } from '../data';
  import { AppstoreAddOutlined, PlusOutlined, SaveOutlined } from '@ant-design/icons-vue';
  import { uniq } from 'lodash-es';
  import CreateTableModel from '../component/CreateTableModel.vue';
  import { useModal } from '@/components/Modal';
  import { useI18n } from '@/hooks/web/useI18n';

  const { t } = useI18n();
  let rightCardLoading = ref(false);
  let leftCardLoading = ref(false);
  let showBlank = ref(true);
  const leftCardRef = ref();
  let tableInfo = reactive({
    table_name: '',
  });
  let deleteRecord: EditRecordRow = [];

  const [registerCreateModal, { openModal }] = useModal();

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
  const [registerTableData, { setTableData: setTableDataPreview, setColumns: setColumnsPreview }] =
    useTable({
      showIndexColumn: false,
      striped: true,
      useSearchForm: false,
      columns: columnsTableDesign,
      showTableSetting: false,
      bordered: false,
      size: 'small',
      resizeHeightOffset: 30,
      pagination: false,
    });

  function tabsChange(key) {
    if (key === '1') {
      loadTableStructure();
    }
    if (key === '2') {
      loadTablePreviewData();
    }
  }

  async function handleCreateTableSuccess() {
    message.success(t('common.successText'));
    const asyncTreeAction: TreeActionType | null = unref(asyncTreeRef);
    const nodeCustomChildren: any = [];
    const tables: any[] = await getTableList();
    if (asyncTreeAction) {
      tables.forEach((table) => {
        const table_name = table.table_name;
        if (table_name.startsWith('custom_')) {
          nodeCustomChildren.push({
            title: table.table_name,
            key: 'custom_table' + '-' + table.table_name,
            isLeaf: true,
            icon: 'ant-design:table-outlined',
          });
        }
      });
      asyncTreeAction.updateNodeByKey('custom_table', { children: nodeCustomChildren });
      asyncTreeAction.setExpandedKeys(uniq(['custom_table', ...asyncTreeAction.getExpandedKeys()]));
    }
  }

  function handleEdit() {
    const tableDatas = getDataSource();
    tableDatas.forEach((item) => {
      item.onEdit?.(true);
    });
  }

  async function handleSave() {
    try {
      const payload = getDataSource();
      await saveTableStructure({ ...tableInfo, data: payload, delete_record: deleteRecord });

      deleteRecord = [];
      await loadTableStructure();
      message.success('Successfully');
    } catch (e) {
      message.error('Failed', e);
    } finally {
      await reload();
    }
  }

  async function handleDelete(record: EditRecordRow) {
    deleteRecord.push(record);
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
  function createActions(record: EditRecordRow): ActionItem[] {
    return [
      {
        color: 'error',
        icon: 'ant-design:delete-outlined',
        disabled: !tableInfo.table_name.startsWith('custom_'),
        popConfirm: {
          title: '是否删除？',
          confirm: handleDelete.bind(null, record),
        },
      },
    ];
  }

  // 左边树
  const asyncTreeRef = ref<Nullable<TreeActionType>>(null);

  const tree = ref([
    {
      title: '在线定义表',
      key: 'custom_table',
      icon: 'ant-design:folder-outlined',
    },
    {
      title: '系统内置表',
      key: 'system_table',
      icon: 'ant-design:folder-outlined',
    },
  ]);
  const activeKey = ref('1');

  function onContextMenuClick(treeKey: string, menuKey: string | number) {
    //创建表
    if (menuKey === '1') {
      openModal();
      // createTableModalOpen.value = true;
    }
    //删除表
    // if (menuKey === 2) {
    // }
    console.log(`treeKey: ${treeKey}, menuKey: ${menuKey}`);
  }
  async function onLoadData(treeNode) {
    const asyncTreeAction: TreeActionType | null = unref(asyncTreeRef);
    const tables: any[] = await getTableList();
    const nodeSystemChildren: any = [];
    const nodeCustomChildren: any = [];

    if (asyncTreeAction) {
      tables.forEach((table) => {
        const table_name = table.table_name;
        if (!table_name.startsWith('custom_')) {
          nodeSystemChildren.push({
            title: table.table_name,
            key: treeNode.eventKey + '-' + table.table_name,
            isLeaf: true,
            icon: 'ant-design:table-outlined',
          });
        } else {
          nodeCustomChildren.push({
            title: table.table_name,
            key: treeNode.eventKey + '-' + table.table_name,
            isLeaf: true,
            icon: 'ant-design:table-outlined',
          });
        }
      });
      if (treeNode.eventKey === 'custom_table') {
        asyncTreeAction.updateNodeByKey(treeNode.eventKey, { children: nodeCustomChildren });
      } else {
        asyncTreeAction.updateNodeByKey(treeNode.eventKey, { children: nodeSystemChildren });
      }
      asyncTreeAction.setExpandedKeys(
        uniq([treeNode.eventKey, ...asyncTreeAction.getExpandedKeys()]),
      );
    }
  }
  async function loadTableStructure() {
    const tableStructure = await getTableStructure(tableInfo);
    await setTableData(tableStructure);
    handleEdit();
  }

  async function loadTablePreviewData() {
    try {
      rightCardLoading.value = true;
      const data = await previewTableData(tableInfo);
      if (data.length === 0) {
        setColumnsPreview([]);
        setTableDataPreview([]);
        return;
      }
      await setColumnsPreview(
        Object.keys(data[0]).map((key) => {
          return {
            title: key,
            dataIndex: key,
            width: 135,
            resizable: true,
          };
        }),
      );
      await setTableDataPreview(data);
    } finally {
      rightCardLoading.value = false;
    }
  }

  async function handleSelect(selectedKeys: string[], info: any) {
    console.log(selectedKeys);
    showBlank.value = !(
      selectedKeys.length !== 0 &&
      selectedKeys[0] !== 'system_table' &&
      selectedKeys[0] !== 'custom_table'
    );

    try {
      rightCardLoading.value = true;
      tableInfo = {
        table_name: info.node.dataRef.key.split('-')[1],
      };
      if (activeKey.value === '1') await loadTableStructure();
      if (activeKey.value === '2') await loadTablePreviewData();
    } finally {
      rightCardLoading.value = false;
    }
  }

  onMounted(async () => {
    // try {
    //   leftCardLoading.value = true;
    //   tree.value = [
    //     {
    //       title: 'Tables',
    //       key: '0',
    //       icon: 'ant-design:database-outlined',
    //     },
    //     {
    //       title: 'Views',
    //       key: '1',
    //       icon: 'ant-design:eye-outlined',
    //     },
    //   ];
    // } finally {
    //   leftCardLoading.value = false;
    // }
  });
  let leftTreeHeight = ref(0);

  const adjustHeight = () => {
    // 获取组件的宽度
    const container: any = document.querySelector('.card-height');
    const height = container.clientHeight;
    leftTreeHeight.value = height - 95;
  };

  // 初始化高度
  onMounted(async () => {
    await nextTick(); // 等待 DOM 更新完成
    adjustHeight();
    window.addEventListener('resize', adjustHeight);
  });

  // 移除事件监听器
  onUnmounted(() => {
    window.removeEventListener('resize', adjustHeight);
  });
</script>
<style scoped lang="less">
  ::v-deep(.ant-card-body) {
    //padding: 10px 20px 10px 10px;
    padding: 10px;
  }
  ::v-deep(.vben-tree-header) {
    padding-bottom: 0;
    border: 0;
  }
  ::v-deep(.vben-tree) {
    padding: 10px 10px 10px 10px;
  }
  ::v-deep(.scroll-container) {
    box-shadow: none;
  }
  .card-height {
    height: calc(100vh - 123px);
  }
  .ellipsis {
    display: block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .tabs-style {
    padding: 0 20px 10px 20px;
  }
  :deep(.scroll-container) {
    border-radius: unset;
  }
</style>
