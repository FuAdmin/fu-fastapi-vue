<template>
  <BasicTree
    :treeData="menuTreeData"
    :fieldNames="{ title: 'title', key: 'id' }"
    :checkedKeys="checkedKeys"
    v-model:value="checkTreeData"
    :selectable="false"
    checkable
    show-icon
    title="菜单权限"
    @check="check"
    checkStrictly
    toolbar
    ref="treeRef"
  />
</template>
<script lang="ts">
  import { defineComponent, nextTick, ref, unref } from 'vue';
  import { BasicTree, TreeActionType, TreeItem } from '@/components/Tree';
  import { getMenuList } from '@/views/fuadmin/system/menu/menu.api';

  export default defineComponent({
    name: 'MenuPermission',
    components: { BasicTree },
    props: {
      checkedKeys: {
        type: Array,
        default: null,
      },
    },
    emits: ['success', 'register', 'menuData'],
    setup(_, { emit }) {
      const checkTreeData = ref([]);
      //树的选中的节点信息
      const selectedKeys = ref([]);

      const menuTreeData = ref<TreeItem[]>([]);
      const treeRef = ref<Nullable<TreeActionType>>(null);

      async function loadData() {
        menuTreeData.value = await getMenuList();
        nextTick(() => {
          unref(treeRef)?.expandAll(true);
        });
      }

      function check(val) {
        const checkData = val.checked;
        nextTick(() => {
          emit('menuData', { checkChildMenuData: val, checkMenuData: checkData });
        });
      }

      return {
        checkTreeData,
        selectedKeys,
        menuTreeData,
        treeRef,
        loadData,
        check,
      };
    },
  });
</script>
