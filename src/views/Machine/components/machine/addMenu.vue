<template>
  <div class="system-menu-container">
    <el-dialog title="机械备件添加" @close="initForm" v-model="state.isShowDialog" width="769px">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col :span="6">
            <el-form-item label="备件图片">
              <el-upload class="avatar-uploader" ref="addmachineimgupload" :on-change="imgpreivew" :multiple="false"
                :onProgress="onProgress" :action="
                  'https://www.ssxyf.cn:5556/machine_uploadfile?imgid=' + state.ruleForm.id + '&&time1=' +
                  new Date().getTime().toString()" :show-file-list="false" :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload" :auto-upload="false">
                <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
                <img v-if="state.ruleForm.imageUrl" :src="state.ruleForm.imageUrl" class="avatar" />

                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
              </el-upload>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件名称">
              <el-input v-model="state.ruleForm.part_name" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件规格">
              <el-input v-model="state.ruleForm.part_spec" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="24" :xl="12">
            <el-form-item label="搁置区域">
              <!-- <el-input v-model="state.ruleForm.part_area_value" placeholder="搁置区域" clearable></el-input> -->

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
                  {{ state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + '-' + state.num }}
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
              <el-input v-model="state.ruleForm.original" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="单价">
              <el-input v-model="state.ruleForm.price" @input="setValue" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="金额">
              <el-input v-model="state.ruleForm.amount" placeholder clearable disabled></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备注">
              <el-input v-model="state.ruleForm.remark" placeholder clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="类型">
              <el-input v-model="state.ruleForm.type" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form><template #footer><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="state.issave" size="small">保存</el-button>
        </span></template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs, onUnmounted, onMounted, ref } from "vue";
import service from "/@/utils/request";
import { compress, compressAccurately } from "image-conversion";
import { ElMessage } from "element-plus";
import { Session } from "/@/utils/storage";

import { Debounce } from '/@/utils/untils'
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
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
  },
  {
    value: "方镀库",
    label: "方镀库",
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
    id: "2222222",
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
    imgsrc: "",
    fileList: [],
    price: 0,
    amount: 0.00
  },
});
const getusearea = async () => {

  let { data: res } = await service.get(`/getmachine_usearea`);

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
const onCancel = () => {
  closeDialog();
  initForm();
};


const onProgress = () => {
  console.log('正在上传');
  console.log('state.ruleform.id', state.ruleForm.id);

}

const addmachineimgupload = ref();

// 新增
const onSubmit = () => {


  let tempStr = state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + "-" + state.num

  if (state.ruleForm.type === "" || state.ruleForm.part_name === "" || state.ruleForm.part_spec === "" || state.floor === "" || state.shelf === "") {
    ElMessage({ type: 'warning', message: '请完善备件信息' })
    return
  } else if (state.ruleForm.balance === "" || state.ruleForm.balance === "") {
    ElMessage({ type: 'warning', message: '请填写件数' })
    return
  }

  // 数据，请注意需要转换的类型

  service
    .get("/addmachine_detail", {
      params: {
        part_name: state.ruleForm.part_name,
        part_spec: state.ruleForm.part_spec,
        area: tempStr,
        balance: state.ruleForm.balance,
        original: state.ruleForm.balance,
        remark: state.ruleForm.remark,
        type: state.ruleForm.type,
        username: Session.get("userInfo").userName,
        price: state.ruleForm.price,
        amount: state.ruleForm.amount
      },
    })
    .then(async (res: any) => {
      ElMessage({
        type: "success",
        message: res.data.msg,
      });
      state.ruleForm.id = res.data.id;


      console.log('state.ruleForm.id', state.ruleForm.id);

      //调用上传图片的方法
      console.log(addmachineimgupload.value);



      await addmachineimgupload.value.submit();
      initForm();
      closeDialog(); // 关闭弹窗
    })
    .catch((err: any) => {
      ElMessage({
        type: "error",
        message: `${err.data} 请检查填写项`,
      });
      initForm();
      closeDialog(); // 关闭弹窗
    });

  // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
};
// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {
  state.ruleForm.part_name = "";
  state.ruleForm.part_spec = "";
  state.ruleForm.area = "";
  state.ruleForm.balance = "";
  state.ruleForm.original = "";
  state.ruleForm.imageUrl = "";
  state.ruleForm.remark = "";
  state.ruleForm.type = "";
  state.ruleForm.price = 0;

  state.ruleForm.id = ''
  state.ruleForm.amount = 0;
  state.ruleForm.part_area_value = "";
  state.floor = ''
  state.shelf = ''
  state.num = ''


  addmachineimgupload.value.clearFiles()
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
  return new Promise((resolve: any) => {
    // compress(file, 100).then((res) => {
    //   console.log(res);
    //   resolve(res);
    // });

    compressAccurately(file, {
      size: 200,
      width: 500,
      height: 500,
    }).then((res: any) => {
      console.log(res);
      resolve(res);
    });
  });
};
const imgpreivew = (file: any) => {
  //图片的raw 转换为url
  state.ruleForm.imageUrl = URL.createObjectURL(file.raw);
};


const setValue = () => {
  Debounce(countAmount, 1000)
}

const countAmount = () => {

  state.ruleForm.amount = state.ruleForm.price * Number(state.ruleForm.balance)



}
</script>
