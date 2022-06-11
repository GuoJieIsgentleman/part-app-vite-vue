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
            <el-form-item label="名称">
              <el-input disabled v-model="partsdetail.use_part_name" clearable></el-input>
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
            <el-form-item label="处理类型">
              <el-select v-model="ruleForm.scrap" placeholder="处理类型">
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
            <el-form-item label="原搁置区域">
              <el-input disabled v-model="partsdetail.use_area" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="新搁置区域">
              <el-select
                v-model="ruleForm.area"
                placeholder="搁置区域"
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
            <el-form-item label="确认人">
              <el-input v-model="ruleForm.name" placeholder="班长名" clearable></el-input>
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
            value: "成套报废",
            label: "成套报废",
          },
          {
            value: "成套不报废",
            label: "成套不报废",
          },
        ],
        balance: 0,
        scrap: "",
        original: 0,
      },

      confirmvalue: "",
      partsdetail: [] as any,
    });

    const getbalance = async () => {
      let { data: balance } = await service.get("/gettooling_balance", {
        params: {
          area: state.partsdetail.use_area,
          type: state.partsdetail.type,
          spec: state.partsdetail.spec,
          part_name: state.partsdetail.use_part_name,
        },
      });

      if (balance.length > 0) {
        state.ruleForm.balance = balance[0][4];
        state.ruleForm.original = balance[0][5];
      }
    };

    //初始化 产线 区域
    onMounted(async () => {
      let { data: res } = await service.get("/gettooling_usearea");

      state.ruleForm.areaArr = res.map((item: any) => {
        return {
          value: item[0],
          label: item[0],
        };
      });
    });
    // 打开弹窗
    const openDialog = async (row?: any) => {
      console.log("----row---");
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

    //确认提交
    const inittooling_maintenance: any = inject("inittooling_maintenance");
    const onSubmit = (v: any) => {
      if (v == "") {
        ElMessage.warning({
          message: "请重新输入",
          type: "warning",
        });
      } else if (state.partsdetail.maintenanceman == "") {
        ElMessage.warning({
          message: "保养人未确认",
          type: "warning",
        });
      } else if (state.ruleForm.scrap == "不报废" && state.ruleForm.area == "") {
        ElMessage.warning({
          message: "最新搁置区域未填写",
          type: "warning",
        });
      } else {
        //更新确认人

        service
          .get("/updatetooling_maintenance", {
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
              new_area: state.ruleForm.area,
              maintenanceman: state.partsdetail.maintenanceman,
              maintenance_date: state.partsdetail.maintenance_date,
              scrap: state.ruleForm.scrap,
              flag: state.partsdetail.remark,
              user: state.partsdetail.user,
              use_procline: state.partsdetail.use_procline,
              useconfirmdate: formatDate111(new Date()),
            },
          })
          .then((res) => {
            ElMessage.success({
              message: res.data,
              type: "success",
            });
            inittooling_maintenance("all");
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
      state.ruleForm.area = "";
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
