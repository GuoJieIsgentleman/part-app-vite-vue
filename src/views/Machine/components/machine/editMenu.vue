<template>
  <div class="system-menu-container">
    <el-dialog title="编辑菜单" v-model="state.isShowDialog" width="769px" :before-close="handleClose">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件图片">
              <div v-if="state.ruleForm.imgsrc != ''">
                <!-- <img :src="ruleForm.imgsrc" alt="" style="height: 40%; width: 40%" /> -->
                <el-upload class="avatar-uploader" :auto-upload="true" :multiple="false" ref="machineupload"
                  :onProgress="onProgress" :action="
                    'https://www.ssxyf.cn:5556/machine_uploadfile?imgid=' +
                    state.ruleForm.id +
                    '&&time1=' +
                    new Date().getTime().toString()
                  " :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload"
                  :on-change="onchange">
                  <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
                  <img v-if="state.ruleForm.imageUrl == ''" :src="state.ruleForm.imgsrc" class="avatar" />
                  <img v-else :src="state.ruleForm.imageUrl" class="avatar" />

                  <!-- <i v-else class="el-icon-plus avatar-uploader-icon"></i> -->
                </el-upload>
              </div>
              <div v-else>
                <el-upload class="avatar-uploader" :auto-upload="true" :multiple="false" ref="machineupload"
                  :onProgress="onProgress" :action="
                    'https://www.ssxyf.cn:5556/machine_uploadfile?imgid=' +
                    state.ruleForm.id +
                    '&&time1=' +
                    new Date().getTime().toString()
                  " :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload"
                  :on-change="onchange">
                  <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
                  <img v-if="state.ruleForm.imageUrl" :src="state.ruleForm.imageUrl" class="avatar" />

                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
                <!-- <img :src="scope.row.partimgsrc" alt="" /> -->
              </div>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="类型">
              <el-input :disabled="isdisabled" v-model="state.ruleForm.type" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件名称">
              <el-input :disabled="isdisabled" v-model="state.ruleForm.part_name" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件型号">
              <el-input :disabled="isdisabled" v-model="state.ruleForm.part_spec" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="机械连接方式">
              <el-input v-model="state.ruleForm.connection" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="新搁置区域" :label-width="85">
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


              </el-row>

            </el-form-item>


            <!-- <el-input v-model="state.ruleForm.area" placeholder=""></el-input> -->
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="最新区域">
              {{ state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + '-' + state.num }}
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="原区域">
              <el-input v-model="state.ruleForm.area" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="结存">
              <el-input v-model="state.ruleForm.balance" :placeholder="state.ruleForm.balance" @input="setValue"
                clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="原有数量">
              <el-input v-model="state.ruleForm.original" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="单价">
              <el-input v-model="state.ruleForm.price" placeholder="" clearable @input="setValue"></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="金额">
              <el-input v-model="state.ruleForm.amount" placeholder="" clearable disabled></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备注">
              <el-input v-model="state.ruleForm.remark" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="state.issave" size="small">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { compress, compressAccurately } from "image-conversion";
import { reactive, toRefs, ref } from "vue";
import { useI18n } from "vue-i18n";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";
import { formatDate111 } from "/@/utils/formatTime";
import { store } from "/@/store";
import { Session } from "/@/utils/storage";
import { Debounce } from "/@/utils/untils";
import { UploadFile } from "element-plus/lib/el-upload/src/upload.type";

// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

//编辑框根据权限显示是否让编辑 班长

const isdisabled = ref(true);
const machineupload = ref();

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
  }
    ,
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
  usernmae: Session.get("userInfo").userName,
  issave: false,
  isShowDialog: false,
  /**
   * 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式（请注意参数类型！）
   * 受到 `element plus` 类型 `string/number/object` 影响，不可使用 `:value="true"`
   * 的写法，所以传值到后台时，需要转换成布尔值，否则页面可能出现玄学。
   * 路由权限标识为数组格式，基本都需要自行转换类型
   */
  ruleForm: {
    new_original: 0,
    new_balance: 0,
    id: "",
    part_name: "",
    part_spec: "",
    area: "",
    balance: "",
    original: "",
    remark: "",
    // filltime: "",
    type: "",
    imgsrc: "",
    imageUrl: "",
    connection: "",
    index: 0,
    userarea: [],
    price: 0,
    amount: 0
  },
});

const getusearea = async () => {

  let { data: res } = await service.get(`/getmachine_usearea`);
  console.log(res);
  state.ruleForm.userarea = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });

};



