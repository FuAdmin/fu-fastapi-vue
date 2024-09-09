<template>
  <Tabs
    class="account-setting"
    tab-position="left"
    :tabBarStyle="{
      width: '220px',
    }"
    v-model:activeKey="activeKey"
  >
    <TabPane key="1" :tab="t('common.account.basicSettingText')">
      <BaseSetting />
    </TabPane>
    <TabPane key="2" :tab="t('common.account.secureSettingText')">
      <SecureSetting />
    </TabPane>
  </Tabs>
</template>

<script setup lang="ts">
  import { Tabs, TabPane } from 'ant-design-vue';
  import BaseSetting from './BaseSetting.vue';
  import SecureSetting from './SecureSetting.vue';
  import { useI18n } from '@/hooks/web/useI18n';
  import { ref } from 'vue';

  const activeKey = ref('1');
  defineOptions({ name: 'ProfileSetting' });

  const { t } = useI18n();
</script>
<style lang="less" scoped>
  //:deep(.ant-tabs-content-holder) {
  //  border: none;
  //}
  .account-setting {
    background-color: @component-background;
    border-radius: 8px;
    padding: 30px;
    height: 100%;

    .base-title {
      padding-left: 0;
    }

    .ant-tabs-tab-active {
      background-color: @item-active-bg;
    }
  }
</style>
