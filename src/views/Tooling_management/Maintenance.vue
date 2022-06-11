<template>
  <div class="system-menu-container">
    <el-card shadow="hover">
      <el-row :gutter="50">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.tooling_add', 'btn.tooling_other']">
            <el-button @click="onOpenAddMenu()" type="danger"
              >增加无库存备件保养记录</el-button
            ></Auths
          >
        </el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>

        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.tooling_add']">
            <el-button @click="exportExcel()" type="primary" plain>导出</el-button>
          </Auths>
        </el-col>
      </el-row>
      <el-row :gutter="24">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
          <el-tag style="background-color: rgb(27, 111, 201); color: white">
            领用48小时未保养显示蓝色</el-tag
          >
          <el-tag style="background-color: rgb(186, 42, 27); color: white">
            保养24小时未确认显示红色</el-tag
          >
        </el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
      </el-row>
      <el-row :gutter="35">
        <el-col :span="12" :xs="15" :sm="12" :md="12" :lg="20" :xl="12">
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

            <el-select v-model="state.flag1" clearable placeholder="是否无库存保养记录">
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

      <el-row :gutter="50">
        <el-col :span="12" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
          <el-button type="primary" @click="find">查询</el-button>
          <el-button @click="getalluse()" type="success" plain>查询全部记录</el-button>

          <el-button @click="getuse()" type="success" plain>查询未确认</el-button>
        </el-col>
      </el-row>

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
        <el-table-column prop="user" label="领用人" width="80" align="center">
        </el-table-column>
        <el-table-column prop="use_area" align="center" min-width="150" label="领用区域">
        </el-table-column>
        <el-table-column prop="use_procline" align="center" label="使用产线" width="90">
        </el-table-column>

        <el-table-column prop="type" align="center" label="备件类型" width="100">
        </el-table-column>
        <el-table-column
          prop="use_part_name"
          align="center"
          label="保养备件名称"
          width="180"
        >
        </el-table-column>
        <el-table-column prop="spec" align="center" label="保养备件型号" width="180">
        </el-table-column>

        <el-table-column prop="use_date" align="center" label="领用时间" width="150">
        </el-table-column>

        <el-table-column prop="use_count" align="center" label="保养数量" width="80">
        </el-table-column>
        <el-table-column
          align="center"
          prop="maintenance_user"
          label="保养人"
          width="140"
        >
          <template #default="scope">
            <el-button
              type="success"
              :disabled="scope.row.maintenanceman == '' ? false : true"
              @click="openmaintenancemanconfirm(scope.row)"
              >{{
                scope.row.maintenanceman == ""
                  ? "请确认"
                  : scope.row.maintenanceman + "已确认"
              }}</el-button
            >
          </template>
        </el-table-column>
        <el-table-column
          prop="maintenance_user"
          align="center"
          label="保养时间"
          width="150"
        >
          <template #default="scope">
            {{ scope.row.maintenance_date }}
          </template>
        </el-table-column>

        <el-table-column
          prop="new_area"
          min-width="150"
          align="center"
          label="保养完成搁置区域"
        >
        </el-table-column>

        <el-table-column prop="useconfirm" align="center" label="确认人" width="140">
          <template #default="scope">
            <el-button
              type="success"
              :disabled="scope.row.useconfirm == '' ? false : true"
              @click="openconfirm(scope.row)"
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
          min-width="150"
        >
        </el-table-column>
        <el-table-column prop="remark" align="center" label="保养备注" min-width="110">
        </el-table-column>
        <el-table-column prop="handle" align="center" label="处理类型" min-width="110">
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
      <el-pagination
        :page-sizes="[20, 40, 60, 80]"
        :page-size="100"
        layout="total, sizes, prev, pager, next, jumper"
        :total="state.total"
      >
      </el-pagination>
    </el-card>
    <AddmaintenanceRecored ref="addmaintenanceRecored" />
    <AddMenu ref="addMenuRef" />
    <Confirm ref="addConfirm" @confirm="getconfirm" />
    <Maintenanceconfirm ref="maintenanceconfirmref" />
  </div>
