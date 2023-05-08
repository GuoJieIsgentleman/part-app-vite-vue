<template>
  <div class="system-menu-container">
    <el-dialog title="修改密码" v-model="state.isShowDialog" width="769px">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="账号">
              <el-input v-model="state.userlist.username" disabled clearable> </el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="密码">
              <el-input v-model="state.ruleForm.password" placeholder="密码" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色">
              <el-select v-model="state.ruleForm.role" placeholder="选择角色">
                <el-option v-for="item in state.ruleForm.rolelist" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="区域授权">
              <el-select v-model="state.ruleForm.value1" multiple placeholder="Select" style="width: 240px">
                <el-option v-for="item in state.ruleForm.Responsible_area" :key="item.value" :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="巡检区域授权">
              <el-select v-model="state.ruleForm.inspect_value" multiple placeholder="Select" style="width: 240px">
                <el-option v-for="item in state.ruleForm.inspect_areas" :key="item.value" :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" size="small">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs, onMounted, inject } from "vue";
import IconSelector from "/@/components/iconSelector/index.vue";
import { useI18n } from "vue-i18n";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";
import { arrayBuffer } from "stream/consumers";
// import Message from "element-plus/lib/el-message/src/message";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

const { t } = useI18n();
const state = reactive({
  userlist: [] as any,
  isShowDialog: false,

  ruleForm: {
    inspect_value: "" as any,
    value1: "" as any,
    Responsible_area: [
      {
        value: "值班室一楼",
        label: "值班室一楼",
      },
      {
        value: "值班室二楼",
        label: "值班室二楼",
      },
      {
        value: "方镀三线一楼",
        label: "方镀三线一楼",
      },
      {
        value: "方镀三线二楼",
        label: "方镀三线二楼",
      },
      {
        value: "圆镀四线一楼",
        label: "圆镀四线一楼",
      },
      {
        value: "圆镀四线二楼",
        label: "圆镀四线二楼",
      },
      {
        value: "南污水南库",
        label: "南污水南库",
      },
      {
        value: "南污水北库",
        label: "南污水北库",
      },
      {
        value: "锌锭库一层",
        label: "锌锭库一层",
      },
      {
        value: "锌锭库二层",
        label: "锌锭库二层",
      },
      {
        value: "方管库一层",
        label: "方管库一层",
      },
      {
        value: "方管库二层",
        label: "方管库二层",
      },
    ],
    username: "",
    password: "",
    rolelist: [],
    role: "",

    inspect_areas: [
      {
        value: "值班室一楼",
        label: "值班室一楼",
      },
      {
        value: "值班室二楼",
        label: "值班室二楼",
      },
      {
        value: "方镀三线一楼",
        label: "方镀三线一楼",
      },
      {
        value: "方镀三线二楼",
        label: "方镀三线二楼",
      },
      {
        value: "圆镀四线一楼",
        label: "圆镀四线一楼",
      },
      {
        value: "圆镀四线二楼",
        label: "圆镀四线二楼",
      },
      {
        value: "南污水南库",
        label: "南污水南库",
      },
      {
        value: "南污水北库",
        label: "南污水北库",
      },
      {
        value: "锌锭库一层",
        label: "锌锭库一层",
      },
      {
        value: "锌锭库二层",
        label: "锌锭库二层",
      },
      {
        value: "方管库一层",
        label: "方管库一层",
      },
      {
        value: "方管库二层",
        label: "方管库二层",
      },
    ]
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
const openDialog = (row: any) => {

  console.log('row  子组件', row);
  state.isShowDialog = true;
  state.userlist = row;

  state.ruleForm.inspect_value = eval(row.inspect_area)



  state.ruleForm.value1 = eval(row.area)

  state.ruleForm.role = state.userlist.role;
  state.ruleForm.password = state.userlist.passwd

};

defineExpose({ openDialog })


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

  console.log('提交 state.ruleForm.inspect_value', state.ruleForm.inspect_value);



  //更新用户

  service
    .get("/hg_updateuser", {
      params: {
        username: state.userlist.username,
        password: state.ruleForm.password,
        role: state.ruleForm.role,
        area: state.ruleForm.value1.length === 0 ? "" : JSON.stringify(state.ruleForm.value1),
        inspect_area: state.ruleForm.inspect_value.length === 0 ? "" : JSON.stringify(state.ruleForm.inspect_value),
        flag: "编辑",
      },
    })
    .then((res: any) => {
      ElMessage.success(res.data);
      inituseData();
      closeDialog();
    });
  // 关闭弹窗

  // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
};
// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {


};

</script>
