<template>
  <div class="system-menu-container">
    <el-dialog
      title="机修使用件添加"
      @close="initForm"
      v-model="state.isShowDialog"
      width="769px"
    >
      <el-form :model="state.ruleForm" label-width="80px">
        <el-row :gutter="50">
         <el-space wrap :size="20">
          <el-col :span="5">
            <el-upload
              class="avatar-uploader"
              ref="upload1"
              :on-change="imgpreivewFLP"
              :auto-upload="false"
              :action="
                'http://61.185.74.251:5556/machine_procline_detail_uploadfile?imgid=' +
                state.ruleForm.id +
                '&&time1=' +
                new Date().getTime().toString() +
                '&&flag=FLP'
              "
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
            >
              <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
              <img v-if="state.ruleForm.FLP" :src="state.ruleForm.FLP" class="imgstyle" />

              <el-icon v-else class="avatar-uploader-icon">图1</el-icon>
            </el-upload>
          </el-col>

          <el-col :span="5">
            <el-upload
              class="avatar-uploader"
              ref="upload2"
              :on-change="imgpreivewZD"
              :auto-upload="false"
              :action="
                'http://61.185.74.251:5556/machine_procline_detail_uploadfile?imgid=' +
                state.ruleForm.id +
                '&&time1=' +
                new Date().getTime().toString() +
                '&&flag=ZD'
              "
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
            >
              <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
              <img v-if="state.ruleForm.ZD" :src="state.ruleForm.ZD" class="imgstyle" />

              <el-icon v-else class="avatar-uploader-icon">图2</el-icon>
            </el-upload></el-col
          >
          <el-col :span="5">
            <el-upload
              class="avatar-uploader"
              ref="upload3"
              :on-change="imgpreivewJC"
              :auto-upload="false"
              :action="
                'http://61.185.74.251:5556/machine_procline_detail_uploadfile?imgid=' +
                state.ruleForm.id +
                '&&time1=' +
                new Date().getTime().toString() +
                '&&flag=JC'
              "
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
            >
              <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
              <img v-if="state.ruleForm.JC" :src="state.ruleForm.JC" class="imgstyle" />

              <el-icon v-else class="avatar-uploader-icon">图3</el-icon>
            </el-upload></el-col
          >
          <el-col :span="5">
            <el-upload
              class="avata"
              ref="upload4"
              :on-change="imgpreivewKS"
              :auto-upload="false"
              :action="
                'http://61.185.74.251:5556/machine_procline_detail_uploadfile?imgid=' +
                state.ruleForm.id +
                '&&time1=' +
                new Date().getTime().toString() +
                '&&flag=KS'
              "
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
            >
              <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
              <img v-if="state.ruleForm.KS" :src="state.ruleForm.KS" class="imgstyle" />

              <el-icon v-else class="avatar-uploader-icon">图4</el-icon>
            </el-upload>
          </el-col>
          <el-col :span="5">
            <el-upload
              class="avatar-uploader"
              ref="upload5"
              :on-change="imgpreivewKZXJ"
              :auto-upload="false"
              :action="
                'http://61.185.74.251:5556/machine_procline_detail_uploadfile?imgid=' +
                state.ruleForm.id +
                '&&time1=' +
                new Date().getTime().toString() +
                '&&flag=KZXJ'
              "
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
            >
              <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
              <img
                v-if="state.ruleForm.KZXJ"
                :src="state.ruleForm.KZXJ"
                class="imgstyle"
              />

              <el-icon v-else class="avatar-uploader-icon">图5</el-icon>
            </el-upload>
          </el-col>
          </el-space>
        </el-row>
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="类型">
              <el-input v-model="state.ruleForm.type" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="区域">
              <el-input v-model="state.ruleForm.area" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件名称">
              <el-input
                v-model="state.ruleForm.part_name"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件规格">
              <el-input
                v-model="state.ruleForm.part_spec"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用区域">
              <el-select
                v-model="state.ruleForm.part_area_value"
                filterable
                :placeholder="state.ruleForm.part_area_value"
                clearable
              >
                <el-option
                  v-for="item in state.ruleForm.userarea"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
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
import { compress, compressAccurately } from "image-conversion";
import { ElMessage } from "element-plus";
import { Session } from "/@/utils/storage";

// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
// "element-plus": "^1.0.2-beta.70",

