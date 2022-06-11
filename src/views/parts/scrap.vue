<template>
  <div class="system-menu-container">
    <el-card shadow="hover">
      <!-- <el-button icon="el-icon-plus" @click="onOpenAddMenu()" type="success"
        >新增外修记录</el-button
      > -->

      <el-row>
        <!-- <Auths :value="['btn.add', 'btn.other']">
          <el-button @click="onOpenAddMenu()" type="success"
            >增加保养记录</el-button
          ></Auths
        > -->
        <Auths :value="['btn.add']">
          <el-button @click="exportExcel()" type="primary" plain>导出</el-button>
        </Auths>
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
        stripe
        align="center"
        heigth="300"
        style="width: 100%"
        header-align="center"
        max-height="400"
        fit
        :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }"
      >
        <el-table-column prop="id" label="序号" fixed width="50" align="center">
        </el-table-column>

        <el-table-column prop="user" label="领用人" width="100" align="center">
        </el-table-column>

        <el-table-column prop="use_area" label="领用区域" width="120" align="center">
        </el-table-column>
        <el-table-column prop="use_procline" label="使用产线" width="110" align="center">
        </el-table-column>
        <el-table-column prop="type" label="备件类型" width="80" align="center">
        </el-table-column>
        <el-table-column
          prop="use_part_name"
          label="报废备件名称"
          width="180"
          align="center"
        >
        </el-table-column>
        <el-table-column prop="spec" label="报废备件型号" width="180" align="center">
        </el-table-column>

        <el-table-column prop="use_date" label="领用时间" width="140" align="center">
        </el-table-column>
        <el-table-column lumn prop="use_count" label="报废数量" width="80" align="center">
        </el-table-column>
        <el-table-column
          prop="applyformconfirm"
          label="报废表申请人员"
          width="140"
          align="center"
        >
          <template #default="scope">
            <el-button
              type="success"
              :disabled="scope.row.applyformconfirm == '' ? false : true"
              @click="openapplyconfirm(scope.row)"
              >{{
                scope.row.applyformconfirm == null
                  ? "请确认"
                  : scope.row.applyformconfirm + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>

        <el-table-column
          prop="applyformconfirmdate"
          label="报废申请时间"
          align="center"
          width="140"
        >
        </el-table-column>
        <el-table-column
          prop="scrapconfirm"
          label="报废件确认人员"
          width="140"
          align="center"
        >
          <template #default="scope">
            <el-button
              type="success"
              :disabled="scope.row.scrapconfirm == '' ? false : true"
              @click="openscarpconfirmref(scope.row)"
              >{{
                scope.row.scrapconfirm == ""
                  ? "请确认"
                  : scope.row.scrapconfirm + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>

        <el-table-column
          prop="scrapconfirmdate"
          label="报废件确认时间"
          width="140"
          align="center"
        >
        </el-table-column>

        <el-table-column
          prop="applicantman"
          label="补件申请人"
          width="140"
          align="center"
        >
          <template #default="scope">
            <el-button
              type="success"
              :disabled="scope.row.applicantman == '' ? false : true"
              @click="openscarpapplyconfirmref(scope.row)"
              >{{
                scope.row.applicantman == ""
                  ? "请确认"
                  : scope.row.applicantman + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>

        <el-table-column prop="selectOption" label="补件情况" width="100" align="center">
        </el-table-column>
        <el-table-column
          prop="applicantdate"
          min-width="140"
          align="center"
          label="申请补件时间"
        >
        </el-table-column>

        <el-table-column prop="received" label="到货数量" align="center" width="80">
        </el-table-column>
        <el-table-column prop="new_area" label="新件放置区域" width="180" align="center">
        </el-table-column>
        <el-table-column
          prop="useconfirm"
          label="到件确认人员"
          min-width="140"
          align="center"
        >
          <template #default="scope">
            <el-button
              type="success"
              :disabled="scope.row.useconfirm == '' ? false : true"
              @click="openscarpuseconfirmref(scope.row)"
              >{{
                scope.row.useconfirm == "" ? "请确认" : scope.row.useconfirm + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>

        <el-table-column
          prop="useconfirmdate"
          label="确认时间"
          width="140"
          align="center"
        >
        </el-table-column>
        <el-table-column prop="user_reason" label="原因" width="180" align="center">
        </el-table-column>
        <el-table-column prop="remark" label="备注" width="180" align="center">
        </el-table-column>

        <!-- <el-table-column prop="use_reason" label="操作" min-width="110">
          <el-button icon="el-icon-plus" @click="onOpenAddMenu()" type="success"
            >确认</el-button
          >
        </el-table-column> -->
      </el-table>
      <!-- 分页栏 -->
      <el-pagination
        :page-sizes="[20, 40, 60, 80]"
        :page-size="100"
        layout="total, sizes, prev, pager, next, jumper"
        :total="79"
      >
      </el-pagination>
    </el-card>
    <Applyconfirm ref="applyconfirmref" />
    <Scarpconfirm ref="scarpconfirmref" />
    <Scarpapplyconfirm ref="scarpapplyconfirmref" />
    <Scarpuseconfirm ref="scarpuseconfirmref" />
  </div>
</template>

<script lang="ts" setup>
import Applyconfirm from "./components/scrap/sapplyconfirm.vue";

import Scarpconfirm from "./components/scrap/scarpconfirm.vue";

import Scarpapplyconfirm from "./components/scrap/scarpapplyconfirm.vue";

import Scarpuseconfirm from "./components/scrap/scarpuseconfirm.vue";
import Confirm from "./components/scrap/sconfirm.vue";
// import AddMenu from "./components/parts/addMenu.vue";
import service from "/@/utils/request";
import { ref, reactive, onMounted, toRefs, provide } from "vue";
import { ElMessageBox } from "element-plus";

import { exportTable } from "/@/utils/exportExcel";
const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}备件报废明细`);
};
import { formatDate111 } from "/@/utils/formatTime";

const addrepairref = ref();

const scarpconfirmref = ref();

const applyconfirmref = ref();

const scarpapplyconfirmref = ref();

const scarpuseconfirmref = ref();

const sendselectOption = (v?: any) => {
  console.log("sendselectOption");
  console.log(v);
  console.log(v["id"]);
  console.log(v["selectOption"]);

  // service.get('/api/')
};

// 打开新增菜单弹窗
const openscarpconfirmref = (row?: any) => {
  scarpconfirmref.value.openDialog(row);
};

const openapplyconfirm = (row?: any) => {
  applyconfirmref.value.openDialog(row);

  console.log(applyconfirmref);
};

const openscarpapplyconfirmref = (row?: any) => {
  scarpapplyconfirmref.value.openDialog(row);

  console.log(scarpapplyconfirmref);
};

const openscarpuseconfirmref = (row?: any) => {
  scarpuseconfirmref.value.openDialog(row);

  console.log(scarpuseconfirmref);
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
  loading: true,
  selectvalue: "",
  value: "",
  partslist: [],
  filterTable: null,
  save: false,
  total: 0,
  options: [
    {
      value: "补",
      label: "补",
    },
    {
      value: "不补",
      label: "不补",
    },
  ],
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

const initscrap = async (flag?: any) => {
  let { data: res } = await service.get("/getscrap", {
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

      scrapconfirm: item[9],
      selectOption: item[10],
      selectOptiondate: formatDate111(item[11]),
      applyformconfirm: item[12],
      applicantman: item[13],
      useconfirm: item[14],
      received: item[15],
      new_area: item[16],
      application_data: item[17],

      use_procline: item[18],
      useconfirmdate: formatDate111(item[19]),
      applyformconfirmdate: formatDate111(item[20]),
      scrapconfirmdate: formatDate111(item[21]),
      applicantdate: formatDate111(item[22]),
      remark: item[25],
    };
  });

  state.total = state.partslist.length;

  console.log("报废list");
  console.log(state.partslist);
  getusearea();
};
provide("initscrap", initscrap);
onMounted(initscrap);
const getuse = () => {
  //未确认记录
  initscrap("noconfirm");
};

const getalluse = () => {
  //所有记录
  initscrap("all");
};

const find = () => {
  console.log("state.start");
  console.log(state.start);
  console.log(state.end);
  service
    .get("/getscrap", {
      params: {
        flag1: "筛选查询",
        start: state.start,
        end: state.end,
        prolince: state.selectprolince,
        area: state.selectarea,
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
          scrapconfirm: item[9],
          selectOption: item[10],
          selectOptiondate: formatDate111(item[11]),
          applyformconfirm: item[12],
          applicantman: item[13],
          useconfirm: item[14],
          received: item[15],
          new_area: item[16],
          application_data: item[17],
          use_procline: item[18],
          useconfirmdate: formatDate111(item[19]),
          applyformconfirmdate: formatDate111(item[20]),
          scrapconfirmdate: formatDate111(item[21]),
          applicantdate: formatDate111(item[22]),
          remark: item[25],
        };
      });

      console.log("state.partslist");
      console.log(state.partslist);
      state.total = state.partslist.length;
    })
    .catch((err) => {});
};
</script>

<style scoped lang="scss">
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
</style>
