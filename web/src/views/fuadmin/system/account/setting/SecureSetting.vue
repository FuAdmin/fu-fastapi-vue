<template>
  <Row :gutter="24">
    <Col :span="14">
      <BasicForm @register="register" />
    </Col>
  </Row>
  <Button type="primary" @click="handleSubmit" :loading="loadStatus">
    {{ t('common.saveText') }}
  </Button>
</template>
<script lang="ts" setup>
  import { Button, message, Row, Col } from 'ant-design-vue';
  import { computed, onMounted, ref } from 'vue';
  import { BasicForm, useForm } from '@/components/Form/index';
  import headerImg from '@/assets/images/header.jpg';
  import { secureSetschemas } from './data';
  import { useUserStore } from '@/store/modules/user';
  import { repassword } from '@/views/fuadmin/system/account/account.api';
  import { useI18n } from '@/hooks/web/useI18n';

  const { t } = useI18n();
  const userStore = useUserStore();
  const getUserInfo = computed(() => {
    const { name = '', id, avatar, desc } = userStore.getUserInfo || {};
    return { name, avatar: avatar || headerImg, desc, id };
  });
  let loadStatus = ref(false);

  const [register, { validate, resetFields }] = useForm({
    labelWidth: 120,
    schemas: secureSetschemas,
    showActionButtonGroup: false,
  });

  onMounted(async () => {
    // const data = await accountInfoApi();
    // setFieldsValue(data);
  });

  const avatar = computed(() => {
    const { avatar } = getUserInfo.value;
    return avatar || headerImg;
  });
  async function handleSubmit() {
    try {
      loadStatus.value = true;
      const values = await validate();
      values.id = getUserInfo.value.id;
      await repassword(values);
      await resetFields();
      loadStatus.value = false;
      message.success(t('sys.api.operationSuccess'));
    } catch {
      loadStatus.value = false;
    }
  }
</script>

<style lang="less" scoped>
  .change-avatar {
    img {
      display: block;
      margin-bottom: 15px;
      border-radius: 50%;
    }
  }
</style>
