<template>
  <div class="system-menu-container">
    <el-dialog title="添加备件" v-model="isShowDialog" width="769px">
      <el-form :model="ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件名称">
              <el-input v-model="ruleForm.part_name" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件规格">
              <el-input v-model="ruleForm.part_spec" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="搁置区域">
              <el-input placeholder v-model="ruleForm.area"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存">
              <el-input v-model="ruleForm.balance" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input v-model="ruleForm.original" placeholder clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备注">
              <el-input v-model="ruleForm.remark" placeholder clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="类型">
              <el-input v-model="ruleForm.type" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row> </el-form
      ><template #footer
        ><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="issave" size="small"
            >保存</el-button
          >
        </span></template
      >
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { reactive, toRefs } from "vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
export default {
  setup() {
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
        id: "",
        part_name: "",
        part_spec: "",
        area: "",
        balance: "",
        original: "",
        type: "",
        remark: "",
      },
    });
    // 打开弹窗
    const openDialog = (row?: object) => {
      console.log(row);
      state.isShowDialog = true;
    };
    // 关闭弹窗
    const closeDialog = (row?: object) => {
      console.log(row);
      state.isShowDialog = false;
    };
    // 是否内嵌下拉改变
    // const onSelectIframeChange = () => {
    // 	if (state.ruleForm.meta.isIframe === 'true') {
    // 		state.ruleForm.isLink = 'true';
    // 	} else {
    // 		state.ruleForm.isLink = '';
    // 	}
    // };
    // 取消
    const onCancel = () => {
      closeDialog();
      initForm();
    };
    // 新增
    const onSubmit = () => {
      console.log(state.ruleForm); // 数据，请注意需要转换的类型
      closeDialog(); // 关闭弹窗
      // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
    };
    // 表单初始化，方法：`resetFields()` 无法使用
    const initForm = () => {
      state.ruleForm.part_name = "";
      state.ruleForm.part_spec = "";
      state.ruleForm.area = "";
      state.ruleForm.balance = "";
      state.ruleForm.original = "";

      state.ruleForm.remark = "";
      state.ruleForm.type = "";
    };
    return {
      openDialog,
      closeDialog,
      onCancel,
      onSubmit,
      ...toRefs(state),
    };
  },
};
</script>