const upload1 = ref();
const upload2 = ref();
const upload3 = ref();
const upload4 = ref();
const upload5 = ref();
const state = reactive({
  issave: false,
  isShowDialog: false,
  ruleForm: {
    procline: "",
    FLP: "",
    ZD: "",
    JC: "",
    KS: "",
    KZXJ: "",
    id: "",
    part_name: "",
    part_spec: "",
    area: "",

    type: "",
    remark: "",
    userarea: [
      {
        value: "圆镀一线",
        label: "圆镀一线",
      },
      {
        value: "圆镀二线",
        label: "圆镀二线",
      },
      {
        value: "圆镀三线",
        label: "圆镀三线",
      },
      {
        value: "圆镀四线",
        label: "圆镀四线",
      },
      {
        value: "圆镀五线",
        label: "圆镀五线",
      },
      {
        value: "圆镀六线",
        label: "圆镀六线",
      },
      {
        value: "方镀一线",
        label: "方镀一线",
      },
      {
        value: "方镀二线",
        label: "方镀二线",
      },
      {
        value: "方镀三线",
        label: "方镀三线",
      },
    ],
    part_area_value: "",
    imageUrl: "",
    imgsrc: "",
    fileList: [],
  },
});
// const getusearea = async () => {
//   console.log("执行了 machine_usearea");
//   let { data: res } = await service.get(`/getmachine_usearea`);
//   console.log(res);
//   state.ruleForm.userarea = res.map((item: any) => {
//     return {
//       value: item[0],
//       label: item[0],
//     };
//   });
// };

// onMounted(getusearea);
// 打开弹窗

const openDialog = (row?: object) => {
  state.isShowDialog = true;
  state.ruleForm.id = row.id;
  state.ruleForm.part_name = row.machine_name;
  state.ruleForm.procline = row.procline;
  state.ruleForm.part_area_value = row.procline;
  state.ruleForm.part_spec = row.machine_spesc;
  state.ruleForm.area = row.area;
  state.ruleForm.type = row.type;
  state.ruleForm.FLP = row.FLP;
  state.ruleForm.ZD = row.ZD;
  state.ruleForm.JC = row.JC;
  state.ruleForm.KS = row.KS;
  state.ruleForm.KZXJ = row.KZXJ;
};
defineExpose({ openDialog });

// 关闭弹窗
const closeDialog = (row?: object) => {
  console.log(row);
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
const onSubmit = () => {
  // 数据，请注意需要转换的类型
  if (
    state.ruleForm.part_name == "" ||
    state.ruleForm.part_spec == "" ||
    state.ruleForm.part_area_value == "" ||
    state.ruleForm.type == ""
  ) {
    ElMessage({
      type: "warning",
      message: "请检查各个选项并填写",
    });
    return;
  }

  service
    .get("/updatemachine_procline_detail", {
      params: {
        id: state.ruleForm.id,
        part_name: state.ruleForm.part_name,
        part_spec: state.ruleForm.part_spec,
        procline: state.ruleForm.part_area_value,
        type: state.ruleForm.type,
        area: state.ruleForm.area,
        username: Session.get("userInfo").userName,
      },
    })
    .then((res) => {
      ElMessage({
        type: "success",
        message: res.data,
      });

      // state.ruleForm.id = res.data[0][0];
      //调用上传图片的方法
      console.log("upload1.value");
      console.log(upload1.value);
      upload1.value.submit();
      upload2.value.submit();
      upload3.value.submit();
      upload4.value.submit();
      upload5.value.submit();
      initForm();
      closeDialog(); // 关闭弹窗
    })
    .catch((err) => {
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

  state.ruleForm.imageUrl = "";
  state.ruleForm.remark = "";
  state.ruleForm.type = "";
  state.ruleForm.part_area_value = "";
  state.ruleForm.FLP = "";
  state.ruleForm.ZD = "";
  state.ruleForm.KS = "";
  state.ruleForm.KZXJ = "";
  state.ruleForm.JC = "";
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
const imgpreivewFLP = (file: any) => {
  //图片的raw 转换为url
  console.log("imgpreivewFLP");
  console.log(file);

  state.ruleForm.FLP = URL.createObjectURL(file.raw);
};

const imgpreivewZD = (file: any) => {
  //图片的raw 转换为url
  console.log("imgpreivewFLP");
  console.log(file);
  state.ruleForm.ZD = URL.createObjectURL(file.raw);
};

const imgpreivewJC = (file: any) => {
  //图片的raw 转换为url
  console.log("imgpreivewJC");
  console.log(file);
  state.ruleForm.JC = URL.createObjectURL(file.raw);
};

const imgpreivewKS = (file: any) => {
  //图片的raw 转换为url
  console.log("imgpreivewKS");
  console.log(file);
  state.ruleForm.KS = URL.createObjectURL(file.raw);
};

const imgpreivewKZXJ = (file: any) => {
  //图片的raw 转换为url
  console.log("imgpreivewKZXJ");
  console.log(file);
  state.ruleForm.KZXJ = URL.createObjectURL(file.raw);
};
</script>

<style scoped>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 5px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 40px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}

.imgstyle {
  width: 80px;
  height: 80px;
}
</style>
