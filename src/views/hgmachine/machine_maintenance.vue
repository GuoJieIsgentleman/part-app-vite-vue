<template>
  <div class="system-menu-container">
    <el-card shadow="hover">

      <el-row :gutter="24">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
          <el-tag style="background-color: rgb(27, 111, 201); color: white">
            领用48小时未保养显示蓝色</el-tag>
          <el-tag style="background-color: rgb(186, 42, 27); color: white">
            保养24小时未确认显示红色</el-tag>
        </el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
          <Auths :value="['btn.add']">
            <el-button @click="exportExcel()" type="primary" plain>导出</el-button>
          </Auths>
        </el-col>
      </el-row>
      <el-row :gutter="35">
        <el-col :span="12" :xs="15" :sm="12" :md="12" :lg="20" :xl="12">
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

      <el-table id="outTable" v-loading="state.loading" :data="state.partslist" border align="center" heigth="300"
        style="width: 100%" header-align="center" max-height="400" fit :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }" :row-class-name="addClass">
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
        <el-table-column prop="use_part_name" align="center" label="保养备件名称" width="180">
        </el-table-column>
        <el-table-column prop="spec" align="center" label="保养备件型号" width="180">
        </el-table-column>
        <el-table-column prop="site_use" align="center" label="使用部位" width="120">
        </el-table-column>
        <el-table-column prop="use_date" align="center" label="领用时间" width="140">
        </el-table-column>

        <el-table-column prop="use_count" align="center" label="保养数量" width="80">
        </el-table-column>
        <el-table-column align="center" prop="useconfirm" label="确认人" width="140">
          <template #default="scope">
            <el-button type="success" :disabled="scope.row.useconfirm == null ? false : true"
              @click="confirm(scope.row)">{{
                scope.row.useconfirm == null
                ? "待确认"
                : scope.row.useconfirm + "已确认"
              }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="useconfirmdate" align="center" label="确认时间" min-width="140">
        </el-table-column>

        <el-table-column prop="new_area" min-width="150" align="center" label="保养完成搁置区域">
        </el-table-column>


        <el-table-column prop="remark" align="center" label="保养备注" min-width="110">
        </el-table-column>
        <el-table-column prop="handle" align="center" label="处理类型" min-width="110">
        </el-table-column>
        <el-table-column prop="create_date" align="center" label="创建时间" min-width="110">
        </el-table-column>
      </el-table>

    </el-card>

    <Confirm ref="ConfirmRef" @confirm="getconfirm" />

  </div>
</template>

<script lang="ts" setup>
import Auths from "/@/components/auth/auths.vue";
import Confirm from "./components/machine_maintenance/mconfirm.vue";
import service from "/@/utils/request";

import { ref, reactive, onMounted, toRefs, provide, computed } from "vue";
import { ElMessage } from "element-plus";
import { formatDate111, subtimehours } from "/@/utils/formatTime";
import { exportTable } from "/@/utils/exportExcel";
import { ListItem, use_proline_options, getElectronArea, getMachineArea } from "/@/hooks/getHgInfo";

const state = reactive({
  use_proline_options: [] as Array<ListItem>,
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
  selectarea: "",
  useareas: [] as Array<ListItem>,
  selectprolince: "",
  start: "",
  end: "",
  istrue: false,
  partslist: [] as Array<object>,
  total: 0,
  filterTable: null,
  save: false,
  confirm: "",
  loading: true,
});
const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}备件保养明细`);
};

const addmaintenanceRecored = ref();

const addConfirm = ref();
const ConfirmRef = ref()
console.log("addConfirm.value.name");

// 打开新增菜单弹窗
const openconfirm = (ROW: any) => {
  addConfirm.value.openDialog(ROW);
};



interface RowData {
  id: number,
  user: string,
  use_area: string,
  type: string,
  spec: string,
  use_part_name: string,
  use_count: string,
  use_reason: string,
  use_date: string,
  useconfirm: string,
  new_area: string,
  useconfirmdate: string,
  use_procline: string,
  remark: string,
  handle: string,
  site_use: string
}

/* 
  打开确认按钮
*/
const confirm = (ROW: RowData) => {
  ConfirmRef.value.openDialog(ROW)
}

const onOpenAddMenu = (ROW?: any) => {
  addmaintenanceRecored.value.openDialog(ROW);
};


onMounted(() => {
  getUse_proline_options()
  getUse_area()
})

const getUse_proline_options = async () => { state.use_proline_options = await use_proline_options() }


const getUse_area = async () => { state.useareas = await getMachineArea() }


const getconfirm = (v: any) => {
  console.log("v");
  console.log(v);
};


//复用返回值

const resdata = (res: Array<Array<any>>) => {
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
      new_area: item[10],
      useconfirmdate: formatDate111(item[11]),
      use_procline: item[12],
      remark: item[13],
      handle: item[14],
      create_date: formatDate111(item[15]),
      site_use: item[16]
    };
  });

  state.total = state.partslist.length;
};

//初始化领用记录
const initmaintenance = async (flag?: any) => {
  let { data: res } = await service.get("/hg_getMachineMaintenance", {
    params: {
      flag: flag,
    },
  });

  console.log('res', res);


  if (res != null) {
    state.loading = false;
  }
  resdata(res);
  console.log("state.partslist");
  console.log(state.partslist);

};

// const getwukucun = () => {
//   let res = service
//     .get("/hg_getMachineMaintenance", {
//       params: {
//         flag: "无库存备件保养记录",
//         flag1: "筛选查询",
//       },
//     })
//     .then((res) => {
//       if (res != null) {
//         state.loading = false;
//       }
//       resdata(res.data);
//     })
//     .catch((err) => {
//       ElMessage({ type: "error", message: err.data });
//     });
// };

provide("initmaintenance", initmaintenance);
onMounted(initmaintenance);

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
  initmaintenance("noconfirm");
};

const getalluse = () => {
  //所有记录
  initmaintenance("all");
};

const find = () => {
  console.log("state.start");
  console.log(state.start);
  console.log(state.end);
  service
    .get("/hg_getMachineMaintenance", {
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
      state.total = state.partslist.length;
    })
    .catch((err) => { });
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

.el-table tbody tr:hover>td {
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
