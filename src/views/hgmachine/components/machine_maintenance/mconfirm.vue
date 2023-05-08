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
            <el-form-item label="名称">
              <el-input disabled v-model="state.partsdetail.use_part_name" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="型号">
              <el-input disabled v-model="state.partsdetail.spec" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用部位">
              <el-input disabled v-model="state.partsdetail.site_use" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存数量">
              <el-input disabled v-model="state.ruleForm.balance" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input disabled v-model="state.ruleForm.original" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="保养数量">
              <el-input disabled v-model="state.partsdetail.use_count" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="处理类型">
              <el-select v-model="state.ruleForm.deal_with_type" placeholder="处理类型" @change="selectChange">
                <el-option v-for="item in state.ruleForm.typeOption" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原搁置区域">
              <el-input disabled v-model="state.partsdetail.use_area" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="新搁置区域" label-width="80">
              <el-select v-model="state.ruleForm.new_use_area" clearable placeholder="领用区域">
                <el-option v-for="item in state.ruleForm.areaArr" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="state.ruleForm.name" placeholder="班长名" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备注">
              <el-input v-model="state.ruleForm.remark" placeholder="备注" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="state.issave" size="small">确定</el-button>
        </span></template>
    </el-dialog>
  </div>
</template>


<script lang="ts" setup>
import {
  reactive,
  inject,
  onMounted,

} from "vue";

import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";

import { ElMessage } from "element-plus";
import { getMachineArea, getMachineBalance, ListItem, typeOption } from "/@/hooks/getHgInfo";

const state = reactive({

  num: '',
  issave: false,
  isShowDialog: false,
  ruleForm: {
    deal_with_type: '',
    machine_part_name: "",
    name: "",
    remark: "",
    areaArr: [] as Array<ListItem>,
    area: "",
    new_use_area: '',
    typeOption: typeOption,
    balance: 0,
    original: 0,
  },
  confirmvalue: "",
  partsdetail: [] as any,
});


const selectChange = (val: any) => {
  console.log('val', val);
  if (val == '报废') {

    state.num = ''
  }
}

const getbalance = async () => {

  let temp = await getMachineBalance(state.partsdetail.use_area, state.partsdetail.type, state.partsdetail.spec, state.partsdetail.use_part_name)

  state.ruleForm.balance = temp[0][0]
  state.ruleForm.original = temp[0][1]

};

//初始化 产线 区域
onMounted(async () => {


});
// 打开弹窗
const openDialog = async (row?: any) => {
  console.log("rowobjec");
  console.log(row);
  state.partsdetail = row;
  //获取库存
  getbalance()
  //获取产线
  state.ruleForm.areaArr = await getMachineArea()
  state.isShowDialog = true;

};

defineExpose({ openDialog })
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

const onSubmit = () => {
  if (state.ruleForm.new_use_area == '' || state.ruleForm.name == '') {
    ElMessage({
      type: 'warning',
      message: '请完善区域或者确认人'
    })
    return
  }
  //更新确认人
  service
    .post("/hg_updateMachineMaintenance", {

      //保养列表的id 不是parts 的id
      id: state.partsdetail.id,
      user: state.partsdetail.user,
      use_area: state.partsdetail.use_area,
      type: state.partsdetail.type,
      spec: state.partsdetail.spec,
      use_part_name: state.partsdetail.use_part_name,
      use_count: state.partsdetail.use_count,
      use_date: formatDate111(state.partsdetail.use_date),
      useconfirm: state.ruleForm.name,
      new_area: state.ruleForm.name,
      useconfirmdate: formatDate111(new Date()),
      use_procline: state.partsdetail.use_procline,
      deal_with_type: state.ruleForm.deal_with_type,
      flag: state.partsdetail.remark,
      site_use: state.partsdetail.site_use,
      remark: state.ruleForm.remark
    })
    .then((res) => {
      ElMessage.success({
        message: res.data,
        type: "success",
      });
      initmaintenance("all");
      closeDialog();
    })
    .catch((err) => {
      ElMessage.warning({
        message: err.data,
        type: "warning",
      });
      closeDialog();
    });
}



const initForm = () => {
  state.ruleForm.name = "";

  state.ruleForm.area = "";
  state.ruleForm.new_use_area = '';



};

</script>
