<template>
  <div class="system-menu-container">
    <el-dialog title="新增角色" v-model="state.isShowDialog" width="500px">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">


          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色名称">
              <el-input v-model="state.ruleForm.auth_name" placeholder="角色名称" clearable>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色编码">
              <el-input v-model="state.ruleForm.auth_code" placeholder="角色编码" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" size="small">新 增</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs, onMounted, inject } from "vue";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

const state = reactive({
  isShowDialog: false,
  ruleForm: {
    auth_code: "",
    auth_name: "",
  },
});




// 打开弹窗
const openDialog = () => {
  console.log("in");
  
  state.isShowDialog = true;
};
defineExpose({ openDialog });
// 关闭弹窗
const closeDialog = (row?: object) => {
  console.log(row);
  state.isShowDialog = false;
};
// 是否内嵌下拉改变

// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增

const reciveparts: any = inject("reciveparts");
const onSubmit = () => {
  //检测 并且提交
  service
    .get("addRole", {
      params: {
        auth_code: state.ruleForm.auth_code,
        auth_name: state.ruleForm.auth_name,
      },
    })
    .then((res: any) => {

      ElMessage.success(res.data);
      
      reciveparts(10,1)
      closeDialog(); 
    })
   

  // 关闭弹窗
  // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
};

const initForm = () => {
  state.ruleForm.auth_code = "";
  state.ruleForm.auth_name = "";

};


</script>
