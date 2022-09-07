<template>
  <div class="system-menu-container">
    <el-dialog
      title="外修班长确认信息"
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
            <el-form-item label="保养数量">
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
              <el-select
                v-model="ruleForm.area"
                placeholder="最新搁置区域"
                :disabled="ruleForm.scrap == '报废' ? true : false"
              >
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
            <el-form-item label="是否报废">
              <el-select v-model="ruleForm.scrap" placeholder="是否报废" clearable>
                <el-option
                  v-for="item in ruleForm.scrapOption"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="成套1">
              <el-input
                v-model="ruleForm.machine_part_name"
                placeholder="是否成套设备，请填写成套名称"
                clearable0
                :disabled="
                  ruleForm.scrap != '成套报废' && ruleForm.scrap != '成套不报废'
                    ? true
                    : false
                "
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input
                v-model="ruleForm.name"
                placeholder="班长确认"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备注">
              <el-input v-model="ruleForm.remark" placeholder="备注" clearable></el-input>
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
import { reactive, toRefs, defineEmits, defineExpose, inject, onMounted } from "vue";
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
        machine_part_name: "",

        name: "",
        remark: "",
        areaArr: [],
        area: "",

        scrapOption: [
          {
            value: "报废",
            label: "报废",
          },
          {
            value: "不报废",
            label: "不报废",
          },
          {
            value: "成套不报废",
            label: "成套不报废",
          },
          {
            value: "成套报废",
            label: "成套报废",
          },
        ],
        balance: 0,
        scrap: "",
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
      console.log("areaArr");
      console.log(state.ruleForm.areaArr);
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
      if (balance.length >= 1) {
        state.ruleForm.balance = balance[0][4];
        state.ruleForm.original = balance[0][5];
      }
    };
    //确认提交
    const initrepair: any = inject("initrepair");
    const onSubmit = (v: any) => {
      if (v == "") {
        ElMessage.warning({
          message: "请重新输入",
          type: "warning",
        });
      } else if (state.partsdetail.scrap == "") {
        ElMessage.warning({
          message: "请选择是否报废",
          type: "warning",
        });
      } else if (state.partsdetail.applicant == "" || state.partsdetail.tryout == "") {
        ElMessage.warning({
          message: "申请人或者试机人未确认",
          type: "warning",
        });
      } else {
        //更新确认人
        service
          .get("/updaterepair", {
            params: {
              //保养列表的id 不是parts 的id
              id: state.partsdetail.id,
              useconfirm: v,
              use_count: state.partsdetail.use_count,
              use_area: state.partsdetail.use_area,
              use_date: formatDate111(state.partsdetail.use_date),
              use_part_name: state.partsdetail.use_part_name,
              use_reason: state.partsdetail.use_reason,
              type: state.partsdetail.type,
              spec: state.partsdetail.spec,
              new_area: state.ruleForm.area,
              applicant: state.partsdetail.applicant,
              receipt: state.partsdetail.receipt,
              tryout: state.partsdetail.tryout,
              scrap: state.ruleForm.scrap,
              user: state.partsdetail.user,
              use_procline: state.partsdetail.use_procline,
              useconfirmdate: formatDate111(new Date()),
              flag: state.partsdetail.remark,
              machine_part_name: state.ruleForm.machine_part_name,
            },
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
