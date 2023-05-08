<template>
  <div class="system-menu-container">
    <el-dialog title="编辑菜单" v-model="state.isShowDialog" width="769px" :before-close="handleClose">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件图片">
              <div v-if="state.ruleForm.imgsrc">

                <el-upload class="avatar-uploader" :multiple="false" ref="upload" :auto-upload="true" :action="'https://www.ssxyf.cn:5556/hg_ToolingUploadfile?imgid=' +
                  state.ruleForm.id +
                  '&&time1=' +
                  new Date().getTime().toString()
                  " :show-file-list="false" :on-success="handleAvatarSuccess" :on-change="onchange"
                  :before-upload="beforeAvatarUpload">
                  <img v-if="state.ruleForm.imageUrl == ''" :src="state.ruleForm.imgsrc" class="avatar" />
                  <img v-else :src="state.ruleForm.imageUrl" class="avatar" />


                </el-upload>

              </div>
              <div v-else>
                <el-upload class="avatar-uploader" :multiple="false" :action="'https://www.ssxyf.cn:5556/hg_ToolingUploadfile?imgid=' +
                  state.ruleForm.id +
                  '&&time1=' +
                  new Date().getTime().toString()
                  " :show-file-list="false" :on-change="onchange" :on-success="handleAvatarSuccess"
                  :before-upload="beforeAvatarUpload">
                  <img v-if="state.ruleForm.imageUrl" :src="state.ruleForm.imageUrl" class="avatar" />

                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="类型">
              <el-input v-model="state.ruleForm.type" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件名称">
              <el-input v-model="state.ruleForm.part_name" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件型号">
              <el-input v-model="state.ruleForm.part_spec" placeholder="" clearable></el-input>
            </el-form-item>
          </el-col>


          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用部位">
              <el-input v-model="state.ruleForm.site_use" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="存放区域">
              <el-input v-model="state.ruleForm.area" placeholder="" clearable></el-input>

            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="结存">
              <el-input v-model="state.ruleForm.balance" :placeholder="(state.ruleForm.balance).toString()"
                clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="原有数量">
              <el-input v-model="state.ruleForm.original" placeholder="" clearable></el-input>
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
import { Debounce } from "/@/utils/untils";
import { UploadFile } from "element-plus/lib/el-upload/src/upload.type";


const state = reactive({

  issave: false,
  isShowDialog: false,

  ruleForm: {
    part_no: '',
    site_use: '',
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

  let { data: res } = await service.get("hg_getToolingUsearea");

  state.ruleForm.userarea = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });

};

const upload = ref();
const handleAvatarSuccess = (file: UploadFile) => {

  console.log('file', file.raw);


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
  }

  // return isJPG && isLt2M;
  //压缩
  return new Promise((resolve) => {


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
  state.ruleForm.remark = row.remark;
  state.ruleForm.site_use = row.site_use
  getusearea();
};
// 关闭弹窗
const closeDialog = (row?: object) => {
  console.log(row);
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

  if (state.ruleForm.type === "" || state.ruleForm.part_name === "" || state.ruleForm.part_spec === "" || state.ruleForm.area === "") {
    ElMessage({ type: 'warning', message: '请完善备件信息' })
    return
  } else if (state.ruleForm.balance === "" || state.ruleForm.balance === "") {
    ElMessage({ type: 'warning', message: '请填写件数' })
    return
  }

  state.issave = !state.issave;

  service.post("hg_updateToolingPart", {
    id: state.ruleForm.id,
    part_name: state.ruleForm.part_name,
    part_spec: state.ruleForm.part_spec,
    site_use: state.ruleForm.site_use,
    area: state.ruleForm.area,
    type: state.ruleForm.type,
    balance: state.ruleForm.balance,
    original: state.ruleForm.original,
    remark: state.ruleForm.remark,
  })
    .then((res) => {


      console.log(res);

      ElMessage({ type: "success", message: res.data });

      emit("senddata", res.data.data, state.ruleForm.index);
      initForm();
    })
    .catch((err) => {
      console.log(err);
      initForm();
    });
  console.log("更新状态信息");

  closeDialog(); // 关闭弹窗

  state.issave = !state.issave;
};

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
  state.ruleForm.site_use = '';
};
const handleClose = () => {

  initForm();
};

// const setValue = (value: string) => {




//   Debounce(countAmount, 1000)


// }

// const countAmount = () => {
//   state.ruleForm.amount = state.ruleForm.price * Number(state.ruleForm.balance)
// }



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
