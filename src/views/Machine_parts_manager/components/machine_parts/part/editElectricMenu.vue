<template>
  <div class="system-menu-container">
    <el-dialog title="更新备件信息" v-model="state.isShowDialog" width="769px" :before-close="handleClose">
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件图片">
              <div v-if="state.ruleForm.imgsrc != ''">
                <!-- <img :src="ruleForm.imgsrc" alt="" style="height: 40%; width: 40%" /> -->
                <el-upload class="avatar-uploader" multiple="false" ref="upload" :action="
                  'https://61.185.74.251:5556/machine_part_uploadfile?imgid=' +
                  state.ruleForm.id +
                  '&&time1=' +
                  new Date().getTime().toString() +
                  '&&machine_part_name=' + state.ruleForm.machine_part_name
                " :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
                  <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
                  <img v-if="state.ruleForm.imageUrl == ''" :src="state.ruleForm.imgsrc" class="avatar" />
                  <img v-else :src="state.ruleForm.imageUrl" class="avatar" />

                  <!-- <i v-else class="el-icon-plus avatar-uploader-icon"></i> -->
                </el-upload>
              </div>
              <div v-else>
                <el-upload class="avatar-uploader" :multiple="false" :action="
                  'https://61.185.74.251:5556/machine_part_uploadfile?imgid=' +
                  state.ruleForm.id +
                  '&&time1=' +
                  new Date().getTime().toString() +
                  '&&machine_part_name=' + state.ruleForm.machine_part_name
                " :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
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
              <el-input disabled v-model="state.ruleForm.type"></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="成套名称">
              <el-input disabled v-model="state.ruleForm.machine_part_name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件名称">
              <el-input disabled v-model="state.ruleForm.part_name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="备件型号">
              <el-input disabled v-model="state.ruleForm.part_spec"></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="搁置区域">
              <el-input disabled v-model="state.ruleForm.area"></el-input>

            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="成套结存">
              <el-input v-model="state.ruleForm.balance" :placeholder="state.ruleForm.balance"
                disabled="true"></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="单件结存原有数量">
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
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

const { t } = useI18n();

const state = reactive({
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
    machine_part_name: "",
  },
});

const getusearea = async () => {
  console.log("执行了 getusearea");
  let { data: res } = await service.get(`/getusearea`);
  console.log(res);
  state.ruleForm.userarea = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
  console.log(state.ruleForm.userarea);
};

const upload = ref();
const handleAvatarSuccess = (res: any, file: any) => {
  state.ruleForm.imageUrl = URL.createObjectURL(file.raw);
  ElMessage({
    type: "success",
    message: "上传成功",
  });
  console.log("upload");
  console.log(upload);
};
const beforeAvatarUpload = (file: any) => {
  const isJPG = file.type === "image/jpeg";
  const isLt2M = file.size / 1024 / 1024 < 2;

  console.log("file");
  console.log(file);
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

// 打开弹窗
const openDialog = (row: any, index: any) => {

  console.log('编辑row', row);


  state.ruleForm.index = index;
  state.ruleForm.id = row.id;
  state.ruleForm.type = row.type;
  state.ruleForm.part_name = row.part_name;
  state.ruleForm.part_spec = row.part_spec;
  state.ruleForm.area = row.area;
  state.ruleForm.balance = row.balance;
  state.ruleForm.original = row.original;
  state.ruleForm.type = row.type;
  state.isShowDialog = true;
  state.ruleForm.machine_part_name = row.machine_part_name;
  state.ruleForm.imgsrc = row.partimgsrc


  // state.ruleForm.imgsrc = row.partimgsrc;
  // state.ruleForm.connection = row.connection;
  getusearea();
};
// 关闭弹窗
const closeDialog = (row?: object) => {
  console.log(row);
  state.isShowDialog = false;
  initForm();
};
// 是否内嵌下拉改变
const onSelectIframeChange = () => {
  // if (state.ruleForm.meta.isIframe === 'true') {
  // 	state.ruleForm.isLink = 'true';
  // } else {
  // 	state.ruleForm.isLink = '';
  // }
};
// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增
defineExpose({ openDialog });
const emit = defineEmits(["senddata"]);

// const sendata = (v: any) => {
//   emit("senddata", v);
// };
const onSubmit = () => {
  // 做保存 更新表的操作

  state.issave = !state.issave;
  //请求
  console.log("state.ruleForm.id:", state.ruleForm.id);
  service
    .get("/update_machine_part", {
      params: {
        id: state.ruleForm.id,
        part_name: state.ruleForm.part_name,
        part_spec: state.ruleForm.part_spec,
        area: state.ruleForm.area,
        type: state.ruleForm.type,
        new_balance: state.ruleForm.balance,
        new_original: state.ruleForm.original,
        connection: state.ruleForm.connection,
        machine_part_name: state.ruleForm.machine_part_name,
      },
    })
    .then((res) => {
      ElMessage({ type: "success", message: res.data });
      // sendata(res.data.data);
      emit("senddata", res.data.data, state.ruleForm.index);
      initForm();
      upload.value.submit();
      closeDialog();
    })
    .catch((err) => {
      console.log(err);
      initForm();
      closeDialog();
    });
  console.log("更新状态信息");

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
