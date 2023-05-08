<template>
  <div>
    <el-dialog title="新增菜单" v-model="state.isShowDialog" width="769px" :destroy-on-close="true" @close="closeDialog">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用人">
              <el-input v-model="state.userinput" placeholder disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用产线">
              <el-select v-model="state.use_proline_value" placeholder="使用产线">
                <el-option v-for="item in state.use_proline_options" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用区域">
              <el-select v-model="state.ruleForm.select_area" key placeholder="" @change="gettype">
                <el-option v-for="item in state.ruleForm.userarea" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>

            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件类型">
              <el-select v-model="state.ruleForm.select_type" placeholder="" @change="getpartname">
                <el-option v-for="item in state.ruleForm.usetype" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>

            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件名称">
              <el-select v-model="state.ruleForm.select_partName" placeholder="" @change="getspesc">
                <el-option v-for="item in state.ruleForm.part_name" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件型号">
              <el-select v-model="state.ruleForm.select_spec" placeholder="" @change="getbalance">
                <el-option v-for="item in state.ruleForm.usespesc" :key="item['value']" :label="item['label']"
                  :value="item['value']">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用部位">
              <el-input disabled v-model="state.ruleForm.site_use" placeholder clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存数量">
              <el-input disabled v-model="state.ruleForm.balance" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input disabled v-model="state.ruleForm.original" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用数量">
              <el-input placeholder="请输入数量" v-model="state.ruleForm.use_count">
                <template #prepend>区域库存为:{{ state.ruleForm.balance }}</template>
              </el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原因">
              <el-input placeholder="原因" v-model="state.ruleForm.reason"> </el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="替换备件处理方式">

              <el-select v-model="state.handle" placeholder="请选择">
                <el-option v-for="item in state.options" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用时间">
              <el-input disabled v-model="state.ruleForm.use_date"></el-input>
            </el-form-item>
          </el-col>

        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog" size="small">取 消</el-button>

          <el-button type="primary" @click="onSubmit" :loading="state.issave" size="small">保存</el-button>
        </span></template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup >
import { reactive, inject } from "vue";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";

import { Session } from "/@/utils/storage";
import { formatDate111 } from "/@/utils/formatTime";
import { use_proline_options, options, ListItem, getMachinetype, getMachinePartName, getMachineSpesc, getMachineSiteUse, getMachineArea, getMachineBalance } from '/@/hooks/getHgInfo'


const state = reactive({
  flag: true,
  userinput: Session.get("userInfo").userName,
  options: options,
  use_proline_options: [] as Array<ListItem>,
  use_proline_value: "",
  handle: "",
  value: "",
  issave: false,
  isShowDialog: false,
  ruleForm: {
    site_use: '',
    original: 0,
    select_area: "",
    select_spec: '',
    select_type: '',
    select_partName: '',
    reason: "",
    balance: 0,
    userarea: [] as Array<ListItem>,
    usetype: [] as Array<ListItem>,
    usespesc: [] as Array<ListItem>,
    part_name: [] as Array<ListItem>,
    user: "",
    use_area: "",
    use_part_name: "",
    use_count: 0,
    user_remark: "",
    use_date: "",
  },
});

const gettype = async () => {
  state.ruleForm.usetype = await getMachinetype(state.ruleForm.select_area)
}

const getpartname = async () => {
  state.ruleForm.part_name = await getMachinePartName(state.ruleForm.select_area, state.ruleForm.select_type)
}

const getspesc = async () => {
  state.ruleForm.usespesc = await getMachineSpesc(state.ruleForm.select_partName, state.ruleForm.select_area, state.ruleForm.select_type)
}

const getbalance = async () => {
  let temp = await getMachineBalance(state.ruleForm.select_area, state.ruleForm.select_type, state.ruleForm.select_spec, state.ruleForm.select_partName)

  state.ruleForm.balance = temp[0][0]
  state.ruleForm.original = temp[0][1]


  //获取使用部位

  let temp1 = (await getMachineSiteUse(state.ruleForm.select_area, state.ruleForm.select_type, state.ruleForm.select_spec, state.ruleForm.select_partName))
  console.log('site_use', temp1);

  state.ruleForm.site_use = temp1[0]
}


// 打开弹窗

const openDialog = async () => {
  state.isShowDialog = true;

  state.ruleForm.userarea = await getMachineArea()
  state.use_proline_options = await use_proline_options()
  state.ruleForm.use_date = formatDate111(new Date())

};
defineExpose({ openDialog });
// 关闭弹窗
const closeDialog = (row?: object) => {
  initForm();
  state.isShowDialog = false;
};

// 新增

const inituserecord: any = inject("inituserecord");
const onSubmit = () => {
  //验证处理
  if (state.ruleForm.use_count > state.ruleForm.balance || state.ruleForm.use_count <= 0) {
    ElMessage.warning("请重新输入");
    state.ruleForm.use_count = 0;
    return
  }




  //提交 保存  做非空验证
  state.issave = !state.issave;
  service.post("/hg_addMachineUserecord", {
    user: state.userinput,
    use_area: state.ruleForm.select_area,
    type: state.ruleForm.select_type,
    spec: state.ruleForm.select_spec,
    use_part_name: state.ruleForm.select_partName,
    use_count: state.ruleForm.use_count,
    use_reason: state.ruleForm.reason,
    use_date: state.ruleForm.use_date,
    use_procline: state.use_proline_value,
    handle: state.handle,
    site_use: state.ruleForm.site_use,
    flag: "add"
  }).then(res => {
    console.log('data', res);

    ElMessage({
      type: 'success',
      message: res.data
    })
    state.issave = !state.issave;
    inituserecord();
    closeDialog();
  }).catch(err => {

    console.log(err);
    ElMessage({
      type: 'error',
      message: err
    })

    state.issave = !state.issave;
    inituserecord();
    closeDialog();
  })



};

const initForm = () => {
  state.ruleForm.user = "";
  state.ruleForm.use_area = "";
  state.ruleForm.use_part_name = "";
  state.ruleForm.use_count = 0;
  state.ruleForm.user_remark = "";
  (state.value = ""),
    (state.ruleForm.select_area = ""),
    (state.ruleForm.select_partName = ""),
    (state.ruleForm.select_spec = ""),
    (state.ruleForm.select_type = ""),
    (state.ruleForm.userarea = []),
    (state.ruleForm.usetype = []),
    (state.ruleForm.usespesc = []),
    (state.ruleForm.part_name = []);
  state.ruleForm.use_date = "";
  state.ruleForm.balance = 0;
  state.ruleForm.reason = "";
};

</script>
