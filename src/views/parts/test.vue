<template>
  <div class="system-menu-container">
    <el-button  v-if="state.ishsowNFC" class="butn" type="primary" @click="test_nfc">NFC巡检</el-button>
   
     <el-button v-if="state.ishsow" class="butn" type="primary" 
     @click="open_inspector">点击巡检</el-button>
   <Inspectshow ref="Inspectshowref" @sendflag="getflag" />
   
    <el-dialog v-model="state.dialogFormVisible" title="选择巡检区域">
      <div>
        <el-form>
          <el-form-item label="请选择巡检区域">

            <el-select v-model="state.part_area_value" filterable placeholder="备件区域" clearable>
              <el-option v-for="item in state.userarea" :key="item['label']" :label="item['label']"
                :value="item['value']">
              </el-option>
            </el-select>
          </el-form-item>

        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="state.dialogFormVisible = false">Cancel</el-button>
          <el-button type="primary" @click="getinfo()">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from "vue";
import Inspectshow from "/@/views/parts/components/inspect/inspectshow.vue";
import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";
import { ElAside, ElMessage } from "element-plus";
import { Session } from "/@/utils/storage";
const Inspectshowref = ref();

const getinfo = () => {

  console.log(state.part_area_value);

  Inspectshowref.value.openDialog(JSON.stringify(state.part_area_value), formatDate111(new Date()));
  state.dialogFormVisible = false;
}



const open_inspector = () => {
  console.log("121212");
  console.log(Inspectshowref.value);

  state.dialogFormVisible = true;




}

const test = () => {
  console.log(Inspectshowref.value);
};
const getflag = (v: any) => {
  state.flag = v;

  console.log("state.flag");
  console.log(state.flag);
};
const state = reactive({
  dialogFormVisible:false,
  ishsow:false,
  ishsowNFC:false,
  flag: true,
  w: null as any,
  cardid: "",
  inspecter: "",
  show: true,
  remarkValue: "",
  part_area_value:"",
  userarea:[]
});

onMounted(() => {
  getuserarea();
  //check();
})



const getuserarea = () => {
  service.get('getinspection', {
    params: {
      username: Session.get("userInfo").userName,
      cardid: "-1"
    }
  }).then((res: any) => {
    console.log(res)
    if (res.data == -1) {
      state.ishsowNFC = true;
      return;
    } else {
      state.ishsowNFC = false;
      state.ishsow = true;
      // var temps = eval('(' + res.data[0][0] + ')');
      state.userarea = res.data.map((item: any) => {
        return {

          value: item[1],
          label: item[2],

        }
      })
      console.log(state.userarea)
    }
  }).catch((err: any) => {
    ElMessage({
      type: "warning",
      message: "NFC巡检"
    })
  })

}

const centerDialogVisible = ref(false);
const dialogBeforeClose = () => {};

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

  Inspectshowref.value.openDialog(JSON.stringify(v), formatDate111(new Date()));

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
//测试
const testback = () => {
  Inspectshowref.value.openDialog(
    JSON.stringify("-6,13,-1,125"),
    formatDate111(new Date())
  );
  console.log("巡检标签执行完毕");
};
</script>

<style lang="less">
.tableclass {
  color: rgb(0, 0, 0);
  size: 50px;
}

section
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
  > button {
  height: 200px;
  left: 40px;
  font-size: 80px;
  display: block;
  margin: 0 auto;
  width: 90%;
  margin-top: 50%;
  padding: 20px;
}
</style>
