<template>
  <div class="system-menu-container">
    <el-dialog
      v-loading="state.loading"
      title="新增菜单"
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
            <!-- <div>
              <el-button type="primary" @click="test_nfc">请点击准备刷NFC</el-button>
            </div> -->
            <el-form-item label="领用区域">
              <el-select
                v-model="state.ruleForm.model"
                key
                placeholder=""
                @change="gettype(state.ruleForm.model)"
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
            <el-form-item label="备件类型">
              <el-select
                v-model="state.ruleForm.model1"
                placeholder=""
                @change="getpartname(state.ruleForm.model1)"
              >
                <el-option
                  v-for="item in state.ruleForm.usetype"
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
            <el-form-item label="备件名称">
              <el-select
                v-model="state.ruleForm.model3"
                placeholder=""
                @change="getspesc(state.ruleForm.model3)"
              >
                <el-option
                  v-for="item in state.ruleForm.part_name"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件型号">
              <el-select
                v-model="state.ruleForm.model2"
                placeholder=""
                @change="getbalance(state.ruleForm.model2)"
              >
                <el-option
                  v-for="item in state.ruleForm.usespesc"
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
            <el-form-item label="结存数量">
              <el-input
                disabled
                v-model="state.ruleForm.balance"
                placeholder
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input
                disabled
                v-model="state.ruleForm.original"
                placeholder
                clearable
              ></el-input>
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
import { ElMessage } from "element-plus";
import { store } from "/@/store";
import { Session } from "/@/utils/storage";
import { formatDate111 } from "/@/utils/formatTime";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

console.log('Session.get("userInfo")');
console.log(Session.get("userInfo"));

const state = reactive({
  flag: true,
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
  loading: true,
  ruleForm: {
    original: 0,
    confirm: "",
    model: "",
    model1: "",
    model2: "",
    model3: "",
    reason: "",
    balance: 0,
    userarea: [],
    usetype: [],
    usespesc: [],
    part_name: [],
    user: "",
    use_area: "",
    use_part_name: "",
    use_count: 0,
    user_remark: "",
    use_date: "",
  },
});

const gettype = async (value?: any) => {
  console.log("进来了");
  console.log(value);

  //通过area 找type

  let { data: type } = await service.get("/gettype", 
  { params: { area: value } });

  console.log("type:",type)
  state.ruleForm.usetype = type.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
};

