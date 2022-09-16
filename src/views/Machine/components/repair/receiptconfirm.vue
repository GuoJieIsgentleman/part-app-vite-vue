<template>
  <div class="system-menu-container">
    <el-dialog title="收货确认信息" v-model="state.isShowDialog" width="769px" :destroy-on-close="true">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="类型">
              <el-input v-model="state.partsdetail.type" clearable disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="型号">
              <el-input disabled v-model="state.partsdetail.spec" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="名称">
              <el-input disabled v-model="state.partsdetail.use_part_name" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="数量">
              <el-input disabled v-model="state.partsdetail.use_count" clearable></el-input>
            </el-form-item>
          </el-col>

       
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="搁置区域">
           
                <el-row>
                  <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="8" :xl="12">
                    <el-select v-model="state.floor" filterable placeholder="存放楼层" clearable>
                      <el-option v-for="item in state.floors" :key="item['value']" :label="item['label']"
                        :value="item['value']">
                      </el-option>
                    </el-select>
                  </el-col>
                  <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="8" :xl="12">
                    <el-select v-model="state.shelf" filterable placeholder="存放架编号" clearable>
                      <el-option v-for="item in state.shelfs" :key="item['value']" :label="item['label']"
                        :value="item['value']">
                      </el-option>
                    </el-select>
                  </el-col>
                  <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="8" :xl="12">
                    <el-select v-model="state.num" filterable placeholder="存放位置编号" clearable>
                      <el-option v-for="item in 5" :key="item" :label="item" :value="item">
                        {{ item }}
                      </el-option>
                    </el-select>
                  </el-col>

                  <el-col class="mb20" :xs="24" :sm="18" :md="18" :lg="18" :xl="18">
                   {{state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + '-' + state.num}}
                  </el-col>
                </el-row>
             
           
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="收货人">
              <el-input v-model="state.ruleForm.name" placeholder="收货人" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit()" :loading="state.issave" size="small">确定</el-button>
        </span></template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import {
  reactive,
  toRefs,
  inject,
  onMounted,
  onUnmounted,
} from "vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";
import { ElMessage } from "element-plus";
import { Session } from "/@/utils/storage";

const state = reactive({
  
  num: '',
  shelfArea: '',
  floor: '',
  floors: [{
    value: "方镀三线二楼",
    label: "方镀三线二楼",
  },
  {
    value: "圆镀四线二楼",
    label: "圆镀四线二楼",
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
  }],
  shelf: '',
  shelfs: [
    {
      value: "1号架",
      label: "1号架",
    },
    {
      value: "2号架",
      label: "2号架",
    },
    {
      value: "3号架",
      label: "3号架",
    },
    {
      value: "4号架",
      label: "4号架",
    },
    {
      value: "5号架",
      label: "5号架",
    },
    {
      value: "6号架",
      label: "6号架",
    },
    {
      value: "7号架",
      label: "7号架",
    },
    {
      value: "8号架",
      label: "8号架",
    },
    {
      value: "9号架",
      label: "9号架",
    },
    {
      value: "10号架",
      label: "10号架",
    },
    {
      value: "11号架",
      label: "11号架",
    },
    {
      value: "12号架",
      label: "12号架",
    },
    {
      value: "13号架",
      label: "13号架",
    },
    {
      value: "14号架",
      label: "14号架",
    },
    {
      value: "15号架",
      label: "15号架",
    },
  ],
  issave: false,
  isShowDialog: false,
  ruleForm: {
    name: "",
    remark: "",
    areaArr: [],
    area: "",

    temporary_area: "",
  },
  confirmvalue: "",
  partsdetail: [] as any,
});


// 打开弹窗
const openDialog = (row?: any) => {
  console.log("rowobjec");
  console.log(row);
  state.partsdetail = row;
  state.isShowDialog = true;
};
defineExpose({ openDialog })
// 关闭弹窗
const closeDialog = (row?: object) => {
  state.isShowDialog = false;
  initForm()
};
// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增

//确认提交
const initrepair: any = inject("initrepair");
const onSubmit = () => {
  let tempStr = state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + "-" + state.num

  if(tempStr==='-'){
    ElMessage.warning({
      message: "请输入搁置区域",
      type: "warning",
    });
    return;
  }


  if ( state.ruleForm.name == '') {
    ElMessage.warning({
      message: "请重新输入",
      type: "warning",
    });
    return;
  }
  if (state.partsdetail.applicant == "") {
    ElMessage.warning({
      message: "申请人未确认不能确认",
      type: "warning",
    });
    return;
  }

  //更新确认人

  service.post("/updateMachine_repair", {

    //外修列表的id 不是parts 的id
    username:Session.get("userInfo").userName,
    id: state.partsdetail.id,
    use_count: state.partsdetail.use_count,
    use_area: state.partsdetail.use_area,
    use_date: formatDate111(state.partsdetail.use_date),
    use_part_name: state.partsdetail.use_part_name,
    use_reason: state.partsdetail.use_reason,
    type: state.partsdetail.type,
    spec: state.partsdetail.spec,
    new_area: tempStr,
    applicant: state.partsdetail.applicant,
    receipt:state.ruleForm.name ,
    receiptdate: formatDate111(new Date())
  }).then((res: any) => {
    ElMessage.success({
      message: res.data,
      type: "success",
    });
    initrepair("other");

    closeDialog();
  }).catch((err: any) => {
    ElMessage.warning({
      message: "错误",
      type: "warning",
    });
    initrepair("other");

    closeDialog();
  })

}


// setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试


const initForm = () => {
  state.ruleForm.name = "";
  state.ruleForm.area = ''
};



</script>
