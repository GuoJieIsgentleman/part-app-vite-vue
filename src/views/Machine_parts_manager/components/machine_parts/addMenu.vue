<template>
  <div class="system-menu-container">
    <el-dialog title="成套备件添加" v-model="state.isShowDialog" width="769px">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="10">
          <el-col :span="6">
           <el-form-item label="备件图片">
            <el-upload
              class="avatar-uploader"
              ref="upload1"
              :on-change="imgpreivew"
              :auto-upload="false"
              :action="
                'http://61.185.74.251:5556/machine_part_uploadfile?imgid=' +
                state.ruleForm.id +
                '&&time1=' +
                new Date().getTime().toString() +
                '&&machine_part_name=' +
                state.ruleForm.machine_part_name
              "
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
            >
              <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
              <img
                v-if="state.ruleForm.imageUrl"
                :src="state.ruleForm.imageUrl"
                class="avatar"
              />

              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
            </el-form-item>
          </el-col>

        </el-row>
        <el-row :gutter="35">
          <!-- <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件编号">
              <el-input v-model="state.machine_part_id" placeholder clearable></el-input>
            </el-form-item>
          </el-col> -->

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="成套备件名称">
              <el-input
                v-model="state.ruleForm.machine_part_name"
                placeholder="'必填，每个成套的专有名称"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="单体类型">
              <el-select
                v-model="state.ruleForm.singlepart"
                filterable
                placeholder="单体类型"
                clearable
              >
                <el-option
                  v-for="item in state.singleparts"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件类型">
              <el-input v-model="state.ruleForm.type" placeholder clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="单体备件名称">
              <el-input
                v-model="state.ruleForm.part_name"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="单体备件规格">
              <el-input
                v-model="state.ruleForm.part_spec"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="搁置区域">
              <!-- <el-select
                v-model="state.ruleForm.part_area_value"
                filterable
                placeholder="备件区域"
                clearable
              >
                <el-option
                  v-for="item in state.ruleForm.userarea"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select> -->
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
            <el-form-item label="结存">
              <el-input v-model="state.ruleForm.balance" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input
                v-model="state.ruleForm.original"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="机械连接方式">
              <el-input
                v-model="state.ruleForm.connection"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备注">
              <el-input v-model="state.ruleForm.remark" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row> </el-form
      ><template #footer
        ><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="state.issave" size="small"
            >保存</el-button
          >
        </span></template
      >
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs, onUnmounted, onMounted, ref } from "vue";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";
import { compressAccurately } from "image-conversion";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

const state = reactive({
  
  num: '',
  shelfArea: '',
  floor: '',
  floors: [
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
        value: "圆镀四线一楼",
        label: "圆镀四线一楼",
      },
      {
        value: "南污水南库",
        label: "南污水南库",
      },{
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
  machine_part_id: "",
  singleparts: [
    {
      value: "机械",
      label: "机械",
    },
    {
      value: "电器",
      label: "电器",
    },
  ],
  issave: false,
  isShowDialog: false,
  ruleForm: {
    id: "",
    part_name: "",
    part_spec: "",
    area: "",
    balance: "",
    original: "",
    type: "",
    remark: "",
    userarea: [],
    part_area_value: "",
    imageUrl: "",
    machine_part_name: "",
    singlepart: "",
    connection: "",
  },
});

const getusearea = async () => {
  let { data: res } = await service.get(`/getmachine_part_usearea`);
  console.log(res);
  state.ruleForm.userarea = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
};

onMounted(getusearea);
// 打开弹窗
const openDialog = (row?: object) => {
  state.isShowDialog = true;
};

defineExpose({ openDialog });
// 关闭弹窗
const closeDialog = (row?: object) => {
  state.isShowDialog = false;
};
// 是否内嵌下拉改变
// const onSelectIframeChange = () => {
// 	if (state.ruleForm.meta.isIframe === 'true') {
// 		state.ruleForm.isLink = 'true';
// 	} else {
// 		state.ruleForm.isLink = '';
// 	}
// };
// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增

const upload1 = ref();
const onSubmit = () => {




  let tempStr = state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + "-" + state.num

  if(state.machine_part_id=='' || state.ruleForm.machine_part_name===''
  ||state.ruleForm.part_spec==='' ||state.ruleForm.part_name===''|| state.ruleForm.type==='')
  {
    ElMessage({type:'warning',message:'请完善成套备件信息'})
    return
  }
  if(state.ruleForm.balance===''){
    ElMessage({type:'warning',message:'请填写库存'})
    return
  }

  service
    .get("/addmachine_part", {
      params: {
        machine_part_id: state.machine_part_id,
        machine_part_name: state.ruleForm.machine_part_name,
        part_name: state.ruleForm.part_name,
        part_spec: state.ruleForm.part_spec,
        area: tempStr,
        balance: state.ruleForm.balance,
        original: state.ruleForm.balance,
        remark: state.ruleForm.remark,
        type: state.ruleForm.type,
        type1: state.ruleForm.singlepart,
        connection: state.ruleForm.connection,
      },
    })
    .then((res) => {
      ElMessage({
        type: "success",
        message: res.data,
      });
      state.ruleForm.id = res.data.id;
      //调用上传图片的方法
    
      upload1.value.submit();
      initForm();
      closeDialog();
    })
    .catch((err) => {
      ElMessage({
        type: "error",
        message: err.data,
      });
    });

  // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
};

const imgpreivew = (file: any) => {
 
  if (file.raw.type == "image/jpeg") {
    //图片的raw 转换为url
    state.ruleForm.imageUrl = URL.createObjectURL(file.raw);
  } else {
    ElMessage({
      type: "error",
      message: "请上传 image/jpeg类型的图片",
    });
  }
};

const handleAvatarSuccess = (res: any, file: any) => {
  state.ruleForm.imageUrl = URL.createObjectURL(file.raw);
  // ElMessage({
  //   type: "success",
  //   message: "上传成功",
  // });
};
const beforeAvatarUpload = (file: any) => {
  const isJPG = file.type === "image/jpeg";
  const isLt2M = file.size / 1024 / 1024 < 2;

  if (!isJPG) {
    ElMessage.error("图片必须为JPG格式");
  }

  // return isJPG && isLt2M;
  //压缩
  return new Promise((resolve) => {
    // compress(file, 100).then((res) => {
    //   console.log(res);
    //   resolve(res);
    // });

    compressAccurately(file, {
      size: 200,
      width: 500,
      height: 500,
    }).then((res) => {
      console.log(res);
      resolve(res);
    });
  });
};
// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {
  state.ruleForm.part_name = "";
  state.ruleForm.part_spec = "";
  state.ruleForm.area = "";
  state.ruleForm.balance = "";
  state.ruleForm.original = "";

  state.ruleForm.remark = "";
  state.ruleForm.type = "";
};
</script>

<style>
#app
  > section
  > section
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > main
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > div
  > div
  > div:nth-child(2)
  > div
  > div
  > div.el-dialog__body
  > form
  > div:nth-child(2)
  > div:nth-child(1)
  > div
  > label {
  line-height: 32px;
  width: 96px;
}

#app
  > section
  > section
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > main
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > div
  > div
  > div:nth-child(2)
  > div
  > div
  > div.el-dialog__body
  > form
  > div:nth-child(2)
  > div:nth-child(2)
  > div
  > label {
  width: 110px !important;
}
</style>
