<template>
  <div class="system-menu-container">
    <el-dialog title="报废确认信息班长" v-model="isShowDialog" width="769px" :destroy-on-close="true">
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
            <el-form-item label="使用部位">
              <el-input disabled v-model="partsdetail.site_use" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="报废数量">
              <el-input disabled v-model="partsdetail.use_count" clearable></el-input>
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
            <el-form-item label="备注">
              <el-input v-model="ruleForm.remark" clearable></el-input>
            </el-form-item>
          </el-col>


          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="ruleForm.name" placeholder="确认人" clearable></el-input>
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
import {
  reactive,
  toRefs,

  inject,
  onMounted,
  onUnmounted,
} from "vue";

import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";

import { ElMessage } from "element-plus";
import { getElectronArea, getMachineArea, ListItem, typeOption } from "/@/hooks/getHgInfo";
export default {
  setup() {
    const state = reactive({
      issave: false,
      isShowDialog: false,
      ruleForm: {
        deal_with_type: "",
        typeOption: [{ value: '报废', label: '报废' }],
        name: "",
        remark: "",
        areaArr: [] as Array<ListItem>,
        area: "",
      },
      confirmvalue: "",
      partsdetail: [] as any,
    });

    //初始化 产线 区域
    onMounted(async () => {
      state.ruleForm.areaArr = await getMachineArea()
    });
    // 打开弹窗
    const openDialog = async (row?: any) => {

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
    const initscrap: any = inject("initscrap");

    const onSubmit = (v: any) => {
      if (v == "") {
        ElMessage.warning({
          message: "请重新输入",
          type: "warning",
        });
      } else if (state.partsdetail.applyformconfirm == "") {
        ElMessage.warning({
          message: "报废申请人员未确认",
          type: "warning",
        });
      } else {
        //更新确认人

        service.post("/hg_updateMachineScrap", {
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
          use_date: state.partsdetail.use_date,
          useconfirm: state.ruleForm.name,
          useconfirmdate: formatDate111(new Date()),
          use_procline: state.partsdetail.use_procline,
          remark: state.ruleForm.remark,
          deal_with_type: state.ruleForm.deal_with_type,
          flag: "报废件确认信息",

        })
          .then((res) => {
            ElMessage.success({
              message: res.data,
              type: "success",
            });
            initscrap();
            closeDialog();
          })
          .catch((err) => {
            ElMessage.warning({
              message: err.data,
              type: "warning",
            });
          });
      }

    };

    const initForm = () => {
      state.ruleForm.name = "";
      // state.ruleForm.part_spec = "";
      // state.ruleForm.area = "";
      // state.ruleForm.balance = "";
      // state.ruleForm.original = "";
      // state.ruleForm.remark = "";

      // state.ruleForm.type = "";
      state.ruleForm.name = "";
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
