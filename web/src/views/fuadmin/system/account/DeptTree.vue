<template>
  <div class="mr-2.5 overflow-hidden bg-white" style="border-radius: 8px">
    <BasicTree
      :toolbar="true"
      :search="true"
      :blockNode="true"
      showLine
      :clickRowToExpand="false"
      :treeData="treeData"
      :fieldNames="{ key: 'id', title: 'name' }"
      :loading="loading"
      @select="handleSelect"
      ref="asyncExpandTreeRef"
    />
  </div>
</template>
<script lang="ts" setup>
  import { nextTick, onMounted, ref, unref } from 'vue';
  import { getDeptList } from '../dept/dept.api';
  import { BasicTree, TreeItem } from '@/components/Tree';
  import XEUtils from 'xe-utils';

  const emit = defineEmits(['select']);
  const treeData = ref<TreeItem[]>([]);
  const loading = ref(false);
  const asyncExpandTreeRef = ref(null);
  const projectName = import.meta.env.VITE_GLOB_APP_TITLE;

  async function fetch() {
    try {
      loading.value = true;
      const topLevel: any = {
        name: projectName,
        id: '0',
        children: [],
      };
      topLevel.children = await getDeptList({});
      treeData.value = [topLevel];
      console.log(treeData.value);
      // 展开全部
      await nextTick(() => {
        console.log(unref(asyncExpandTreeRef));
        unref(asyncExpandTreeRef)?.expandAll(true);
      });
    } finally {
      loading.value = false;
    }
  }

  function handleSelect(keys, event) {
    const data = XEUtils.toTreeArray(event.selectedNodes);
    let dept_ids: any = [];
    data.forEach((item) => {
      return dept_ids.push(item.id);
    });
    if (keys[0] == 0) dept_ids = undefined;
    emit('select', dept_ids);
  }

  onMounted(() => {
    fetch();
  });
</script>

<style scoped lang="less">
  ::v-deep(.ant-card-body) {
    padding: 19px 10px 10px 10px;
  }
  ::v-deep(.vben-tree-header) {
    padding-bottom: 20px;
    border: 0;
  }
  ::v-deep(.vben-tree) {
    padding: 10px 10px 10px 10px;
  }
  ::v-deep(.scroll-container) {
    box-shadow: none;
  }
</style>
