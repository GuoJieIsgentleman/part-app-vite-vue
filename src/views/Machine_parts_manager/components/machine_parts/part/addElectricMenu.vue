<template>
  <div class="system-menu-container">
    <el-dialog
      title="添加需要的备件"
      v-model="state.isShowDialog"
      width="769px"
      @close="closeDialog"
    >
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="成套备件名称">
              <el-input v-model="state.ruleForm.machine_part_name" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="单体类型">
              <el-input v-model="state.ruleForm.type" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="成套备件区域">
              <el-input v-model="state.ruleForm.machine_part_area" disabled=""></el-input>
            </el-form-item>
          </el-col>
          <el-table
            :data="state.tabledata"
            style="width: 80%"
            show
            border
            align="center"
            height="200"
            header-align="center"
            @row-click="rowclick"
          >
            <el-table-column prop="part_name" label="part_name" width="180" />
            <el-table-column prop="part_spec" label="part_spec" width="180" />
            <el-table-column prop="balance" label="balance" width="80" />
            <el-table-column prop="area" label="area" width="180" />
          </el-table>

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
            <el-form-item label="搁置区域">
              <el-select
                v-model="state.ruleForm.area"
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
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存">
              <el-input v-model="state.ruleForm.balance" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="补充数量">
              <el-input-number
                v-model="state.ruleForm.addcount"
                :min="1"
                :max="state.ruleForm.balance"
              />
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
  tabledata: [],
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
    machine_part_area: "",
    singlepart: "",
    addcount: "",
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

const get_part_balance = (part_name: string) => {
  service
    .get("/get_part_balanceinfo", {
      params: {
        part_name: part_name,
      },
    })
    .then((res) => {
      console.log("获取的 单体备件信息");
      console.log(res.data);
      state.tabledata = res.data.map((item: any) => {
        return {
          id: item[0],
          part_name: item[1],
          part_spec: item[2],
          area: item[3],
          balance: item[4],
          original: item[5],
          remark: item[6],
          type: item[7],
          partimgsrc: item[8],
          connection: item[9],
        };
      });
    })
    .catch((err) => {
      console.log(err);
    });
};
// 打开弹窗

const openDialog = (row: any, index: any) => {
  console.log("增加库存row和index");

  console.log("row", row);
  //获取 单体备件库存
  get_part_balance(row["part_name"]);
  state.isShowDialog = true;

  state.ruleForm.machine_part_name = row["machine_part_name"];
  state.ruleForm.type = row["type"];
  state.ruleForm.machine_part_area = row["area"];
};

defineExpose({ openDialog });
// 关闭弹窗
const closeDialog = (row?: object) => {
  initForm();
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
  state.tabledata = [];
  console.log("取消 重置table");
  initForm();
  closeDialog();
};
// 新增

const upload1 = ref();
const onSubmit = () => {
  // 数据，请注意需要转换的类型
  // 关闭弹窗

  //增加成套库存  减少单体库存
  if (state.ruleForm.part_name == "") {
    ElMessage({
      type: "error",
      message: "请确认信息",
    });
  } else {
    service
      .get("/addmachine_part_count", {
        params: {
          machine_part_area: state.ruleForm.machine_part_area,
          machine_part_name: state.ruleForm.machine_part_name,
          part_name: state.ruleForm.part_name,
          part_spec: state.ruleForm.part_spec,
          area: state.ruleForm.area,
          balance: state.ruleForm.balance,
          original: state.ruleForm.balance,
          remark: state.ruleForm.remark,
          type: state.ruleForm.type,
          addcount: state.ruleForm.addcount,
        },
      })
      .then((res) => {
        ElMessage({
          type: "success",
          message: res.data,
        });

        initForm();
        closeDialog();
      })
      .catch((err) => {
        ElMessage({
          type: "error",
          message: err.data,
        });
        initForm();
        closeDialog();
      });
  }
  // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
};

// const imgpreivew = (file: any) => {
//   console.log(file.raw.type);
//   if (file.raw.type == "image/jpeg") {
//     //图片的raw 转换为url
//     state.ruleForm.imageUrl = URL.createObjectURL(file.raw);
//   } else {
//     ElMessage({
//       type: "error",
//       message: "请上传 image/jpeg类型的图片",
//     });
//   }
// };

// const handleAvatarSuccess = (res: any, file: any) => {
//   state.ruleForm.imageUrl = URL.createObjectURL(file.raw);
//   // ElMessage({
//   //   type: "success",
//   //   message: "上传成功",
//   // });
// };
// const beforeAvatarUpload = (file: any) => {
//   const isJPG = file.type === "image/jpeg";
//   const isLt2M = file.size / 1024 / 1024 < 2;

//   if (!isJPG) {
//     ElMessage.error("图片必须为JPG格式");
//   }

//   // return isJPG && isLt2M;
//   //压缩
//   return new Promise((resolve) => {
//     // compress(file, 100).then((res) => {
//     //   console.log(res);
//     //   resolve(res);
//     // });

//     compressAccurately(file, {
//       size: 200,
//       width: 500,
//       height: 500,
//     }).then((res) => {
//       console.log(res);
//       resolve(res);
//     });
//   });
// };
// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {
  state.ruleForm.part_name = "";
  state.ruleForm.part_spec = "";
  state.ruleForm.area = "";
  state.ruleForm.balance = "";
  state.ruleForm.original = "";

  state.ruleForm.remark = "";
  state.ruleForm.type = "";
  state.tabledata = [];
};

const rowclick = (row: any, column: any, event: any) => {
  state.ruleForm.balance = "";
  state.ruleForm.addcount = "";
  state.ruleForm.part_name = row["part_name"];
  state.ruleForm.balance = row["balance"];
  state.ruleForm.area = row["area"];
  state.ruleForm.part_spec = row["part_spec"];
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
</style>
