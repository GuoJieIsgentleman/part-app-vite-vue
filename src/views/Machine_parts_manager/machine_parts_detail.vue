<template>
  <div class="system-menu-container">
    <el-card shadow="hover">
      <!-- <el-button @click="resetDateFilter">清除日期过滤器</el-button>
      <el-button @click="clearFilter">清除所有过滤器</el-button> -->

      <el-row :gutter="35">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.machine_part_add']">
            <el-button @click="onOpenAddMenu()" type="success">添加成套备件</el-button>
          </Auths>
        </el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.export']">
            <el-button @click="exportExcel1()" type="primary">导出</el-button>
          </Auths>
        </el-col>
      </el-row>
      <el-row :gutter="24">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
          <el-tag type="danger" style="background-color: red; color: white">
            库存数为1时显示红色</el-tag
          >
        </el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
      </el-row>
      <el-select
        v-model="state.part_area_value"
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

      <el-select
        @change="getpartname(state.part_type_value)"
        v-model="state.part_type_value"
        filterable
        placeholder="备件类型"
        clearable
      >
        <el-option
          v-for="item in state.ruleForm.usetype"
          :key="item['value']"
          :label="item['label']"
          :value="item['value']"
        >
        </el-option>
      </el-select>

      <el-select
        v-model="state.part_name_value"
        @change="getspesc(state.part_name_value)"
        filterable
        placeholder="备件名称"
        clearable
      >
        <el-option
          v-for="item in state.ruleForm.part_name"
          :key="item['value']"
          :label="item['label']"
          :value="item['value']"
        >
        </el-option>
      </el-select>
      <el-select
        v-model="state.part_spec_value"
        filterable
        placeholder="规格型号"
        clearable
      >
        <el-option
          v-for="item in state.ruleForm.usespesc"
          :key="item['value']"
          :label="item['label']"
          :value="item['value']"
        >
        </el-option>
      </el-select>

      <el-button @click="selectparts()" type="success">查询</el-button>

      <!-- :row-class-name="tableRowClassName" -->
      <el-table
        id="outTable"
        v-loading="state.loading"
        :data="state.partslist"
        :ref="filterTable"
        :span-method="objectSpanMethod1"
        border
        show
        align="center"
        height="600"
        style="width: 100%"
        header-align="center"
        max-height="900"
        @cell-mouse-enter="cellMouseEnter"
        @cell-mouse-leave="cellMouseLeave"
        fit
        :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }"
        size="mini"
        :row-class-name="addClass"
        show-summary
        :summary-method="getSummaries"
        row-key="id"
      >
        <el-table-column prop="id" label="序号" fixed width="50" align="center">
        </el-table-column>
        <!-- <el-table-column
          show-overflow-tooltip
          prop="machine_part_id"
          label="成套设备id"
          fixed
          width="80"
          align="center"
        >
        </el-table-column> -->

        <el-table-column
          prop="machine_part_name"
          label="成套备件名称"
          width="180"
          align="center"
        >
        </el-table-column>

        <el-table-column prop="type1" label="类型" width="50" align="center">
        </el-table-column>



        <el-table-column prop="part_name" label="单体备件名称" width="200" align="center">
        </el-table-column>
        <el-table-column prop="part_spec" label="规格型号" width="200" align="center">
        </el-table-column>

        <el-table-column
          prop="connection"
          label="机械连接方式"
          width="180"
          align="center"
        >
        </el-table-column>
        <el-table-column prop="partimgsrc" label="图片展示" width="200" align="center">
          <template #default="scope">
            <div v-if="scope.row.partimgsrc != ''">
              <el-image
                style="width: 100px; height: 100px"
                :preview-src-list="[scope.row.partimgsrc]"
                :src="scope.row.partimgsrc"
              >
              </el-image>
            </div>
            <div v-else>
              无图
              <!-- <img :src="scope.row.partimgsrc" alt="" /> -->
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="area" min-width="150" align="center" label="搁置产线区域">
        </el-table-column>

        <el-table-column
          prop="balance"
          label="成套结存剩余（台)"
          min-width="100"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="original"
          label="单体结存剩余（台)"
          min-width="100"
          align="center"
        >
        </el-table-column>
        <el-table-column prop="type" label="备件类型" width="100" align="center">
        </el-table-column>

        <el-table-column label="操作" align="center" width="210">
          <template #default="scope">
         
              <div v-if="scope.row['type1'] == '机械' ? true : false">
                <Auths :value="['btn.edit']" class="btnDisplay">
                <el-button
                  type="primary"
                  size="mini"
                  @click="onEditMenu(scope.row, scope.$index, 0)"
                  >修改</el-button
                >
                </Auths>
                <Auths :value="['btn.del']" class="btnDisplay">
                <el-button
                  type="info"
                  size="mini"
                  @click="onRowDel(scope.row, scope.$index, 0)"
                  >删除</el-button
                >
                </Auths>
              </div>
              <div v-else>
                <Auths :value="['btn.add']" class="btnDisplay">
                <el-button
                  type="success"
                  size="mini"
                  v-if="scope.row['balance'] == 0 ? true : false"
                  @click="onOpenElectricaddMenu(scope.row, scope.$index)"
                  >增加</el-button
                ></Auths>
                   <Auths :value="['btn.edit']" class="btnDisplay">
                <el-button
                  type="warning"
                  size="mini"
                  @click="onEditMenu(scope.row, scope.$index, 1)"
                  >修改</el-button
                ></Auths>
                <Auths :value="['btn.del']" class="btnDisplay">
                <el-button
                  type="danger"
                  size="mini"
                  @click="onRowDel(scope.row, scope.$index, 1)"
                  >删除</el-button
                >
                </Auths>
              </div>
          
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        @prev-click="prev()"
        @next-click="next()"
        layout="total, sizes, prev, pager, next, jumper"
        :total="state.total"
        prev-text="上一页"
        next-text="下一页"
        :page-count="state.pagecount"
      >
      </el-pagination>
    </el-card>
    <AddMenu ref="addMenuRef" />
    <AddElectricMenu ref="addElectricMenuref" />
    <!-- <EditMenu ref="editMenuref" /> -->
    <EditMenu ref="editMenuref" @senddata="setdata" />
  </div>
