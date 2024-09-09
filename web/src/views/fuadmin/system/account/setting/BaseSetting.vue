<template>
  <Row :gutter="24">
    <Col :span="14">
      <BasicForm @register="register">
        <template #avatar="{ model, field }">
          <CropperAvatar
            width="80"
            :showBtn="false"
            :uploadApi="uploadApi"
            v-model:value="model[field]"
          />
        </template>
      </BasicForm>
    </Col>
  </Row>
  <Button type="primary" @click="handleSubmit"> {{ t('common.saveText') }} </Button>
</template>
<script lang="ts" setup>
  import { Button, Row, Col, message } from 'ant-design-vue';
  import { computed, onMounted } from 'vue';
  import { BasicForm, useForm } from '@/components/Form/index';
  import { CropperAvatar } from '@/components/Cropper';

  import headerImg from '@/assets/images/header.jpg';
  import { baseSetschemas } from './data';
  import { useUserStore } from '@/store/modules/user';
  import { uploadApi } from '@/api/sys/upload';
  import { createOrUpdate, getById } from '@/views/fuadmin/system/account/account.api';
  import { useI18n } from '@/hooks/web/useI18n';

  const { t } = useI18n();
  const userStore = useUserStore();
  const getUserInfo = computed(() => {
    const { name = '', id, avatar, desc } = userStore.getUserInfo || {};
    return { name, avatar: avatar || headerImg, desc, id };
  });
  const [register, { setFieldsValue, validate }] = useForm({
    labelWidth: 120,
    schemas: baseSetschemas,
    showActionButtonGroup: false,
  });

  onMounted(async () => {
    const data = await getById(getUserInfo.value.id);
    await setFieldsValue(data);
  });

  async function handleSubmit() {
    const values = await validate();
    updateAvatar(values.avatar);
    await createOrUpdate(values, true);
    message.success(t('sys.api.operationSuccess'));
  }

  function updateAvatar(src: string) {
    const userinfo = userStore.getUserInfo;
    userinfo.avatar = src;
    userStore.setUserInfo(userinfo);
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
