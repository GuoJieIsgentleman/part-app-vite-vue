<template>
  <div class="system-menu-container">
    <el-dialog title="确认人" v-model="state.isShowDialog" width="300px">
      <el-input
        v-model="state.ruleForm.name"
        placeholder="请填写姓名"
        clearable
      ></el-input>
      <template #footer
        ><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button
            type="primary"
            @click="onSubmit(state.ruleForm.name)"
            :loading="state.issave"
            size="small"
            >确定</el-button
          >
        </span></template
      >
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs, defineEmits, defineExpose, inject } from "vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";

import { ElMessage } from "element-plus";

const state = reactive({
  issave: false,
  isShowDialog: false,
  ruleForm: {
    name: "",

    remark: "",
  },
  confirmvalue: "",
  partsdetail: [] as any,
});
// 打开弹窗
const openDialog = (row?: any) => {
  console.log("rowobjec");
  console.log(row);
  state.partsdetail = row;

  state.isShowDialog = true;
};

defineExpose({ openDialog });
// 关闭弹窗
const closeDialog = (row?: object) => {
  state.isShowDialog = false;
};
// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增

//确认提交
const inittooling_maintenance: any = inject("inittooling_maintenance");
const onSubmit = (v: any) => {
  if (v == "") {
    alert("请重新输入");
  } else {
    //更新确认人

    // const param = {
    //   id: state.partsdetail.id,
    //   spec: state.partsdetail.spec,
    //   type: state.partsdetail.type,
    //   use_area: state.partsdetail.use_area,
    //   use_count: state.partsdetail.use_count,
    //   use_date: formatDate111(state.partsdetail.use_date),
    //   use_part_name: state.partsdetail.use_part_name,
    //   use_reason: state.partsdetail.use_reason,
    //   useconfirm: state.partsdetail.useconfirm,
    //   user: state.partsdetail.user,
    // };

    service
      .get("/updatetooling_maintenance", {
        params: {
          id: state.partsdetail.id,
          maintenanceman: v,
          maintenance_date: formatDate111(new Date()),
        },
      })
      .then((res) => {
        ElMessage({
          type: "success",
          message: res.data,
        });
        inittooling_maintenance("other");
        closeDialog();
      })
      .catch((err) => {
        ElMessage({
          type: "error",
          message: err.data,
        });
        inittooling_maintenance("other");
        closeDialog();
      });
  }
};
// 关闭弹窗
// setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试

// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {
  state.ruleForm.name = "";
  // state.ruleForm.part_spec = "";
  // state.ruleForm.area = "";
  // state.ruleForm.balance = "";
  // state.ruleForm.original = "";
  // state.ruleForm.remark = "";

  // state.ruleForm.type = "";
};
</script>