</template>

<script lang="ts" setup>
import table2excel from "js-table2excel";
import Auths from "/@/components/auth/auths.vue";
import AddMenu from "./components/machine_parts/addMenu.vue";
import EditMenu from "./components/machine_parts/part/editElectricMenu.vue";

// import FileSaver from "file-saver";
// import XLSX2 from "xlsx";
// import XLSX from "xlsx-style";

import AddElectricMenu from "./components/machine_parts/part/addElectricMenu.vue";
import service from "/@/utils/request";
import { ref, reactive, onMounted, toRefs, onUnmounted } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { formatDate111 } from "/@/utils/formatTime";
import { exportTable } from "/@/utils/exportExcel";
import EditElectricMenu1 from "./components/machine_parts/part/editElectricMenu.vue";
const addMenuRef = ref();

const addElectricMenuref = ref();
const editMenuref = ref();
const onOpenElectricaddMenu = (row: object, index: any) => {
  addElectricMenuref.value.openDialog(row, index);
};

const onEditMenu = (row: object, index: any, flag: any) => {
  editMenuref.value.openDialog(row, index, flag);
};

// 打开新增菜单弹窗
const onOpenAddMenu = () => {
  addMenuRef.value.openDialog();
};
// 打开编辑菜单弹窗

const IsPC = () => {
  var sUserAgent = navigator.userAgent.toLowerCase();
};

//分页功能
const prev = () => {
  console.log("前一页");
};
const next = () => {
  console.log("下一页");
};

const handleSizeChange = (val: any) => {
  console.log("每页" + val);
  state.pagesize = val;
  reciveparts(state.pagesize, 1);
  //初始化 页数
};
const handleCurrentChange = (val: any) => {
  console.log("改变页数" + val);
  reciveparts(state.pagesize, val);
};

const onOpenMachineEditMenu = (row: object, index: any) => {
  editMenuref.value.openDialog(row, index);
};

let dom: any = null;

const setdata = (v: any, v1: any) => {

  console.log("设置表格的值");

};

const filterHandler = (value: any, row: any, column: any) => {};

const clearFilter = () => {};
const resetDateFilter = () => {};
const handleClick = (val: any) => {
  // console.log(val.area);
};
const state = reactive({
  column: [
    { title: "序号", key: "id", type: "text" },
    { title: "备件名称", key: "part_name", type: "text" },
    { title: "规格型号", key: "part_spec", type: "text" },
    { title: "机械连接方式", key: "connection", type: "text" },
    { title: "图片展示", key: "partimgsrc", type: "image", width: 200, height: 200 },
    { title: "搁置产线区域", key: "area", type: "text" },
    { title: "结存剩余（台)", key: "balance", type: "text" },
    { title: "原有数量（台)", key: "original", type: "text" },
    { title: "备件类型", key: "type", type: "text" },
  ],
  pagearray: [10, 20, 30, 40, 50],
  ruleForm: {
    model: "",
    model1: "",
    model2: "",
    model3: "",
    usetype: [],
    userarea: [],
    part_name: [],
    usespesc: [],
  },
  part_spec_options: [] as any[],
  part_spec_value: "",
  part_name_value: "",
  part_area_value: "",
  part_type_value: "",
  loading: true,
  part_name_options: [] as any[],
  part_area_options: [] as any[],
  part_type_options: [] as any[],
  part_spec: [],

  partslist: [] as any,
  filterTable: null,
  save: false,
  total: 0,
  pagecount: 0,
  pagesize: 10,
  filte_part_name: [],
  filte_part_spec: [],
  filte_area: [],
  filte_remark: [],
  filte_type: [],
  srcList: [""],
  rowdata: [],
  spanArr: [] as any,
  pos: 0,
  rowIndex: "",
  hoverOrderArr: [],
  orderarray: [] as any,
  cellindex: -1,
});
const filterTable = (el: any) => {};

