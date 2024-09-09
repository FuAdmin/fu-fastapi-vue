<template>
  <BasicTree
    :treeData="buttonTreeData"
    :fieldNames="{ title: 'title', key: 'id' }"
    :checkedKeys="checkedKeys"
    v-model:value="checkTreeData"
    checkable
    show-icon
    title="按钮权限"
    :selectable="false"
    toolbar
    @check="check"
    ref="treeRef"
  />
</template>
<script lang="ts">
  import { defineComponent, nextTick, ref, unref } from 'vue';
  import { BasicTree, TreeActionType, TreeItem } from '@/components/Tree';
  import XEUtils from 'xe-utils';
  import { getMenuButtonList } from '@/views/fuadmin/system/role/role.api';

  export default defineComponent({
    name: 'ButtonPermission',
    components: { BasicTree },
    props: {
      menuIds: {
        type: Array,
        default: null,
      },
      checkedKeys: {
        type: Array,
        default: null,
      },
    },
    emits: ['success', 'register', 'buttonData'],
    setup(_, { emit }) {
      const checkTreeData = ref([]);
      //树的选中的节点信息
      const buttonTreeData = ref<TreeItem[]>([]);
      const treeRef = ref<Nullable<TreeActionType>>(null);

      async function loadData() {
        buttonTreeData.value = await getMenuButtonList();
        buttonTreeData.value = XEUtils.toArrayTree(buttonTreeData.value, {
          parentKey: 'parent_id',
          strict: true,
        });
        nextTick(() => {
          unref(treeRef)?.expandAll(true);
        });
      }

      function check(val) {
        nextTick(() => {
          emit('buttonData', val);
        });
      }

      return {
        checkTreeData,
        buttonTreeData,
        treeRef,
        check,
        loadData,
      };
    },
  });
</script>
