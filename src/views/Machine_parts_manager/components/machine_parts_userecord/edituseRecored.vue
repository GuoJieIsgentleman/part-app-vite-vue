<template>
  <div class="system-menu-container">
    <el-dialog title="编辑菜单" v-model="isShowDialog" width="769px">
      <el-form :model="ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="领用人">
              <el-input
                v-model="ruleForm.use_part_name"
                placeholder=""
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <!-- <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="使用区域">
              <el-input v-model="ruleForm." placeholder="" clearable></el-input>
            </el-form-item>
          </el-col> -->
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件类型">
              <el-input placeholder="备件类型" v-model="ruleForm.use_area" />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="领用时间">
              <el-input v-model="ruleForm.use_count" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="领用备件">
              <el-input v-model="ruleForm.use_count" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="领用数量">
              <el-input v-model="ruleForm.remark" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="确认人">
              <el-input v-model="ruleForm.type" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="领用备注">
              <el-input v-model="ruleForm.type" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="issave" size="small"
            >保存</el-button
          >
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { reactive, toRefs } from "vue";
import { useI18n } from "vue-i18n";
import service from "/@/utils/request";
import jsonEditorVue from "../../../../../vue-typescript-admin-template-master/src/views/components-demo/json-editor.vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
export default {
  name: "systemEditMenu",
  setup() {
    const { t } = useI18n();
    const state = reactive({
      issave: false,
      isShowDialog: false,
      shortcuts: [
        {
          text: "今天",
          value: new Date(),
        },
        {
          text: "昨天",
          value: () => {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24);
            return date;
          },
        },
        {
          text: "一周前",
          value: () => {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
            return date;
          },
        },
      ],
      /**
       * 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式（请注意参数类型！）
       * 受到 `element plus` 类型 `string/number/object` 影响，不可使用 `:value="true"`
       * 的写法，所以传值到后台时，需要转换成布尔值，否则页面可能出现玄学。
       * 路由权限标识为数组格式，基本都需要自行转换类型
       */
      ruleForm: {
        confirm: "",
        id: "",
        type: "",
        use_area: "",
        use_count: "",
        use_date: "",
        use_part_name: "",
        user: "",
        user_remark: "",

        // new: "",
        // new_date: "",
        // manner: "",
        // pike: "",
        // piker: " ",
        // piker_date: "",
        // piker_procline: "",
        // pike_reason: "",
        // confirm_person: "",
        remark: "",
        // filltime: "",
      },
    });
    // 打开弹窗
    const openDialog = (row: any) => {
      state.isShowDialog = true;
      console.log(row);
      state.ruleForm;
    };
    // 关闭弹窗
    const closeDialog = (row?: object) => {
      console.log(row);
      state.isShowDialog = false;
    };
    // 是否内嵌下拉改变
    const onSelectIframeChange = () => {
      // if (state.ruleForm.meta.isIframe === 'true') {
      // 	state.ruleForm.isLink = 'true';
      // } else {
      // 	state.ruleForm.isLink = '';
      // }
    };
    // 取消
    const onCancel = () => {
      closeDialog();
      initForm();
    };
    // 新增
    const onSubmit = () => {
      // 做保存 更新表的操作

      state.issave = !state.issave;
      //请求

      service
        .get("/update", {
          params: {
            ruleForm: state.ruleForm,
          },
        })
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
        });
      console.log("更新状态信息");

      closeDialog(); // 关闭弹窗
      // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
      state.issave = !state.issave;
    };
    // 表单初始化，方法：`resetFields()` 无法使用
    const initForm = () => {
      state.ruleForm.use_part_name = "";
      state.ruleForm.use_count = "";
      state.ruleForm.use_area = "";
      state.ruleForm.use_date = "";
      state.ruleForm.user = "";
    };

    return {
      openDialog,
      closeDialog,
      onSelectIframeChange,
      onCancel,
      onSubmit,
      ...toRefs(state),
    };
  },
};
</script>
