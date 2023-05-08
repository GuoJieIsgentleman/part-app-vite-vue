<template>
  <div class="system-menu-container">
    <el-card shadow="hover">


      <el-row :gutter="24">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="24" :xl="24">
          <!-- 
          <el-tag type="danger" style="background-color: rgb(218, 94, 72); color: white">
            试机12小时未确认显示红色</el-tag> -->
        </el-col>
      </el-row>
      <el-row :gutter="35">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="20" :xl="12">
          <div>
            <el-date-picker size="mini" class="timestyle" v-model="state.start" type="datetime" placeholder="选择开始日期"
              format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD H H:mm:ss">
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
              <el-option v-for="item in state.useareas" :key="item['value']" :label="item['label']"
                :value="item['value']">
              </el-option>
            </el-select>

          </div>
        </el-col>
        <el-col class="mb20" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
          <Auths :value="['btn.add']">
            <el-button @click="exportExcel()" type="primary" plain>导出</el-button>
          </Auths>
        </el-col>
        <el-col class="mb20" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
      </el-row>
      <el-button type="primary" @click="find">查询</el-button>
      <el-button @click="getalluse()" type="success" plain>查询全部记录</el-button>
      <el-button @click="getuse()" type="success" plain>查询未确认</el-button>
      <el-table id="outTable" v-loading="state.loading" :data="state.partslist" border align="center" heigth="300"
        style="width: 100%" header-align="center" max-height="400" fit :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }" :row-class-name="addClass">
        <el-table-column prop="id" label="序号" fixed width="50" align="center">
        </el-table-column>
        <el-table-column prop="user" label="领用人" width="65" align="center">
        </el-table-column>
        <el-table-column prop="use_area" min-width="150" align="center" label="领用区域">
        </el-table-column>
        <el-table-column prop="use_procline" label="使用产线" width="80" align="center">
        </el-table-column>

        <el-table-column prop="type" label="备件类型" width="70" align="center">
        </el-table-column>
        <el-table-column prop="use_part_name" label="外修备件名称" align="center" width="120">
        </el-table-column>
        <el-table-column prop="spec" label="外修备件型号" align="center" width="180">
        </el-table-column>

        <el-table-column prop="site_use" label="使用部位" align="center" width="120">
        </el-table-column>
        <el-table-column prop="use_date" label="领用时间" align="center" width="140">
        </el-table-column>
        <el-table-column prop="use_count" label="外修数量" align="center" width="80">
        </el-table-column>


        <el-table-column prop="useconfirm" align="center" label="确认" min-width="140">
          <template #default="scope">
            <el-button :disabled="scope.row.useconfirm == null ? false : true" @click="onOpenconfirmref(scope.row)"
              type="danger">{{
                scope.row.useconfirm == null ? "待确认" : scope.row.useconfirm + "已确认"
              }}</el-button>
          </template>
        </el-table-column>

        <el-table-column prop="useconfirmdate" align="center" label="确认时间" width="140">
        </el-table-column>
        <el-table-column prop="remark" align="center" label="备注" width="180">
        </el-table-column>
        <el-table-column prop="handle" align="center" label="处理方式" width="130">
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
    </el-card>

    <Confirm ref="confirmref" />
  </div>
</template>

<script lang="ts" setup>
import Confirm from "./components/repair/reconfirm.vue";

import service from "/@/utils/request";

import { formatDate111, subtimehours } from "/@/utils/formatTime";

import { ref, reactive, onMounted, toRefs, provide } from "vue";

import { exportTable } from "/@/utils/exportExcel";

import { getElectronArea, ListItem, use_proline_options } from "/@/hooks/getHgInfo";

const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}备件外修明细`);
};

const addrepairref = ref();

const confirmref = ref();

// 打开新增菜单弹窗

const onOpenAddMenu = (row?: any) => {
  addrepairref.value.openDialog(row);
};

const onOpenconfirmref = (row?: any) => {
  confirmref.value.openDialog(row);
};


onMounted(async () => {
  state.use_proline_options = await use_proline_options()

  state.useareas = await getElectronArea()
})


const state = reactive({
  options: [
    {
      value: "是",
      label: "是",
    },
    {
      value: "否",
      label: "否",
    },
  ],
  flag1: "",
  use_proline_options: [] as Array<ListItem>,
  selectarea: "",
  useareas: [] as Array<ListItem>,
  selectprolince: "",
  start: "",
  end: "",
  partslist: [],
  filterTable: null,
  save: false,
  total: 0,
  loading: true,
});


const conversion = (res: any) => {
  state.partslist = res.map((item: any[]) => {
    return {
      id: item[0],
      user: item[1],
      use_area: item[2],
      type: item[3],
      spec: item[4],
      use_part_name: item[5],
      site_use: item[6],
      use_count: item[7],
      use_reason: item[8],
      use_date: formatDate111(item[9]),
      useconfirm: item[10],
      useconfirmdate: formatDate111(item[11]),
      new_area: item[12],
      use_procline: item[13],
      remark: item[14],
      handle: item[15],
      create_date: item[16]
    };
  });
}


const initrepair = async (flag?: any) => {
  let { data: res } = await service.post("/hg_getrepair", {
    flag: flag,
  });
  if (res != null) {
    state.loading = false;
  }
  conversion(res)

  state.total = state.partslist.length;

};
provide("initrepair", initrepair);
onMounted(initrepair);
const addClass = ({ row, rowIndex }: any) => {
  //如果时间相差3小时 就提示颜色
  let timesub = subtimehours(row.receiptdate);
  let timesub1 = subtimehours(row.use_date);
  let timesub2 = subtimehours(row.tryoutdate);
  if (timesub >= 24 && row.tryout == "") {
    return "warning-row";
  }

  if (timesub1 >= 72 && row.applicant == "") {
    return "warning-row2";
  }
  if (timesub2 >= 12 && row.useconfirm == "") {
    return "warning-row1";
  }
};

const getuse = () => {
  //未确认记录
  initrepair("noconfirm");
};

const getalluse = () => {
  //所有记录
  initrepair("all");
};

const find = () => {
  console.log("state.start");
  console.log(state.start);
  console.log(state.end);
  service.post("/hg_getrepair", {
    flag1: "筛选查询",
    start: state.start,
    end: state.end,
    prolince: state.selectprolince,
    area: state.selectarea,
    flag: state.flag1,
  })
    .then((res) => {
      console.log("筛选查询");
      console.log(res);
      if (res != null) {
        state.loading = false;
      }
      conversion(res)
      state.total = state.partslist.length;
    })
    .catch((err) => { });
};
</script>

<style lang="scss" scoped>
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
  background-color: rgb(74, 89, 202);
  color: white;
}

.el-table .warning-row1 {
  background-color: rgb(218, 94, 72);
  color: white;
}

.el-table .warning-row2 {
  background-color: rgb(151, 226, 144);

  color: white;
}

.el-table tbody tr:hover>td {
  background-color: #96b7dc !important;
  color: black;
}

.el-date-picker .el-picker__popper {
  width: 280px !important;
  height: 280px !important;
  left: 2% !important;
  top: 1% !important;
  margin: 0 !important;
}

.el-picker__popper {
  width: 280px !important;
  height: 280px !important;
  left: 2% !important;
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
  font-size: 18px;
}
</style>
