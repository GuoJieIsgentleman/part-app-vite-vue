<template>
  <div class="system-menu-container">
    <el-dialog title="外修班长确认信息" v-model="isShowDialog" width="769px" :destroy-on-close="true">
      <el-form :model="ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="类型">
              <el-input v-model="partsdetail.type" clearable disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="型号">
              <el-input disabled v-model="partsdetail.spec" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用部位">
              <el-input disabled v-model="partsdetail.site_use" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存数量">
              <el-input disabled v-model="ruleForm.balance" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input disabled v-model="ruleForm.original" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="外修数量">
              <el-input disabled v-model="partsdetail.use_count" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="名称">
              <el-input disabled v-model="partsdetail.use_part_name" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原搁置区域">
              <el-input disabled v-model="partsdetail.use_area" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="新搁置区域">
              <el-select v-model="ruleForm.area" placeholder="最新搁置区域">
                <el-option v-for="item in ruleForm.areaArrs" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="处理类型">
              <el-select v-model="ruleForm.deal_with_type" placeholder="处理类型" clearable>
                <el-option v-for="item in ruleForm.typeOption" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="ruleForm.name" placeholder="班长确认" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备注">
              <el-input v-model="ruleForm.remark" placeholder="备注" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="issave" size="small">确定</el-button>
        </span></template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { reactive, toRefs, inject, onMounted } from "vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";

import { ElMessage } from "element-plus";
import { getMachineArea, getMachineBalance, ListItem, typeOption } from "/@/hooks/getHgInfo";
export default {
  setup() {
    const state = reactive({
      issave: false,
      isShowDialog: false,
      ruleForm: {
        machine_part_name: "",

        name: "",
        remark: "",
        areaArrs: [] as Array<ListItem>,
        area: "",
        typeOption: typeOption,
        balance: 0,
        deal_with_type: "",
        original: 0,

      },
      confirmvalue: "",
      partsdetail: [] as any,
    });

    //初始化 产线 区域
    onMounted(async () => {
      state.ruleForm.areaArrs = await getMachineArea()
    });
    // 打开弹窗
    const openDialog = async (row?: any) => {
      console.log("rowobjec");
      console.log(row);
      state.partsdetail = row;

      state.isShowDialog = true;

      getbalance();
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

    const getbalance = async () => {
      let temp = await getMachineBalance(state.partsdetail.area, state.partsdetail.type, state.partsdetail.spec, state.partsdetail.part_name)

      state.ruleForm.balance = temp[0][0]
      state.ruleForm.original = temp[0][1]


    }

    //确认提交
    const initrepair: any = inject("initrepair");
    const onSubmit = () => {
      if (state.ruleForm.name == "") {
        ElMessage.warning({
          message: "请重新输入",
          type: "warning",
        });
        return
      }

      //更新确认人
      service.post("/hg_updateMachineRepair", {

        //保养列表的id 不是parts 的id
        id: state.partsdetail.id,
        user: state.partsdetail.user,
        use_area: state.partsdetail.use_area,
        type: state.partsdetail.type,
        spec: state.partsdetail.spec,
        use_part_name: state.partsdetail.use_part_name,
        site_use: state.partsdetail.site_use,
        use_count: state.partsdetail.use_count,
        use_reason: state.partsdetail.use_reason,
        use_date: formatDate111(state.partsdetail.use_date),
        useconfirm: state.ruleForm.name,
        useconfirmdate: formatDate111(new Date()),
        new_area: state.ruleForm.area,
        use_procline: state.partsdetail.use_procline,
        remark: state.ruleForm.remark,
        deal_with_type: state.ruleForm.deal_with_type

      })
        .then((res) => {
          console.log("返回成功");
          ElMessage.success({
            message: res.data,
            type: "success",
          });
          closeDialog();
          initrepair("other");
        })
        .catch((err) => {
          ElMessage.warning({
            message: err.data,
            type: "warning",
          });
          closeDialog();
        });


    };
    // 表单初始化，方法：`resetFields()` 无法使用
    const initForm = () => {
      state.ruleForm.name = "";

      state.ruleForm.area = "";
      state.ruleForm.balance = 0
      state.ruleForm.original = 0;
      state.ruleForm.remark = "";


      state.ruleForm.name = "";
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
