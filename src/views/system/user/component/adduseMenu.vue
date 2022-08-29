<template>
  <div class="system-menu-container">
    <el-dialog title="新增菜单" v-model="state.isShowDialog" width="500px">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="用户名">
              <el-input v-model="state.ruleForm.username" placeholder="用户名" clearable>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="密码">
              <el-input v-model="state.ruleForm.password" placeholder="密码" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色">
              <el-select v-model="state.ruleForm.role" placeholder="更改角色">
                <el-option v-for="item in state.ruleForm.rolelist" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" size="small">新 增</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs, onMounted, inject } from "vue";
import IconSelector from "/@/components/iconSelector/index.vue";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

const state = reactive({
  isShowDialog: false,
  ruleForm: {
    username: "",
    password: "",
    role: "",
    rolelist: [],
  },
});
onMounted(() => {
  //获取角色
  service.get("/getrolelist").then((res: any) => {
    state.ruleForm.rolelist = res.data.map((item: any) => {
      return {
        value: item[2],
        label: item[1],
      };
    });

  });



});
// 打开弹窗
const openDialog = (row?: object) => {
  console.log(row);
  state.isShowDialog = true;
};


defineExpose({openDialog})


// 关闭弹窗
const closeDialog = (row?: object) => {
  console.log(row);
  state.isShowDialog = false;
};

// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增

const inituseData: any = inject("inituseData");
const onSubmit = () => {
  //检测 并且提交
  service
    .get("adduser", {
      params: {
        username: state.ruleForm.username,
        password: state.ruleForm.password,
        role: state.ruleForm.role,
      },
    })
    .then((res:any) => {
      console.log("onSubmit回复");
      console.log(res);
      if (res.data == "添加成功") {
        ElMessage.success("添加成功");
      } else {
        ElMessage.warning(res.data);
      }

      inituseData();
    });

  console.log(state.ruleForm); // 数据，请注意需要转换的类型
  closeDialog(); // 关闭弹窗
  // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
};
// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {

};

</script>
