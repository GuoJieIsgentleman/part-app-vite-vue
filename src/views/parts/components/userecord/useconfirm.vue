<template>
  <div class="system-menu-container">
    <el-dialog title="领用班长确认信息" v-model="state.isShowDialog" width="769px" :destroy-on-close="true">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用产线">
              <el-input disabled v-model="state.partsdetail.use_procline"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="类型">
              <el-input v-model="state.partsdetail.type" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="名称">
              <el-input disabled v-model="state.partsdetail.use_part_name"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="型号">
              <el-input disabled v-model="state.partsdetail.spec"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存数量">
              <el-input disabled v-model="state.ruleForm.balance"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input disabled v-model="state.ruleForm.original"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用数量">
              <el-input disabled v-model="state.partsdetail.use_count"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原搁置区域">
              <el-input disabled v-model="state.partsdetail.use_area"></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="替换备件处理方式">

              <el-select v-model="state.handle" placeholder="请选择">
                <el-option v-for="item in state.options" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="state.ruleForm.name" placeholder="班长确认" clearable></el-input>
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
import { reactive, toRefs, inject, onMounted } from "vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";
import { ElMessage } from "element-plus";


const state = reactive({
  options: [
    {
      value: "保养",
      label: "保养",
    },
    {
      value: "外修",
      label: "外修",
    },
    {
      value: "报废",
      label: "报废",
    },
    {
      value: "设备整改",
      label: "设备整改",
    },
  ],
  handle: "",
  issave: false,
  isShowDialog: false,
  ruleForm: {
    name: "",
    remark: "",
    areaArr: [],
    area: "",
    balance: 0,
    original: 0,
  },
  confirmvalue: "",
  partsdetail: [] as any,
});

//初始化 产线 区域
onMounted(async () => {
  let { data: res } = await service.get("/getarea");

  state.ruleForm.areaArr = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });

});
// 打开弹窗
const openDialog = async (row?: any) => {

  state.partsdetail = row;

  state.isShowDialog = true;
  getbalance();
};

defineExpose({ openDialog })


const getbalance = async () => {
  let { data: balance } = await service.get("/getbalance", {
    params: {
      area: state.partsdetail.use_area,
      type: state.partsdetail.type,
      spec: state.partsdetail.spec,
      part_name: state.partsdetail.use_part_name,
    },
  });



  state.ruleForm.balance = balance[0][4];
  state.ruleForm.original = balance[0][5];
};

// 关闭弹窗
const closeDialog = (row?: object) => {
  state.isShowDialog = false;
  initForm();
};
// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增

//确认提交
const inituserecord: any = inject("inituserecord");
const onSubmit = () => {
  if (state.ruleForm.name == "" || state.handle == "") {
    ElMessage.warning({
      message: "请重新输入",
      type: "warning",
    });
    return
  }
  //更新确认人

  service.get("/updateuserecord", {
    params: {
      //保养列表的id 不是parts 的id
      id: state.partsdetail.id,
      useconfirm: state.ruleForm.name,
      use_count: state.partsdetail.use_count,
      use_area: state.partsdetail.use_area,
      use_date: formatDate111(state.partsdetail.use_date),
      use_part_name: state.partsdetail.use_part_name,
      type: state.partsdetail.type,
      spec: state.partsdetail.spec,
      user: state.partsdetail.user,
      user_reason: state.partsdetail.user_remark,
      confirm_date: formatDate111(new Date()),
      handle: state.handle,
      flag: "confirm",
      use_procline: state.partsdetail.use_procline,
    },
  }).then((res: any) => {
    console.log("更新外修明细返回值");
    console.log(res);

    ElMessage.success({
      message: res.data,
      type: "success",
    });

    inituserecord("other");

    closeDialog();
  }).catch((err: any) => {
    closeDialog();
    ElMessage.warning({
      message: "错误",
      type: "warning",
    });
  })
}

// 关闭弹窗
// setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试

// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {
  state.ruleForm.name = "";
  state.partsdetail=[]
  state.ruleForm.name = "";
};

</script>
