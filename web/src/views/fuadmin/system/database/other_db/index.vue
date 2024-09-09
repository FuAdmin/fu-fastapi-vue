<template>
  <div>
    <Row>
      <Col :span="6">
        <Card class="card-height" style="margin-right: 10px">
          <BasicTree
            :height="630"
            :search="true"
            show-icon
            :blockNode="true"
            ref="asyncTreeRef"
            :treeData="tree"
            :load-data="onLoadData"
            @select="handleSelect"
          >
            <template #title="{ title }">
              <Tooltip :title="title" placement="right">
                <span class="ellipsis">{{ title }}</span>
              </Tooltip>
            </template>
          </BasicTree>
        </Card>
      </Col>
      <Col :span="18">
        <Card class="card-height">
          <Tabs v-model:activeKey="activeKey" class="tabs-style">
            <TabPane key="1" tab="设计表结构">
              <BasicTable @register="registerTable">
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
              <!--              <a-button block type="dashed" @click="handleAdd"> 新增 </a-button>-->
            </TabPane>
            <TabPane key="2" tab="表详细信息">Content of Tab Pane 1</TabPane>
            <TabPane key="3" tab="预览表数据">Content of Tab Pane 3</TabPane>
          </Tabs>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script lang="ts" setup>
  import { Row, Col, Card, Tooltip, Tabs, TabPane, message, Space } from 'ant-design-vue';
  import { BasicTree, TreeActionType } from '@/components/Tree';
  import { onMounted, ref, unref, h } from 'vue';
  import { uniq } from 'lodash-es';
  import { BasicTable, useTable, TableAction, EditRecordRow, ActionItem } from '@/components/Table';
  // import { columnsHoliday, searchFormHolidaySchema } from '@/views/field_it/coe_roster/data';
  // import { getList, createOrUpdate, deleteItem } from './api.holiday';

  import type { Nullable } from '@vben/types';
  import {
    getDBList,
    getSchemaList,
    getTableList,
    getTableStructure,
    saveTableStructure,
  } from './api';
  import { columnsTableDesign } from './data';
  import { AppstoreAddOutlined, ConsoleSqlOutlined, SaveOutlined } from '@ant-design/icons-vue';

  let tableInfo = {};
  let deleteRecord: EditRecordRow = [];
  const [registerTable, { getDataSource, reload, setTableData, deleteTableDataRecord }] = useTable({
    showIndexColumn: false,
    striped: true,
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
        popConfirm: {
          title: '是否删除？',
          confirm: handleDelete.bind(null, record),
        },
      },
    ];
  }

  // 左边树
  const asyncTreeRef = ref<Nullable<TreeActionType>>(null);

  const tree = ref([]);
  const activeKey = ref('1');
  async function onLoadData(treeNode) {
    const pos: string = treeNode.pos;

    const asyncTreeAction: TreeActionType | null = unref(asyncTreeRef);
    if (pos.split('-').length === 2) {
      const schemas: any[] = await getSchemaList({ db_name: treeNode.eventKey });
      if (asyncTreeAction) {
        const nodeChildren = schemas.map((schema) => {
          return {
            title: schema.schema_name,
            key: treeNode.eventKey + '-' + schema.schema_name,
            icon: 'ant-design:codepen-outlined',
          };
        });
        asyncTreeAction.updateNodeByKey(treeNode.eventKey, { children: nodeChildren });
        asyncTreeAction.setExpandedKeys(
          uniq([treeNode.eventKey, ...asyncTreeAction.getExpandedKeys()]),
        );
      }
    }

    if (pos.split('-').length === 3) {
      const dbName = treeNode.eventKey.split('-')[0];
      const schemaName = treeNode.eventKey.split('-')[1];
      const tables: any[] = await getTableList({ db_name: dbName, schema_name: schemaName });
      if (asyncTreeAction) {
        const nodeChildren = tables.map((table) => {
          return {
            title: table.table_name,
            key: treeNode.eventKey + '-' + table.table_name,
            isLeaf: true,
            icon: 'ant-design:table-outlined',
          };
        });
        asyncTreeAction.updateNodeByKey(treeNode.eventKey, { children: nodeChildren });
        asyncTreeAction.setExpandedKeys(
          uniq([treeNode.eventKey, ...asyncTreeAction.getExpandedKeys()]),
        );
      }
    }

    // if (pos.split('-').length === 3) {
    //   if (asyncTreeAction) {
    //     const nodeChildren = [
    //       {
    //         title: 'table',
    //         key: treeNode.eventKey + '-' + 'table',
    //       },
    //       {
    //         title: 'view',
    //         key: treeNode.eventKey + '-' + 'view',
    //       },
    //     ];
    //
    //     asyncTreeAction.updateNodeByKey(treeNode.eventKey, { children: nodeChildren });
    //     asyncTreeAction.setExpandedKeys(
    //       uniq([treeNode.eventKey, ...asyncTreeAction.getExpandedKeys()]),
    //     );
    //   }
    // }
    // if (pos.split('-').length === 4) {
    //   const dbName = treeNode.eventKey.split('-')[0];
    //   const schemaName = treeNode.eventKey.split('-')[1];
    //   const category = treeNode.eventKey.split('-')[2];
    //   if (category === 'table') {
    //     const tables: any[] = await getTableList({ db_name: dbName, schema_name: schemaName });
    //     if (asyncTreeAction) {
    //       const nodeChildren = tables.map((table) => {
    //         return {
    //           title: table.table_name,
    //           key: table.table_name,
    //           isLeaf: true,
    //         };
    //       });
    //       asyncTreeAction.updateNodeByKey(treeNode.eventKey, { children: nodeChildren });
    //       asyncTreeAction.setExpandedKeys(
    //         uniq([treeNode.eventKey, ...asyncTreeAction.getExpandedKeys()]),
    //       );
    //     }
    //   }
    // }
  }

  async function loadTableStructure() {
    const tableStructure = await getTableStructure(tableInfo);
    await setTableData(tableStructure);
    handleEdit();
  }

  async function handleSelect(selectedKeys: string[], info: any) {
    tableInfo = {
      db_name: info.node.dataRef.key.split('-')[0],
      schema_name: info.node.dataRef.key.split('-')[1],
      table_name: info.node.dataRef.key.split('-')[2],
    };
    await loadTableStructure();
  }

  onMounted(async () => {
    const dbs = await getDBList();
    tree.value = dbs.map((db) => {
      return {
        title: db.db_name,
        key: db.db_name,
        icon: 'ant-design:database-outlined',
      };
    });
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
</style>
