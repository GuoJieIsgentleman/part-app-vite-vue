<template>
  <div class="system-menu-container">
    <el-dialog title="确认人" v-model="isShowDialog" width="300px">
      <el-input v-model="ruleForm.name" placeholder="请填写姓名" clearable></el-input>
      <template #footer
        ><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button
            type="primary"
            @click="onSubmit(ruleForm.name)"
            :loading="issave"
            size="small"
            >确定</el-button
          >
        </span></template
      >
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { reactive, toRefs, defineEmits, defineExpose, inject } from "vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";
export default {
  setup() {
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
    const initmaintenance: any = inject("initmaintenance");
    const onSubmit = async (v: any) => {
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
        console.log("---------v----------");
        console.log(v);
        let { data: res } = await service.get("/api/updatemaintenance", {
          params: {
            id: state.partsdetail.id,
            maintenanceman: v,
            maintenance_date: formatDate111(new Date()),
          },
        });

        console.log("更新保养明细返回值");
        console.log(res);
        initmaintenance();
        closeDialog();
      }

      // 关闭弹窗
      // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
    };
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