const onProgress = () => {
  console.log('正在上传');
  console.log('state.ruleform.id', state.ruleForm.id);

}
const handleAvatarSuccess = (res: any, file: any) => {
  state.ruleForm.imageUrl = URL.createObjectURL(file.raw);
  ElMessage({
    type: "success",
    message: "上传成功",
  });

};
const beforeAvatarUpload = (file: any) => {
  const isJPG = file.type === "image/jpeg";
  const isLt2M = file.size / 1024 / 1024 < 2;




  if (!isJPG) {
    ElMessage.error("图片必须为JPG格式");
    return
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

// 打开弹窗
const openDialog = (row: any, index: any) => {

  state.ruleForm.index = index;
  state.ruleForm.id = row.id;
  state.ruleForm.part_name = row.part_name;
  state.ruleForm.part_spec = row.part_spec;
  state.ruleForm.area = row.area;
  state.ruleForm.balance = row.balance;
  state.ruleForm.original = row.original;
  state.ruleForm.type = row.type;
  state.isShowDialog = true;
  state.ruleForm.imgsrc = row.partimgsrc;
  state.ruleForm.connection = row.connection;
  state.ruleForm.price = row.price;
  state.ruleForm.amount = row.amount;
  state.ruleForm.remark = row.remark
  getusearea();



  store.state.userInfos.userInfos.authBtnList.map((val: any) => {
    if (val == "btn.isdisabled") {
      isdisabled.value = false;
    }
  });
};
// 关闭弹窗
const closeDialog = (row?: object) => {

  state.isShowDialog = false;
  initForm();
};

// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增
defineExpose({ openDialog });
const emit = defineEmits(["senddata"]);


const onSubmit = () => {


  // 做保存 更新表的操作
  let temp = state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + '-' + state.num
  if (state.ruleForm.type === "" || state.ruleForm.part_name === "" || state.ruleForm.part_spec === "" || state.ruleForm.area === "") {
    ElMessage({ type: 'warning', message: '请完善备件信息' })
    return
  } else if (state.ruleForm.balance === "" || state.ruleForm.balance === "") {
    ElMessage({ type: 'warning', message: '请填写件数' })
    return
  }
  state.issave = !state.issave;
  //请求

  service
    .get("/updatemachine_part", {
      params: {
        id: state.ruleForm.id,
        part_name: state.ruleForm.part_name,
        part_spec: state.ruleForm.part_spec,
        area: temp === "-" ? state.ruleForm.area : temp,
        type: state.ruleForm.type,
        new_balance: state.ruleForm.balance,
        new_original: state.ruleForm.original,
        connection: state.ruleForm.connection,
        username: Session.get("userInfo").userName,
        price: state.ruleForm.price,
        amount: state.ruleForm.amount,
        remark: state.ruleForm.remark

      },
    })
    .then(async (res) => {

      state.ruleForm.id = res.data.id

      await machineupload.value.submit()
      ElMessage({ type: "success", message: res.data.msg })

      emit("senddata", res.data.data, state.ruleForm.index);
      initForm();


    })
    .catch((err) => {

      ElMessage({ type: "warning", message: '更新出错' });


      initForm();
    });


  closeDialog(); // 关闭弹窗
  // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
  state.issave = !state.issave;
};
// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {
  state.ruleForm.part_name = "";
  state.ruleForm.part_spec = "";
  state.ruleForm.area = "";
  state.ruleForm.balance = "";
  state.ruleForm.new_balance = 0;
  state.ruleForm.new_original = 0;
  state.ruleForm.original = "";
  state.isShowDialog = false;
  state.ruleForm.imageUrl = "";
  state.ruleForm.imgsrc = "";
};
const handleClose = () => {
  state.ruleForm.part_name = "";
  state.ruleForm.part_spec = "";
  state.ruleForm.area = "";
  state.ruleForm.balance = "";
  state.ruleForm.new_balance = 0;
  state.ruleForm.new_original = 0;
  state.ruleForm.original = "";
  state.isShowDialog = false;
  state.ruleForm.imageUrl = "";
  state.ruleForm.imgsrc = "";
  initForm();
};

const setValue = () => {
  Debounce(countAmount, 1000)
}

const countAmount = () => {

  state.ruleForm.amount = state.ruleForm.price * Number(state.ruleForm.balance)



}



const onchange = (uploadFile: UploadFile) => {
  console.log('文件状态改变', uploadFile);
  state.ruleForm.imageUrl = URL.createObjectURL(uploadFile.raw);
  state.ruleForm.imgsrc = ''
}

</script>
<style lang="less">
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 160px;
  height: 160px;
  display: block;
}
</style>