</template>

<script lang="ts" setup>
import Auth from "/@/components/auth/auth.vue";
import AddmaintenanceRecored from "/@/views/Tooling_management/components/maintenance/addmaintenanceRecored.vue";

import Maintenanceconfirm from "/@/views/Tooling_management/components/maintenance/maintenanceconfirm.vue";
import Confirm from "/@/views/Tooling_management/components/maintenance/mconfirm.vue";
import service from "/@/utils/request";
import { ref, reactive, onMounted, toRefs, provide } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Console } from "console";
import { formatDate111, subtimehours } from "/@/utils/formatTime";

import { exportTable } from "/@/utils/exportExcel";
const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}机修保养明细`);
};

const addmaintenanceRecored = ref();
const addMenuRef = ref();
const addConfirm = ref();
const maintenanceconfirmref = ref();
console.log("addConfirm.value.name");

// 打开新增菜单弹窗
const openconfirm = (ROW: any) => {
  addConfirm.value.openDialog(ROW);
};

const openmaintenancemanconfirm = (ROW: any) => {
  maintenanceconfirmref.value.openDialog(ROW);
};

const onOpenAddMenu = (ROW?: any) => {
  addmaintenanceRecored.value.openDialog(ROW);
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

const getconfirm = (v: any) => {
  console.log("v");
  console.log(v);
};

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
  istrue: false,
  partslist: [],
  total: 0,
  filterTable: null,
  save: false,
  confirm: "",
  loading: true,
});
// const filterTable = (el: any) => {
// 	console.log(el);
// };
const getusearea = async () => {
  console.log("执行了 gettooling_usearea");
  let { data: res } = await service.get(`/gettooling_usearea`);
  console.log(res);
  state.useareas = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
};

//复用返回值

const resdata = (res: any) => {
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
      maintenanceman: item[10],
      maintenance_date: formatDate111(item[11]),
      new_area: item[12],
      useconfirmdate: formatDate111(item[13]),
      use_procline: item[14],
      remark: item[16],
      handle: item[17],
    };
  });

  state.total = state.partslist.length;
};

//初始化领用记录
const inittooling_maintenance = async (flag?: any) => {
  let { data: res } = await service.get("/gettooling_maintenance", {
    params: {
      flag: flag,
    },
  });

  if (res != null) {
    state.loading = false;
  }
  resdata(res);
  console.log("state.partslist");
  console.log(state.partslist);
  getusearea();
};

const getwukucun = () => {
  let res = service
    .get("/gettooling_maintenance", {
      params: {
        flag: "无库存备件保养记录",
        flag1: "筛选查询",
      },
    })
    .then((res) => {
      if (res != null) {
        state.loading = false;
      }
      resdata(res.data);
    })
    .catch((err) => {
      ElMessage({ type: "error", message: err.data });
    });
};

provide("inittooling_maintenance", inittooling_maintenance);
onMounted(inittooling_maintenance);

const addClass = ({ row, rowIndex }: any) => {
  //如果时间相差3小时 就提示颜色
  let timesub = subtimehours(row.use_date);
  let timesub1 = subtimehours(row.maintenance_date);
  if (timesub >= 48 && row.maintenanceman == "") {
    return "warning-row";
  }
  if (timesub1 >= 24 && row.useconfirm == "") {
    return "warning-row1";
  }
};

const getuse = () => {
  //未确认记录
  inittooling_maintenance("noconfirm");
};

const getalluse = () => {
  //所有记录
  inittooling_maintenance("all");
};

const find = () => {
  console.log("state.start");
  console.log(state.start);
  console.log(state.end);
  service
    .get("/gettooling_maintenance", {
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
      resdata(res.data);

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
  background-color: rgb(12, 80, 151);
  color: white;
}

.el-table .warning-row1 {
  background-color: rgb(202, 34, 34);
  color: white;
}

.el-table tbody tr:hover > td {
  background-color: #96b7dc !important;
  color: black;
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