const getusearea = async () => {
  console.log("执行了 getusearea");
  let { data: res } = await service.get(`/getmachine_part_usearea`);

  state.ruleForm.userarea = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
};

const reciveparts = (page?: any, pagesize?: any) => {
  let res = service
    .get("/getmachine_parts_detail", {
      params: {
        currentpagecount: page,
        pagesize: pagesize,
      },
    })
    .then((res) => {
      if (res != null) {
        state.pagecount = res.data.pages;
        state.total = res.data.total;
        state.loading = false;
        state.partslist = res.data.data1.map((item: any[]) => {
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
            type1: item[10],
            machine_part_name: item[11],
            machine_part_id: item[12],
          };
        });
      }

      getSpanArr();
    })
    .catch((err) => {
      ElMessage({ type: "error", message: err.data });
    });
};

//通过分页返回值

const initpart = () => {
  //置0

  console.log("执行了 initpart");
  getusearea();
  reciveparts(10, 1);
};

//----------------------------------
const gettype = async (value?: any) => {
  //通过area 找type

  let { data: type } = await service.get("/getmachine_part_type");

  state.ruleForm.usetype = type.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
};

//----------------------------------
const getpartname = async (value?: any) => {
  //通过area 找type

  let { data: partname } = await service.get("/getmachine_part_names", {
    params: {
      type: value,
      // spec: state.ruleForm.model2,
    },
  });

  state.ruleForm.part_name = partname.map((item: any) => {
    return {
      value: item[1],
      label: item[1],
      count: item[4],
    };
  });
};
//---------------------------------------

//---------------------------------------

const getspesc = async (value?: any) => {
  //通过area 找type

  let { data: type } = await service.get("/getmachine_part_spesc", {
    params: {
      use_part_name: state.part_name_value,
      type: state.part_type_value,
    },
  });

  state.ruleForm.usespesc = type.map((item: any) => {
    return {
      value: item[2],
      label: item[2],
    };
  });
};

//---------------------------------------

onMounted(() => {
  initpart();

  gettype();
  IsPC();
});
// 删除当前行
const onRowDel = (row: any, index: any, flag: any) => {
  ElMessageBox.confirm("此操作将永久删除备件信息, 是否继续?", "提示", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      console.log(row.part_name);
      service
        .get("/deletemachine_part", {
          params: {
            single_part_name: row.part_name,
            flag: flag,
            part_id: row.id,
          },
        })
        .then((res) => {
          ElMessage({
            message: res.data,
            type: "success",
          });

          initpart();
        })
        .catch((err) => {
          ElMessage({
            message: err.data,
            type: "warning",
          });
        });
    })
    .catch(() => {});
};

// const onElectricRowDel = (row: any, index: any) => {
//   ElMessageBox.confirm("此操作将永久删除备件信息, 是否继续?", "提示", {
//     confirmButtonText: "删除",
//     cancelButtonText: "取消",
//     type: "warning",
//   })
//     .then(() => {
//       service
//         .get("/deletemachine_part", {
//           params: {
//             machine_part_name: row.machine_part_name,
//           },
//         })
//         .then((res) => {
//           ElMessage({
//             message: res.data,
//             type: "success",
//           });

//           initpart();
//         })
//         .catch((err) => {
//           ElMessage({
//             message: err.data,
//             type: "warning",
//           });
//         });
//     })
//     .catch(() => {});
// };

const selectparts = async () => {
  let { data: res } = await service.get("/selectmachine_part", {
    params: {
      part_spec: state.part_spec_value,
      part_name: state.part_name_value,
      area: state.part_area_value,
      type: state.part_type_value,
    },
  });
  state.partslist = res.map((item: any[]) => {
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
      type1: item[10],
      machine_part_name: item[11],
      machine_part_id: item[12],
    };
  });

  getSpanArr();
};

