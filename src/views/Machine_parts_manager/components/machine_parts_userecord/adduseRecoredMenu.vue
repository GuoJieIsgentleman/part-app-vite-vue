<template>
  <div class="system-menu-container">
    <el-dialog
      title="增加成套领用"
      v-model="state.isShowDialog"
      width="769px"
      close-on-press-escape
      :destroy-on-close="true"
      @close="closeDialog"
    >
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用人">
              <el-input v-model="state.userinput" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用产线">
              <el-select v-model="state.use_proline_value" placeholder="使用产线">
                <el-option
                  v-for="item in state.use_proline_options"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用区域">
              <el-select
                v-model="state.ruleForm.use_area"
                key
                placeholder=""
                @change="getmachine_part_names(state.ruleForm.use_area)"
              >
                <el-option
                  v-for="item in state.ruleForm.userarea"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
              <!-- <el-input v-model="ruleForm.use_area" placeholder clearable></el-input> -->
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="成套备件名称">
              <el-select
                v-model="state.machine_part_name"
                placeholder=""
                @change="getpartname(state.machine_part_name)"
              >
                <el-option
                  v-for="item in state.ruleForm.machine_part_names"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
              <!-- <el-input v-model="ruleForm.use_area" placeholder clearable></el-input> -->
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
            <el-table
              :data="state.tableData"
              id="table1"
              style="width: 100%"
              align="center"
              @row-click="rowclick"
            >
              <el-table-column
                prop="part_name"
                label="单体备件名称"
                width="180"
                align="center"
              />
              <el-table-column
                prop="part_spec"
                label="单体备件规格型号"
                width="180"
                align="center"
              />
              <el-table-column
                prop="original"
                label="单体结存剩余（台)"
                align="center"
                width="100"
              />
              <el-table-column prop="type" label="单体类型" align="center" width="120" />
              <el-table-column prop="type1" label="单体类型" align="center" width="120" />
            </el-table>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件名称">
              <el-input disabled v-model="state.ruleForm.part_name"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="规格型号">
              <el-input disabled v-model="state.ruleForm.part_spec"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件类型">
              <el-input disabled v-model="state.ruleForm.type"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存数量">
              <el-input
                disabled
                v-model="state.ruleForm.original"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="单体类型">
              <el-input disabled v-model="state.ruleForm.type1"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用数量">
              <el-input placeholder="请输入数量" v-model="state.ruleForm.use_count">
                <template #prepend>区域库存为:{{ state.ruleForm.original }}</template>
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
              <!-- <el-input placeholder v-model="ruleForm.user_remark"></el-input> -->

              <el-select v-model="state.handle" placeholder="请选择">
                <el-option
                  v-for="item in state.options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用时间">
              <el-input disabled v-model="state.ruleForm.use_date"></el-input>
            </el-form-item>
          </el-col>
          <!-- <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input
                v-model="ruleForm.confirm"
                placeholder="班长"
                clearable
              ></el-input>
            </el-form-item>
          </el-col> -->
        </el-row>
      </el-form>
      <template #footer
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
import { reactive, toRefs, onUnmounted, inject } from "vue";
import service from "/@/utils/request";
import { ElMessage, ElRow } from "element-plus";
import { store } from "/@/store";
import { Session } from "/@/utils/storage";
import { formatDate111 } from "/@/utils/formatTime";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

console.log('Session.get("userInfo")');
console.log(Session.get("userInfo"));

const state = reactive({
  machine_part_name: "",
  tableData: [],
  userinput: Session.get("userInfo").userName,
  options: [
    {
      value: "保养",
      label: "保养",
    },
    {
      value: "外修",
      label: "外修",
    },
    {
      value: "报废",
      label: "报废",
    },
    {
      value: "设备整改",
      label: "设备整改",
    },
  ],
  use_proline_options: [
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
    {
      value: "圆镀料场",
      label: "圆镀料场",
    },
    {
      value: "方镀料场",
      label: "方镀料场",
    },
    {
      value: "锌锭库天车",
      label: "锌锭库天车",
    },
    {
      value: "锅炉房",
      label: "锅炉房",
    },
    {
      value: "换热站",
      label: "换热站",
    },
    {
      value: "空压机房",
      label: "空压机房",
    },
    {
      value: "配电室",
      label: "配电室",
    },
  ],
  use_proline_value: "",
  handle: "",
  value: "",
  issave: false,
  isShowDialog: false,
  shortcuts: [
    {
      text: "今天",
      value: new Date(),
    },
    {
      text: "昨天",
      value: () => {
        const date = new Date();
        date.setTime(date.getTime() - 3600 * 1000 * 24);
        return date;
      },
    },
    {
      text: "一周前",
      value: () => {
        const date = new Date();
        date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
        return date;
      },
    },
  ],
  /**
   * 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式（请注意参数类型！）
   * 受到 `element plus` 类型 `string/number/object` 影响，不可使用 `:value="true"`
   * 的写法，所以传值到后台时，需要转换成布尔值，否则页面可能出现玄学。
   * 路由权限标识为数组格式，基本都需要自行转换类型
   */
  ruleForm: {
    original: 0,
    confirm: "",

    reason: "",
    balance: 0,
    userarea: [],

    part_name: [],
    user: "",
    use_area: "",
    use_part_name: "",
    use_count: 0,
    user_remark: "",
    use_date: "",
    machine_part_names: [],
    type: "",
    usespesc: [],
    type1: "",
    part_spec: "",
  },
});

