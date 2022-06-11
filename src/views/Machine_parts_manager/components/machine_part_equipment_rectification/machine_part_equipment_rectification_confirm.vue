<template>
  <div class="system-menu-container">
    <el-dialog
      title="确认信息"
      v-model="isShowDialog"
      width="769px"
      :destroy-on-close="true"
    >
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
            <el-form-item label="名称">
              <el-input disabled v-model="partsdetail.use_part_name" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存数量">
              <el-input
                disabled
                v-model="ruleForm.balance"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input
                disabled
                v-model="ruleForm.original"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用数量">
              <el-input disabled v-model="partsdetail.use_count" clearable></el-input>
            </el-form-item>
          </el-col>
          <!-- <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="补件数量">
              <el-input disabled v-model="partsdetail.received" clearable></el-input>
            </el-form-item>
          </el-col> -->
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="搁置区域">
              <el-select v-model="ruleForm.area" placeholder="最新搁置区域">
                <el-option
                  v-for="item in ruleForm.areaArr"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="ruleForm.name" placeholder="确认人" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="30">
          <el-col>
            <el-form-item label="备注">
              <el-input v-model="ruleForm.remark" width="300px" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
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
import {
  reactive,
  toRefs,
  defineEmits,
  defineExpose,
  inject,
  onMounted,
  onUnmounted,
} from "vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";

import { ElMessage } from "element-plus";
export default {
  setup() {
    const state = reactive({
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
      let { data: res } = await service.get("/getmachine_part_usearea");

      state.ruleForm.areaArr = res.map((item: any) => {
        return {
          value: item[0],
          label: item[0],
        };
      });
      console.log("areaArr");
      console.log(state.ruleForm.areaArr);
    });
    const getbalance = async () => {
      let { data: balance } = await service.get("/getbalance", {
        params: {
          area: state.partsdetail.use_area,
          type: state.partsdetail.type,
          spec: state.partsdetail.spec,
          part_name: state.partsdetail.use_part_name,
        },
      });

      console.log("balance");
      console.log(balance);
      if (balance.length > 0) {
        state.ruleForm.balance = balance[0][4];
        state.ruleForm.original = balance[0][5];
      }
    };
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
      initForm();
    };
    // 取消
    const onCancel = () => {
      closeDialog();
      initForm();
    };
    // 新增

    //确认提交
    const initmachine_part_equipment_rectification: any = inject(
      "initmachine_part_equipment_rectification"
    );
    const onSubmit = (v: any) => {
      if (v == "") {
        ElMessage.warning({
          message: "请重新输入",
          type: "warning",
        });
      } else if (state.ruleForm.name == "") {
        ElMessage.warning({
          message: "信息未确认",
          type: "warning",
        });
      } else {
        //更新确认人

        let res = service
          .get("/updateMachine_part_equipment_rectification", {
            params: {
              //保养列表的id 不是parts 的id
              id: state.partsdetail.id,
              user: state.partsdetail.user,
              use_area: state.partsdetail.use_area,
              type: state.partsdetail.type,
              spec: state.partsdetail.spec,
              use_part_name: state.partsdetail.use_part_name,
              use_count: state.partsdetail.use_count,
              use_reason: state.partsdetail.use_reason,
              use_date: state.partsdetail.use_date,
              useconfirm: v,
              use_procline: state.partsdetail.use_procline,
              new_area: state.ruleForm.area,
              useconfirmdate: formatDate111(new Date()),
              remark: state.ruleForm.remark,
              flag: "设备整改确认",
              flag1: state.partsdetail.remark,
            },
          })
          .then((res) => {
            ElMessage.success({
              message: res.data,
              type: "success",
            });

            initmachine_part_equipment_rectification();
            closeDialog();
          })
          .catch((err) => {
            ElMessage.warning({
              message: err.data,
              type: "warning",
            });
          });
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
    onUnmounted(initForm);
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
