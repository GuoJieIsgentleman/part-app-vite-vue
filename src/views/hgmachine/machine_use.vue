<template>
  <div class="system-menu-container">


    <AdduseRecoredMenu ref="adduseRecoredMenuref" />

    <Useconfirm ref="useconfirmref" />
    <el-card shadow="hover">
      <el-row :gutter="50">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.add', 'btn.other']">
            <el-button @click="onOpenAddMenu()" type="success">增加库存备件领用记录</el-button>
          </Auths>
        </el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.add']">
            <el-button @click="exportExcel()" type="primary" plain>导出</el-button>
          </Auths>
        </el-col>
      </el-row>
      <el-row :gutter="24">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
          <el-tag type="danger" style="background-color: red; color: white">
            3小时未确认显示红色</el-tag>
        </el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
      </el-row>

      <el-row :gutter="35">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="20" :xl="12">
          <el-date-picker size="mini" class="timestyle" v-model="state.start" type="datetime" placeholder="选择开始日期"
            format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD HH:mm:ss">
          </el-date-picker>
          <el-date-picker size="mini" v-model="state.end" type="datetime" placeholder="选择结束日期"
            format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD HH:mm:ss">
          </el-date-picker>
          <el-select v-model="state.selectprolince" clearable placeholder="选择产线">
            <el-option v-for="item in state.use_proline_options" :key="item.value" :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-select v-model="state.selectarea" clearable placeholder="领用区域">
            <el-option v-for="item in state.useareas" :key="item['value']" :label="item['label']" :value="item['value']">
            </el-option>
          </el-select>
        </el-col>
        <el-col class="mb20" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
        <el-col class="mb20" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="4" :xs="5" :sm="8" :md="8" :lg="3" :xl="1">
          <el-button type="primary" @click="find">查询</el-button></el-col>
        <el-col :span="4" :xs="9" :sm="8" :md="8" :lg="3" :xl="2">
          <el-button @click="find" type="success" plain>查询全部记录</el-button>
        </el-col>
        <el-col :span="4" :xs="6" :sm="8" :md="8" :lg="3" :xl="1">
          <el-button @click="getuse()" type="success" plain>查询未确认</el-button>
        </el-col>
      </el-row>
      <el-table id="outTable" v-loading="state.loading" :data="state.partslist" border align="center" heigth="300"
        style="width: 100%" header-align="center" max-height="400" fit :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }" :row-class-name="addClass">
        <el-table-column prop="id" label="序号" fixed width="50" align="center">
        </el-table-column>
        <el-table-column prop="user" label="领用人" width="70" align="center">
        </el-table-column>

        <el-table-column prop="use_area" min-width="150" align="center" label="领用区域">
        </el-table-column>
        <el-table-column prop="use_procline" min-width="100" align="center" label="使用产线">
        </el-table-column>
        <el-table-column prop="handle" min-width="90" align="center" label="处理方式">
        </el-table-column>
        <el-table-column prop="type" label="备件类型" width="90" align="center">
        </el-table-column>

        <el-table-column prop="use_part_name" label="备件名称" width="180" align="center">
        </el-table-column>
        <el-table-column prop="spec" label="领用备件型号" width="180" align="center">
        </el-table-column>
        <el-table-column prop="site_use" label="使用部件" width="180" align="center">
        </el-table-column>

        <el-table-column prop="use_date" label="领用时间" width="140" align="center">
        </el-table-column>

        <el-table-column prop="use_count" label="领用数量" width="80" align="center">
        </el-table-column>
        <el-table-column prop="useconfirm" label="领用确认人" width="160" align="center">
          <template #default="scope">
            <el-button :disabled="scope.row.useconfirm == null ? false : true" @click="onOpenuseconfirmref(scope.row)"
              type="success">{{
                scope.row.useconfirm == null ? "请确认" : `${scope.row.useconfirm}已确认`
              }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="confirm_date" label="领用确认时间" width="140" align="center">
        </el-table-column>
        <el-table-column prop="user_reason" label="领用备注" min-width="180" align="center">
        </el-table-column>

      </el-table>

    </el-card>


  </div>
</template>

<script lang="ts" setup >
import AdduseRecoredMenu from "./components/machine_use/machine_adduseRecoredMenu.vue";

import Useconfirm from "./components/machine_use/machine_useconfirm.vue";
import service from "/@/utils/request";
import { ref, reactive, onMounted, toRefs, provide } from "vue";
import { formatDate111, subtimehours } from "/@/utils/formatTime";
import { exportTable } from "/@/utils/exportExcel";
import Auths from "/@/components/auth/auths.vue";
import { getElectronArea, ListItem, use_proline_options } from "/@/hooks/getHgInfo";
const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}备件领用明细`);
}


const adduseRecoredMenuref = ref();
const useconfirmref = ref();

const onOpenAddMenu = () => {
  adduseRecoredMenuref.value.openDialog();
};




const onOpenuseconfirmref = (row?: any) => {

  useconfirmref.value.openDialog(row);
};





const state = reactive({
  use_proline_options: [] as Array<ListItem>,
  useareas: [] as Array<ListItem>,
  selectarea: "",
  selectprolince: "",
  start: "",
  end: "",
  area: "",
  confirm: "",

  partslist: [],
  total: 0,
  filterTable: null,
  save: false,

  loading: true,
});

onMounted(async () => {
  state.use_proline_options = await use_proline_options()
  state.useareas = await getElectronArea()
  inituserecord('noconfirm')
})




const conversion = (res: any) => {

  state.partslist = res.data.map((item: any[]) => {
    return {
      id: item[0],
      user: item[1],
      use_area: item[2],
      use_procline: item[3],
      type: item[4],
      spec: item[5],
      use_part_name: item[6],
      site_use: item[7],
      use_count: item[8],
      user_reason: item[9],
      use_date: formatDate111(item[10]),
      useconfirm: item[11],
      handle: item[12],
      confirm_date: formatDate111(item[13]),
      create_date: formatDate111(item[14])

    };
  });
}


//初始化领用记录
const inituserecord = (flag?: any) => {
  console.log(flag);
  service.post("/hg_getMachineUserecord", { flag: flag }).then(res => {
    if (res != null) {
      state.loading = false;
    }

    conversion(res)

    state.total = state.partslist.length;

  })


};

provide("inituserecord", inituserecord);
onMounted(inituserecord);

const addClass = ({ row, rowIndex }: any) => {
  //如果时间相差3小时 就提示颜色

  if (subtimehours(row.use_date) >= 3 && row.useconfirm == "") {
    return "warning-row";
  }
};

const getuse = () => {
  //未确认记录
  inituserecord("noconfirm");
};

const getalluse = () => {
  //所有记录
  inituserecord("all");
};

const find = () => {

  service.post("/hg_getMachineUserecord", {
    flag1: "筛选查询",
    start: state.start,
    end: state.end,
    prolince: state.selectprolince,
    area: state.selectarea
  })
    .then((res) => {

      if (res != null) {
        state.loading = false;
      }

      conversion(res)


      state.total = state.partslist.length;
    })
    .catch((err) => { });
}

</script>


<style lang="scss">
.el-table .el-table-column {
  justify-content: center;

  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  table-layout: fixed;
}

.el-table__body-wrapper::-webkit-scrollbar {
  width: 20px; // 横向滚动条
  height: 20px; // 纵向滚动条 必写
}

// 滚动条的滑块
.el-table__body-wrapper::-webkit-scrollbar-thumb {
  background-color: #ddd;

  border-radius: 10px;
}

.el-table .warning-row {
  background-color: rgb(213, 134, 120);
  color: white;
}

.el-table .success-row {
  --el-table-tr-background-color: var(--el-color-success-lighter);
}

.el-date-picker .el-picker__popper {
  width: 300px !important;
  height: 300px !important;
  left: 10% !important;
  top: 1% !important;
  margin: 0 !important;
}

.el-picker__popper {
  width: 300px !important;
  height: 300px !important;
  left: 10% !important;
  top: 1% !important;
  margin: 0 !important;
}

div.el-picker-panel.el-date-picker.has-time>div.el-picker-panel__body-wrapper>div>div.el-picker-panel__content>table>tbody>tr>td>div>span {
  position: relative !important;
}

div.el-picker-panel.el-date-picker.has-time>div.el-picker-panel__body-wrapper>div>div.el-picker-panel__content>table>tbody>tr>td {
  padding: 0% !important;
}

div.el-picker-panel.el-date-picker.has-time>div.el-picker-panel__body-wrapper>div>div.el-picker-panel__content>table>tbody>tr>td>div {
  padding: 0% !important;
}


div.el-picker-panel.el-date-picker.has-time>div.el-picker-panel__body-wrapper>div>div.el-date-picker__header {
  margin: 0px;
}

div.el-picker-panel.el-date-picker.has-time>div.el-picker-panel__body-wrapper>div>div.el-date-picker__time-header {
  padding: 0px;
}

div.el-picker-panel.el-date-picker.has-time>div.el-picker-panel__body-wrapper>div>div.el-picker-panel__content>table>tbody>tr>th {
  padding: 0%;
}

div.el-picker-panel.el-date-picker.has-time>div.el-picker-panel__footer {
  padding: 0%;
  border: 0px;
}

section>section>div>div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default>div>main>div>div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default>div>div>div>div.el-card.is-hover-shadow>div>div>div>span {
  font-size: 20px;
}
</style>
