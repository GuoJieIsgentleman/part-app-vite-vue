<template>
  <div class="system-menu-container">
    <el-card shadow="hover">
      <!-- <el-button icon="el-icon-plus" @click="onOpenAddMenu()" type="success"
        >新增外修记录</el-button
      > -->
      <el-row :gutter="24">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <!-- <Auths :value="['btn.add', 'btn.other']">
          <el-button @click="onOpenAddMenu()" type="success"
            >增加保养记录</el-button
          ></Auths
        > -->
          <Auths :value="['btn.add', 'btn.other']">
            <el-button @click="onOpenAddMenu()" type="danger"
              >增加无库存备件外修记录</el-button
            >
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
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="24" :xl="24">
          <el-tag type="danger" style="background-color: rgb(83, 181, 74); color: white">
            领用72小时未申请外修显示绿色</el-tag
          >
          <el-tag type="danger" style="background-color: rgb(74, 89, 202); color: white">
            收货24小时未试机显示蓝色</el-tag
          >
          <el-tag type="danger" style="background-color: rgb(218, 94, 72); color: white">
            试机12小时未确认显示红色</el-tag
          >
        </el-col>
      </el-row>
      <el-row :gutter="35">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="20" :xl="12">
          <div>
            <el-date-picker
              size="mini"
              class="timestyle"
              v-model="state.start"
              type="datetime"
              placeholder="选择开始日期"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD H H:mm:ss"
            >
            </el-date-picker>
            <el-date-picker
              size="mini"
              v-model="state.end"
              type="datetime"
              placeholder="选择结束日期"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
            >
            </el-date-picker>
            <el-select v-model="state.selectprolince" clearable placeholder="选择产线">
              <el-option
                v-for="item in state.use_proline_options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
            <el-select v-model="state.selectarea" clearable placeholder="领用区域">
              <el-option
                v-for="item in state.useareas"
                :key="item['value']"
                :label="item['label']"
                :value="item['value']"
              >
              </el-option>
            </el-select>
            <el-select v-model="state.flag1" clearable placeholder="是否无库存外修记录">
              <el-option
                v-for="item in state.options"
                :key="item['value']"
                :label="item['label']"
                :value="item['value']"
              >
              </el-option>
            </el-select>
          </div>
        </el-col>
        <el-col class="mb20" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
        <el-col class="mb20" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
      </el-row>
      <el-button type="primary" @click="find">查询</el-button>
      <el-button @click="getalluse()" type="success" plain>查询全部记录</el-button>
      <el-button @click="getuse()" type="success" plain>查询未确认</el-button>
      <el-table
        id="outTable"
        v-loading="state.loading"
        :data="state.partslist"
        border
        align="center"
        heigth="300"
        style="width: 100%"
        header-align="center"
        max-height="400"
        fit
        :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }"
        :row-class-name="addClass"
      >
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
        <el-table-column
          prop="use_part_name"
          label="外修备件名称"
          align="center"
          width="180"
        >
        </el-table-column>
        <el-table-column prop="spec" label="外修备件型号" align="center" width="180">
        </el-table-column>
        <el-table-column prop="use_date" label="领用时间" align="center" width="140">
        </el-table-column>
        <el-table-column prop="use_count" label="外修数量" align="center" width="80">
        </el-table-column>

        <el-table-column
          prop="applicant"
          label="外修申请人"
          align="center"
          min-width="140"
        >
          <template #default="scope">
            <el-button
              @click="onOpenapplicantConfirm(scope.row)"
              :disabled="scope.row.applicant == '' ? false : true"
              type="success"
              >{{
                scope.row.applicant == "" ? "请确认" : scope.row.applicant + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>

        <el-table-column
          prop="applicantdate"
          min-width="150"
          align="center"
          label="申请外修时间"
        >
        </el-table-column>

        <el-table-column
          prop="temporary_area"
          align="center"
          label="收货临时存放区"
          width="180"
        >
        </el-table-column>
        <el-table-column
          prop="receipt"
          label="外修收货人员"
          align="center"
          min-width="140"
        >
          <template #default="scope">
            <el-button
              >>>>>>> e5b1217 (gongzhuang) :disabled="scope.row.receipt == '' ? false :
              true" @click="onOpenreceiptconfirm(scope.row)" type="success" >{{
                scope.row.receipt == "" ? "请确认" : scope.row.receipt + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>

        <el-table-column prop="receiptdate" align="center" label="收货时间" width="140">
        </el-table-column>
        <el-table-column
          prop="tryout"
          align="center"
          label="外修试机人员"
          min-width="140"
        >
          <template #default="scope">
            <el-button
              :disabled="scope.row.tryout == '' ? false : true"
              @click="onOpentryoutconfirm(scope.row)"
              type="success"
              >{{
                scope.row.tryout == "" ? "请确认" : scope.row.tryout + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>

        <el-table-column prop="tryoutdate" align="center" label="试机时间" width="140">
        </el-table-column>
        <el-table-column
          prop="new_area"
          min-width="140"
          align="center"
          label="试机完成搁置区域"
        >
        </el-table-column>
        <el-table-column
          prop="useconfirm"
          align="center"
          label="外修确认人员"
          min-width="140"
        >
          <template #default="scope">
            <el-button
              :disabled="scope.row.useconfirm == '' ? false : true"
              @click="onOpenconfirmref(scope.row)"
              type="success"
              >{{
                scope.row.useconfirm == "" ? "请确认" : scope.row.useconfirm + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>

        <el-table-column
          prop="useconfirmdate"
          align="center"
          label="确认时间"
          width="140"
        >
        </el-table-column>
        <el-table-column prop="remark" align="center" label="外修备注" width="180">
        </el-table-column>
        <el-table-column prop="handle" align="center" label="处理方式" width="130">
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
    </el-card>
    <AddrepairRecored ref="addrepairref" />
    <AddMenu ref="addMenuRef" />
    <Tryoutconfirm ref="tryoutconfirmref" />
    <Receiptconfirm ref="receiptconfirmref" />
    <ApplicantConfirm ref="applicantConfirmref" />
    <Confirm ref="confirmref" />
  </div>
</template>

<script lang="ts" setup>
import AddrepairRecored from "./components/repair/addrepairRecored.vue";
import Confirm from "./components/repair/reconfirm.vue";
// import AddMenu from "./components/parts/addMenu.vue";
import service from "/@/utils/request";

import { formatDate111, subtimehours } from "/@/utils/formatTime";

import { ref, reactive, onMounted, toRefs, provide } from "vue";

import Tryoutconfirm from "./components/repair/tryoutconfirm.vue";
import Receiptconfirm from "./components/repair/receiptconfirm.vue";

import { ElMessageBox } from "element-plus";

import { exportTable } from "/@/utils/exportExcel";
const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}备件外修明细`);
};

const addrepairref = ref();
import ApplicantConfirm from "./components/repair/applicantConfirm.vue";

const addMenuRef = ref();
const tryoutconfirmref = ref();
const confirmref = ref();
const receiptconfirmref = ref();

const applicantConfirmref = ref();
// 打开新增菜单弹窗
const onOpentryoutconfirm = (row?: any) => {
  tryoutconfirmref.value.openDialog(row);
};
const onOpenreceiptconfirm = (row?: any) => {
  receiptconfirmref.value.openDialog(row);
};
const onOpenapplicantConfirm = (row?: any) => {
  applicantConfirmref.value.openDialog(row);
};
const onOpenAddMenu = (row?: any) => {
  addrepairref.value.openDialog(row);
};

const onOpenconfirmref = (row?: any) => {
  confirmref.value.openDialog(row);
};

// // 删除当前行
// const onTabelRowDel = (row: object) => {
// 	ElMessageBox.confirm('此操作将永久删除备件信息, 是否继续?', '提示', {
// 		confirmButtonText: '删除',
// 		cancelButtonText: '取消',
// 		type: 'warning',
// 	})
// 		.then(() => {
// 			console.log(row);
// 		})
// 		.catch(() => {});
// };

const handleSizeChange = (val: any) => {};
const handleCurrentChange = (val: any) => {};
const currentPage4 = (val: any) => {
  // console.log(val.area);
};

const filterHandler = (value: any, row: any, column: any) => {};

const clearFilter = () => {};
const resetDateFilter = () => {};
const handleClick = (val: any) => {
  // console.log(val.area);
};
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
  selectarea: "",
  useareas: [],
  selectprolince: "",
  start: "",
  end: "",

  partslist: [],
  filterTable: null,
  save: false,
  total: 0,

  loading: true,
});
// const filterTable = (el: any) => {
// 	console.log(el);
// };

const getusearea = async () => {
  console.log("执行了 getusearea");
  let { data: res } = await service.get(`/getusearea`);
  console.log(res);
  state.useareas = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
};
const initrepair = async (flag?: any) => {
  let { data: res } = await service.get("/getrepair", {
    params: {
      flag: flag,
    },
  });
  if (res != null) {
    state.loading = false;
  }

  state.partslist = res.map((item: any[]) => {
    return {
      id: item[0],
      user: item[1],
      use_area: item[2],
      type: item[3],
      spec: item[4],
      use_part_name: item[5],
      use_count: item[6],
      use_reason: item[7],
      use_date: formatDate111(item[8]),
      useconfirm: item[9],
      applicant: item[10],
      tryout: item[11],
      receipt: item[12],
      new_area: item[13],

      applicantdate: formatDate111(item[14]),
      receiptdate: formatDate111(item[15]),
      tryoutdate: formatDate111(item[16]),
      useconfirmdate: formatDate111(item[17]),
      use_procline: item[18],
      temporary_area: item[20],
      remark: item[21],
      handle: item[22],
    };
  });
  state.total = state.partslist.length;
  getusearea();
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
  service
    .get("/getrepair", {
      params: {
        flag1: "筛选查询",
        start: state.start,
        end: state.end,
        prolince: state.selectprolince,
        area: state.selectarea,
        flag: state.flag1,
      },
    })
    .then((res) => {
      console.log("筛选查询");
      console.log(res);
      if (res != null) {
        state.loading = false;
      }
      state.partslist = res.data.map((item: any[]) => {
        return {
          id: item[0],
          user: item[1],
          use_area: item[2],
          type: item[3],
          spec: item[4],
          use_part_name: item[5],
          use_count: item[6],
          use_reason: item[7],
          use_date: formatDate111(item[8]),
          useconfirm: item[9],
          applicant: item[10],
          tryout: item[11],
          receipt: item[12],
          new_area: item[13],
          applicantdate: formatDate111(item[14]),
          receiptdate: formatDate111(item[15]),
          tryoutdate: formatDate111(item[16]),
          useconfirmdate: formatDate111(item[17]),
          use_procline: item[18],
          temporary_area: item[20],
          remark: item[21],
        };
      });

      console.log("state.partslist");
      console.log(state.partslist);
      state.total = state.partslist.length;
    })
    .catch((err) => {});
};
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

.el-table tbody tr:hover > td {
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

div.el-picker-panel.el-date-picker.has-time
  > div.el-picker-panel__body-wrapper
  > div
  > div.el-picker-panel__content
  > table
  > tbody
  > tr
  > td
  > div
  > span {
  position: relative !important;
}

div.el-picker-panel.el-date-picker.has-time
  > div.el-picker-panel__body-wrapper
  > div
  > div.el-picker-panel__content
  > table
  > tbody
  > tr
  > td {
  padding: 0% !important;
}
div.el-picker-panel.el-date-picker.has-time
  > div.el-picker-panel__body-wrapper
  > div
  > div.el-picker-panel__content
  > table
  > tbody
  > tr
  > td
  > div {
  padding: 0% !important;
}

div.el-picker-panel.el-date-picker.has-time
  > div.el-picker-panel__body-wrapper
  > div
  > div.el-picker-panel__content
  > table {
}

div.el-picker-panel.el-date-picker.has-time
  > div.el-picker-panel__body-wrapper
  > div
  > div.el-date-picker__header {
  margin: 0px;
}
div.el-picker-panel.el-date-picker.has-time
  > div.el-picker-panel__body-wrapper
  > div
  > div.el-date-picker__time-header {
  padding: 0px;
}

div.el-picker-panel.el-date-picker.has-time
  > div.el-picker-panel__body-wrapper
  > div
  > div.el-picker-panel__content
  > table
  > tbody
  > tr
  > th {
  padding: 0%;
}

div.el-picker-panel.el-date-picker.has-time > div.el-picker-panel__footer {
  padding: 0%;
  border: 0px;
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
  > div.el-card.is-hover-shadow
  > div
  > div
  > div
  > span {
  font-size: 18px;
}
</style>