const getmachine_part_names = (value?: any) => {
  console.log("进来了");
  console.log(value);

  //通过area 找type

  service
    .get("/getmachine_part_names", {
      params: { area: value },
    })
    .then((res) => {
      state.ruleForm.machine_part_names = res.data.map((item: any) => {
        return {
          value: item[0],
          label: item[0],
        };
      });
    })
    .catch((err) => {
      console.log(err);
    });
};

const getspesc = async (value?: any) => {
  console.log("进来了getspesc");
  console.log(value);

  //通过area 找type

  let { data: type } = await service.get("/getmachine_part_spesc", {
    params: {
      area: state.ruleForm.use_area,
      use_part_name: value,
      type: state.ruleForm.type,
    },
  });

  console.log("getspesc   type ");
  console.log(type);
  state.ruleForm.usespesc = type.map((item: any) => {
    return {
      value: item[2],
      label: item[2],
    };
  });
};

const getpartname = async (value?: any) => {
  //通过area 找type

  console.log("通过成套名称 获取单体备件明细+", value);

  service
    .get("/getmachine_parts_singlepart", {
      params: {
        machine_part_name: value,
      },
    })
    .then((res) => {
      console.log(res);
      state.tableData = res.data.data.map((item: any) => {
        return {
          id: item[0],
          part_name: item[1],
          part_spec: item[2],
          area: item[3],
          balance: item[4],
          original: item[5],
          remark: item[6],
          type: item[7],
          connection: item[9],
          type1: item[10],
          machine_part_name: item[11],
          machine_part_id: item[12],
        };
      });
    })
    .catch((err) => {});
};

const getbalance = async (value?: any) => {
  let { data: balance } = await service.get("/get_part_balanceinfo", {
    params: {
      area: state.ruleForm.use_area,
      type: state.ruleForm.type,
      part_name: state.ruleForm.use_part_name,
    },
  });

  console.log("balance");
  console.log(balance);

  state.ruleForm.balance = balance[0][4];
  state.ruleForm.original = balance[0][5];
};

const openDialog = async (row?: object) => {
  state.isShowDialog = true;

  // 领用区域获取
  let { data: res } = await service.get(`/getmachine_part_usearea`);
  console.log(res);
  state.ruleForm.userarea = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
  state.ruleForm.use_date = formatDate111(new Date());
};
// 打开弹窗

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
  closeDialog();
  initForm();
};
// 新增

const inituserecord: any = inject("inituserecord");
const onSubmit = async () => {
  //验证处理
  console.log("handle,,,,", state.handle);
  service
    .get("/addmachine_part_userecord", {
      params: {
        machine_part_name: state.machine_part_name,
        part_name: state.ruleForm.part_name,
        type1: state.ruleForm.type1,
        use_count: state.ruleForm.use_count,
        part_spec: state.ruleForm.part_spec,
        reason: state.ruleForm.reason,
        handle: state.handle,
        use_area: state.ruleForm.use_area,
        user: state.userinput,
        use_procline: state.use_proline_value,
        type: state.ruleForm.type,
        use_date: formatDate111(new Date()),
      },
    })
    .then((res) => {
      console.log(res);
      ElMessage({
        type: "success",
        message: res.data,
      });
      closeDialog();
    })
    .catch((err) => {
      ElMessage({
        type: "error",
        message: err.data,
      });
      closeDialog();
    });

  // let { data: res } = await service.get("/adduserecord", {
  //   params: {
  //     ruleForm: state.ruleForm,
  //   },
  // });

  // 数据，请注意需要转换的类型
  // 关闭弹窗
  //给父组件发送 调用方法 刷新数据
  inituserecord();
  //setBackEndControlRefreshRoutes(); // 刷新菜单，未进行后端接口测试
};
// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {
  state.ruleForm.user = "";
  state.ruleForm.use_area = "";
  state.ruleForm.use_part_name = "";
  state.ruleForm.use_count = 0;
  state.ruleForm.user_remark = "";
  (state.value = ""),
    (state.ruleForm.userarea = []),
    (state.ruleForm.usespesc = []),
    (state.ruleForm.part_name = []);
  state.ruleForm.use_date = "";
  state.ruleForm.balance = 0;
  state.ruleForm.reason = "";
  state.ruleForm.original = 0;
};

const rowclick = (row: any, column: any, event: any) => {
  console.log("点击了事件");
  console.log(row);
  state.ruleForm.balance = row.balance;
  state.ruleForm.original = row.original;
  state.ruleForm.type1 = row.type1;
  state.ruleForm.part_spec = row.part_spec;
  state.ruleForm.part_name = row.part_name;
  state.ruleForm.type = row.type;
  if (row.type1 == "机械") {
    state.options = [
      {
        value: "保养",
        label: "保养",
      },
      {
        value: "设备整改",
        label: "设备整改",
      },
    ];
  } else {
    state.options = [
      {
        value: "保养",
        label: "保养",
      },
      {
        value: "外修",
        label: "外修",
      },
      {
        value: "设备整改",
        label: "设备整改",
      },
    ];
  }
};
</script>

<style>
#table1 {
  text-overflow: ellipsis;
  margin-top: 10px;
  overflow: hidden;
  white-space: nowrap;
  table-layout: fixed;
  padding: 1px 0;
}
</style>