const addClass = ({ row, column, rowIndex, columnIndex }: any) => {
  let r = -1;
  state.partslist.forEach((item: any) => {
    if (state.cellindex === row.order) {
      r = rowIndex;
    }
  });
  if (rowIndex === r && columnIndex != 0) {
    return "warning-row3";
  }
};

const cellMouseEnter = (row: any, column: any, cell: any, event: any) => {
  state.partslist.forEach((item: any) => {
    if (row.order === item.order) {
      state.cellindex = row.order;
    }
  });
};

const cellMouseLeave = (row: any, column: any, cell: any, event: any) => {
  state.cellindex = -1;
};

const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}成套备件明细`);
};
const exportExcel1 = () => {
  table2excel(
    state.column,
    state.partslist,
    `${formatDate111(new Date())}成套备件明细.xlsx`
  );
};

const getSummaries = (param: any) => {
  const { columns, data } = param;
  const sums: any[] = [];
  columns.forEach((column: any, index: any) => {
    if (index === 0) {
      sums[index] = "合计";
      return;
    }
    if (
      index === 1 ||
      index === 2 ||
      index === 3 ||
      index === 4 ||
      index === 5 ||
      index === 6
    ) {
      sums[index] = "";
    } else if (index === 9) {
      const values = data.map((item: any) => Number(item[column.property]));

      if (!values.every((value: any) => isNaN(value))) {
        sums[index] = `${
          values.reduce((prev: any, curr: any) => {
            const value = Number(curr);
            if (!isNaN(value)) {
              return prev + curr;
            } else {
              return prev;
            }
          }, 0) / 2
        }`;
      } else {
        sums[index] = "";
      }
    } else {
      const values = data.map((item: any) => Number(item[column.property]));

      if (!values.every((value: any) => isNaN(value))) {
        sums[index] = `${values.reduce((prev: any, curr: any) => {
          const value = Number(curr);

          if (!isNaN(value)) {
            return prev + curr;
          } else {
            return prev;
          }
        }, 0)}`;
      } else {
        sums[index] = "";
      }
    }
  });

  return sums;
};

const getSpanArr = () => {
  state.spanArr = [];
  state.pos = 0;
  console.log("state.partslist======");

  console.log(state.partslist);
  let order = 1;
  state.partslist.map((item: any, i: never) => {
    if (i === 0) {
      state.spanArr.push(1);
      state.pos = 0;
      state.partslist[i].order = order;
    } else {
      // 判断当前元素与上一个元素是否相同
      if (item.machine_part_id === state.partslist[i - 1].machine_part_id) {
        state.spanArr[state.pos] += 1;
        state.spanArr.push(0);
        state.partslist[i]["order"] = state.partslist[i - 1]["order"] = state.partslist[
          i
        ]["order"]
          ? state.partslist[i]["order"]
          : order;
      } else {
        state.spanArr.push(1);
        state.pos = i;
        order = order + 1;
        state.partslist[i]["order"] = order;
      }
    }
  });

  console.log("state.spanArr======");

  console.log(state.spanArr);

  console.log(state.pos);
  console.log("state.orderarray======");
  console.log(state.partslist);
  // console.log("count.value-------" + count.value);
  // console.log(count.value);
};

const objectSpanMethod1 = ({ row, column, rowIndex, columnIndex }: any) => {
  if (
    columnIndex == 1 ||
    columnIndex == 2 ||
    columnIndex == 6 ||
    columnIndex == 7 ||
    columnIndex == 8 ||
    columnIndex == 9
  ) {
    const _row = state.spanArr[rowIndex];

    const _col = _row > 0 ? 1 : 0;

    return {
      rowspan: _row,
      colspan: _col,
    };
  } else {
    return [1, 1];
  }
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

// .el-table .warning-row {
//   --el-table-tr-background-color: var(--el-color-warning-lighter);
// }

.el-table .warning-row {
  background-color: rgb(208, 58, 58);
  color: white;
}
.el-table .warning-row3 {
  background-color: rgb(150, 183, 220);
  color: rgb(5, 4, 4);
}

.el-table .warning-row2 {
  background-color: rgb(88, 199, 78);
  color: rgb(5, 4, 4);
}
.el-table .success-row {
  --el-table-tr-background-color: var(--el-color-success-lighter);
}
.el-table tbody tr:hover > td {
  background-color: #96b7dc !important;
  color: black;
}

#app > section > div.el-backtop {
  cursor: pointer;
  z-index: 5;
  right: 40px;
  bottom: 40px;
  top: 500px;
}
.btnDisplay{
  display: inline-block;
}
</style>
