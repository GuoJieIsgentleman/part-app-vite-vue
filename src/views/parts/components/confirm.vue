<template>
  <div class="system-menu-container">
    <el-dialog title="确认信息" v-model="isShowDialog" width="300px">
      <el-form :model="ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="ruleForm.name" placeholder="班长名" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="搁置区域">
              <el-select v-model="ruleForm.area" placeholder="搁置区域">
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
      },
      confirmvalue: "",
      partsdetail: [] as any,
    });

    //初始化 产线 区域
    onMounted(async () => {});
    // 打开弹窗
    const openDialog = async (row?: any) => {
      console.log("rowobjec");
      console.log(row);
      state.partsdetail = row;

      state.isShowDialog = true;
      let { data: res } = await service.get("/api/getarea");

      state.ruleForm.areaArr = res.map((item: any) => {
        return item[0];
      });
      console.log("areaArr");
      console.log(state.ruleForm.areaArr);
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
    const initmaintenance: any = inject("initmaintenance");
    const onSubmit = async (v: any) => {
      if (v == "") {
        alert("请重新输入");
      } else {
        //更新确认人

        let { data: res } = await service.get("/api/updatemaintenance", {
          params: {
            id: state.partsdetail.id,
            useconfirm: v,
          },
        });

        console.log("更新保养明细返回值");
        console.log(res);

        initmaintenance();
        closeDialog();
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
