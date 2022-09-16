<template>
  <div class="system-menu-container">
    <el-dialog title="确认信息" v-model="state.isShowDialog" width="769px" :destroy-on-close="true">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="类型">
              <el-input v-model="state.partsdetail.type" clearable disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="型号">
              <el-input disabled v-model="state.partsdetail.spec" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="外修数量">
              <el-input disabled v-model="state.partsdetail.use_count" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="名称">
              <el-input disabled v-model="state.partsdetail.use_part_name" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="state.ruleForm.name" placeholder="申请人" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit()" :loading="state.issave" size="small">确定</el-button>
        </span></template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import {
  reactive,
  toRefs,
  inject,
  onMounted,
  onUnmounted,
} from "vue";
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
    areaArr: [],
    area: "",
  },
  confirmvalue: "",
  partsdetail: [] as any,
});




const openDialog = (row?: any) => {
  console.log("row");
  console.log(row);
  state.partsdetail = row;

  state.isShowDialog = true;
};

defineExpose({ openDialog })

// 关闭弹窗
const closeDialog = (row?: object) => {
  state.isShowDialog = false;
  initForm()
};
// 取消
const onCancel = () => {

  closeDialog();

};
// 新增

//确认提交
const initrepair: any = inject("initrepair");
const onSubmit = () => {
  if (state.ruleForm.name == "") {
    ElMessage.warning({
      message: "请重新输入",
      type: "warning",
    });
    return;
  }
  //更新确认人


  service.post("/updateMachine_repair", {
   
      //row的id 不是parts 的id
      id: state.partsdetail.id,
      useconfirm: state.partsdetail.useconfirm,
      use_count: state.partsdetail.use_count,
      use_area: state.partsdetail.use_area,
      use_date: formatDate111(state.partsdetail.use_date),
      use_part_name: state.partsdetail.use_part_name,
      use_reason: state.partsdetail.use_reason,
      type: state.partsdetail.type,
      spec: state.partsdetail.spec,
      new_area: state.ruleForm.area,
      applicant: state.ruleForm.name,
      receipt: state.partsdetail.receipt,
      applicantdate: formatDate111(new Date())
    }
    
 ).then((res: any) => {
    console.log('res', res);
  
    initrepair("other");
    closeDialog();

  }).catch((err: any) => {

  })
 


}

const initForm = () => {
  state.ruleForm.name = "";

  //onUnmounted(initForm);
};

</script>
