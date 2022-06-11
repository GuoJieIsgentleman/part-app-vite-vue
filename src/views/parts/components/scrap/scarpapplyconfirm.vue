<template>
  <div class="system-menu-container">
    <el-dialog
      title="补件申请"
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
            <el-form-item label="报废数量">
              <el-input disabled v-model="partsdetail.use_count" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="补件情况">
              <el-select
                v-model="selectOption"
                placeholder="请选择"
                @change="sendselectOption(selectOption)"
              >
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label == '' ? '' : item.label"
                  :value="item.value == '' ? '' : item.value"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="补件数量">
              <el-input
                v-model="add_count"
                clearable
                :placeholder="
                  selectOption == '补'
                    ? '到货数量'
                    : selectOption == '不补'
                    ? '不补'
                    : '请选择是否补件'
                "
                :disabled="selectOption == '补' ? false : true"
              ></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="ruleForm.name" placeholder="确认人" clearable></el-input>
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
      selectOption: "",
      add_count: 0,

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

      options: [
        {
          value: "补",
          label: "补",
        },
        {
          value: "不补",
          label: "不补",
        },
      ],
    });

    const sendselectOption = (v?: any) => {};

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
      if (v == "" || state.selectOption == "") {
        ElMessage.warning({
          message: "请重新输入(补件情况)",

          type: "warning",
        });
      } else if (
        state.partsdetail.applyformconfirm == "" ||
        state.partsdetail.scrapconfirm == ""
      ) {
        ElMessage.warning({
          message: "报废人员未确认",
          type: "warning",
        });
      } else if (state.selectOption == "补" && state.add_count < 1) {
        ElMessage.warning({
          message: "件数至少为1件",
          type: "warning",
        });
      } else {
        //更新确认人

        let res = service
          .get("/updatescrap", {
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
              scrapconfirm: state.partsdetail.scrapconfirm,
              selectOption: state.selectOption,
              selectOptiondate: state.partsdetail.selectOptiondate,
              applyformconfirm: state.partsdetail.applyformconfirm,
              applicantman: v,
              useconfirm: state.partsdetail.useconfirm,
              received: state.partsdetail.received,
              new_area: state.partsdetail.new_area,
              add_count: state.add_count,
              flag: "补件申请人",
            },
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
    onUnmounted(initForm);
    return {
      openDialog,
      closeDialog,
      onCancel,
      onSubmit,
      ...toRefs(state),

      sendselectOption,
    };
  },
};
</script>
