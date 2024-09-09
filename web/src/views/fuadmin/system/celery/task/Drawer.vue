<template>
  <BasicDrawer
    v-bind="$attrs"
    @register="registerDrawer"
    showFooter
    :title="getTitle"
    width="50%"
    @ok="handleSubmit"
  >
    <BasicForm @register="registerForm">
      <template #taskCron="{ model, field }">
        <FuadminCron v-model:value="model[field]" />
      </template>
    </BasicForm>
  </BasicDrawer>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicForm, useForm } from '@/components/Form/index';
  import { BasicDrawer, useDrawerInner } from '@/components/Drawer';
  import { createOrUpdate } from './api';
  import { formSchema } from './data';
  import { useI18n } from '@/hooks/web/useI18n';
  import { FuadminCron } from '@/components/Fu FastApi Vue/Cron';

  export default defineComponent({
    name: 'ButtonDrawer',
    components: { BasicDrawer, BasicForm, FuadminCron },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const { t } = useI18n();

      const [registerForm, { resetFields, setFieldsValue, validate }] = useForm({
        labelWidth: 100,
        schemas: formSchema,
        showActionButtonGroup: false,
        baseColProps: { lg: 24, md: 24 },
      });

      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(async (data) => {
        await resetFields();
        setDrawerProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        if (unref(isUpdate)) {
          // crontab和interval本来是对象，现在转换为id
          const record = data.record;
          const crontabObj = record.crontab;
          const crontab = `${crontabObj.minute} ${crontabObj.hour} ${crontabObj.day_of_month} ${crontabObj.month_of_year} ${crontabObj.day_of_week}`;
          const timezone = crontabObj.timezone;
          await setFieldsValue({
            ...record,
            crontab,
            timezone,
          });
        }
      });

      const getTitle = computed(() =>
        !unref(isUpdate) ? t('common.addText') : t('common.updateText'),
      );

      async function handleSubmit() {
        try {
          const values = await validate();
          setDrawerProps({ confirmLoading: true });
          await createOrUpdate(values, unref(isUpdate));
          closeDrawer();
          emit('success');
        } finally {
          setDrawerProps({ confirmLoading: false });
        }
      }

      return {
        registerDrawer,
        registerForm,
        getTitle,
        handleSubmit,
      };
    },
  });
</script>