const getspesc = async (value?: any) => {
  console.log("进来了getspesc");
  console.log(value);

  //通过area 找type

  let { data: type } = await service.get("/getspesc", {
    params: {
      area: state.ruleForm.model,
      use_part_name: value,
      type: state.ruleForm.model1,
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

  let { data: partname } = await service.get("/getpartname", {
    params: {
      area: state.ruleForm.model,
      type: state.ruleForm.model1,
      // spec: state.ruleForm.model2,
    },
  });

  console.log("partname");
  console.log(partname);

  state.ruleForm.part_name = partname.map((item: any) => {
    return {
      value: item[1],
      label: item[1],
      count: item[4],
    };
  });
};

const getbalance = async (value?: any) => {
  let { data: balance } = await service.get("/getbalance", {
    params: {
      area: state.ruleForm.model,
      type: state.ruleForm.model1,
      spec: state.ruleForm.model2,
      part_name: state.ruleForm.model3,
    },
  });

  console.log("balance");
  console.log(balance);

  state.ruleForm.balance = balance[0][4];
  state.ruleForm.original = balance[0][5];
};

// 打开弹窗

const openDialog = async (row?: object) => {
  state.isShowDialog = true;

  // 领用区域获取
  let { data: res } = await service.get(`/getusearea`);
  console.log(res);
  state.ruleForm.userarea = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
  state.ruleForm.use_date = formatDate111(new Date());
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
  closeDialog();
  initForm();
};
// 新增

const inituserecord: any = inject("inituserecord");
const onSubmit = async () => {
  //验证处理
  state.issave = !state.issave;
  if (state.ruleForm.use_count <= state.ruleForm.balance && state.ruleForm.balance > 0) {
    if (state.ruleForm.use_count <= 0 || state.handle == "" || state.userinput == "") {
      console.log("state.ruleForm.use----------r");
      console.log(state.ruleForm.use_count);
      console.log(state.handle);
      console.log(state.ruleForm.user);
      ElMessage.warning("请重新输入");
      state.ruleForm.use_count = 0;
    } else {
      //提交 保存  做非空验证

      let { data: res } = await service.post("/adduserecord", {
        user: state.userinput,
        area: state.ruleForm.model,
        type: state.ruleForm.model1,
        spec: state.ruleForm.model2,
        part_name: state.ruleForm.model3,
        use_count: state.ruleForm.use_count,
        reason: state.ruleForm.reason,
        use_date: state.ruleForm.use_date,
        confirm: state.ruleForm.confirm,
        use_procline: state.use_proline_value,
        handle: state.handle,
        flag: "add",
      });
      console.log("添加领用记录返回值");
      console.log(res);
      ElMessage({
        type: "success",
        message: `${state.handle}成功`,
        showClose: true,
      });
      state.issave = !state.issave;
      closeDialog();
    }
  } else {
    state.issave = !state.issave;
    ElMessage.warning("领用件数不能大于库存件数，请重新输入");
    state.ruleForm.use_count = 0;
  }

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
    (state.ruleForm.model = ""),
    (state.ruleForm.model1 = ""),
    (state.ruleForm.model2 = ""),
    (state.ruleForm.model3 = ""),
    (state.ruleForm.userarea = []),
    (state.ruleForm.usetype = []),
    (state.ruleForm.usespesc = []),
    (state.ruleForm.part_name = []);
  state.ruleForm.use_date = "";
  state.ruleForm.balance = 0;
  state.ruleForm.reason = "";
};

import { ElLoading } from "element-plus";
const openFullScreen2 = () => {
  setTimeout(() => {
    loading.close();
  }, 2000);

  //设置请求 获取值
};

const newintent1 = () => {
  console.log("newintent");

  setTimeout(handle_nfc_data, 1000);
};
const test_nfc = () => {
  if (state.flag == true) {
    state.flag = false;
    console.log("state.flag");
    console.log(state.flag);
    state.w = plus.nativeUI.showWaiting("请靠近NFC点检标签");
    console.log(state.w);
    var main = plus.android.runtimeMainActivity();
    var Intent = plus.android.importClass("android.content.Intent");
    var Activity = plus.android.importClass("android.app.Activity");
    var PendingIntent = plus.android.importClass("android.app.PendingIntent");
    var IntentFilter = plus.android.importClass("android.content.IntentFilter");
    var NfcAdapter = plus.android.importClass("android.nfc.NfcAdapter");
    var nfcAdapter = NfcAdapter.getDefaultAdapter(main);
    var intent = new Intent(main, main.getClass());
    intent.addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
    var pendingIntent = PendingIntent.getActivity(main, 0, intent, 0);
    var ndef = new IntentFilter("android.nfc.action.TECH_DISCOVERED");
    ndef.addDataType("*/*");
    var intentFiltersArray = [ndef];
    var techListsArray = [
      ["android.nfc.tech.IsoDep"],
      ["android.nfc.tech.NfcA"],
      ["android.nfc.tech.NfcB"],
      ["android.nfc.tech.NfcF"],
      ["android.nfc.tech.Nfcf"],
      ["android.nfc.tech.NfcV"],
      ["android.nfc.tech.NdefFormatable"],
      ["android.nfc.tech.MifareClassi"],
      ["android.nfc.tech.MifareUltralight"],
    ];

    document.addEventListener("newintent", newintent1, false);
    document.addEventListener(
      "pause",
      function (e) {
        if (nfcAdapter) {
          nfcAdapter.disableForegroundDispatch(main);
          console.log("pause");
        }
      },
      false
    );
    document.addEventListener(
      "resume",
      function (e) {
        if (nfcAdapter) {
          console.log("resume");
          nfcAdapter.enableForegroundDispatch(
            main,
            pendingIntent,
            intentFiltersArray,
            techListsArray
          );
        }
      },
      false
    );
    nfcAdapter.enableForegroundDispatch(
      main,
      pendingIntent,
      intentFiltersArray,
      techListsArray
    );
  } else {
    ElMessage({
      type: "warning",
      message: "请执行完本次巡检",
    });
  }
};
const handle_nfc_data = () => {
  state.w.setTitle("请勿移开标签\n正在读取数据...");
  var main = plus.android.runtimeMainActivity();
  var runtimeIntent = main.getIntent();

  var b = runtimeIntent.getExtras();
  plus.android.importClass(b);
  var set = b.keySet();
  plus.android.importClass(set);
  var sb;
  var i = set.iterator();
  plus.android.importClass(i);
  var hasNest = i.hasNext();
  var NfcA = plus.android.importClass("android.nfc.tech.NfcA");
  var IsoDep = plus.android.importClass("android.nfc.tech.IsoDep");
  var Tag = plus.android.importClass("android.nfc.Tag");
  var key = i.next();
  var v = b.get(key);

  if (v instanceof NfcA) {
    var atqa = v.getAtqa();
    var sak = v.getSak();
    var tag = g.getTag();
    plus.android.importClass(tag);
    var techList = tag.getTechList();
    console.log("NfcA Atqa=" + atqa + ";Sak=" + sak + ";techList=" + techList);
  } else if (v instanceof IsoDep) {
    var tag = g.getTag();
    plus.android.importClass(tag);
    var techList = tag.getTechList();
    console.log("IsoDep techList=" + techList);
  } else if (v instanceof Tag) {
    var tag = v;
    var techList = tag.getTechList();
    console.log("Tag techList=" + techList);
  }
  console.log("v=" + v);
  state.cardid = v;
  console.log("cardid=" + state.cardid);

  //获取值
  // getinspection(JSON.stringify(v));

  getinspection(JSON.stringify(v));

  document.removeEventListener("newintent", newintent1, false);
  //关闭事件监听器

  state.w.close();
  // getinspection("[77,-25,-78,33]");
  // state.isShowDialog = !state.isShowDialog;
  // document.getElementById("a").innerHTML = state.resdata;
  // // document.getElementById("b").innerHTML = v;
  // sb = key + "=" + v + "\n";
  // hasNest = i.hasNext();
  // console.log("hasNest=" + hasNest);
  // console.log("v=" + v);
};

//获取点检区域
const getinspection = (v: String) => {
  const loading = ElLoading.service({
    lock: true,
    text: "请将手机靠近NFC",
    background: "rgba(0, 0, 0, 0.7)",
  });
  service
    .get("/getinspection", {
      params: {
        cardid: v,
        flag: "1",
      },
    })
    .then((res) => {
      console.log(res.data);
      state.ruleForm.userarea = res.data.map((item: any) => {
        return {
          label: item[0],
          value: item[0],
        };
      });
      loading.close();
      state.flag = true;
    })
    .catch((err) => {
      ElMessage({
        type: "error",
        message: err.data,
      });
      state.flag = true;
    });
};
</script>
