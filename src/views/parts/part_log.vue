<template>
  <div class="system-menu-container">
    <el-card shadow="hover">
      <el-table
        id="outTable"
        v-loading="state.loading"
        :data="state.partslist"
        border
        show
        align="center"
        height="600"
        style="width: 100%"
        header-align="center"
        max-height="900"
        fit
        :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }"
        size="mini"
        show-summary
        row-key="id"
      >
        <el-table-column prop="id" label="序号" fixed width="50" align="center">
        </el-table-column>
        <el-table-column prop="username" label="人员" width="180" align="center">
        </el-table-column>

        <el-table-column prop="area" label="区域" width="180" align="center">
        </el-table-column>

        <el-table-column prop="spec" label="规格型号" width="180" align="center">
        </el-table-column>
        <el-table-column prop="item_name" label="规格名称" width="200" align="center">
        </el-table-column>

        <el-table-column prop="count" min-width="150" align="center" label="数量">
        </el-table-column>
        <el-table-column
          prop="create_date"
          label="新增时间"
          min-width="100"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="update_date"
          label="更新时间"
          min-width="100"
          align="center"
        >
        </el-table-column>
        <el-table-column prop="flag" label="操作" width="100" align="center">
        </el-table-column>
        <el-table-column prop="remark" label="备注" width="100" align="center">
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :page-size="state.pagearray"
        @prev-click="prev()"
        @next-click="next()"
        layout="total, sizes, prev, pager, next, jumper"
        :total="state.total"
        prev-text="上一页"
        next-text="下一页"
        :pageSize="state.pagesize"
        :page-count="state.pagecount"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import table2excel from "js-table2excel";
import Auths from "/@/components/auth/auths.vue";
import service from "/@/utils/request";
import { ref, reactive, onMounted, toRefs, onUnmounted } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { formatDate111 } from "/@/utils/formatTime";
import { exportTable } from "/@/utils/exportExcel";
import { Session } from "/@/utils/storage";

const IsPC = () => {
  var sUserAgent = navigator.userAgent.toLowerCase();
  console.log(sUserAgent);
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

const state = reactive({
  areainfo:
    Session.get("userInfo").areainfo == null ? "" : Session.get("userInfo").areainfo,
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
});

// const getusearea = async () => {
//   console.log("执行了 getmachine_usearea");
//   let { data: res } = await service.get(`/getmachine_usearea`);
//   console.log(res);
//   state.ruleForm.userarea = res.map((item: any) => {
//     return {
//       value: item[0],
//       label: item[0],
//     };
//   });
// };

const reciveparts = (page?: any, pagesize?: any) => {
  let res = service
    .get("/get_log", {
      params: {
        currentpagecount: page,
        pagesize: pagesize,
        remark: "电器备件管理",
      },
    })
    .then((res) => {
      console.log("工装管理res = ", res);

      if (res != null) {
        state.pagecount = res.data.pages;
        state.total = res.data.total;
        state.loading = false;
        state.partslist = res.data.map((item: any[]) => {
          return {
            id: item[0],
            username: item[2],
            area: item[3],
            spec: item[4],
            item_name: item[5],

            count: item[6],
            create_date: item[7],
            update_date: item[8],
            flag: item[9],
            remark: item[10],
          };
        });
      }
    })
    .catch((err) => {
      ElMessage({ type: "error", message: err.data });
    });
};

//通过分页返回值

const initpart = () => {
  //置0
  state.partslist = [];
  console.log("执行了 init");

  reciveparts(10, 1);
};

onMounted(() => {
  initpart();
});

const selectparts = async () => {
  let { data: res } = await service.get("/selectmachine", {
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
    };
  });
};

const addClass = ({ row, column, rowIndex, columnIndex }: any) => {
  if (row.balance <= 1) {
    return "warning-row";
  }
};

const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}机修备件明细`);
};
const exportExcel1 = () => {
  console.log(table2excel);
  table2excel(
    state.column,
    state.partslist,
    `${formatDate111(new Date())}机修备件明细.xlsx`
  );
};

// const getSummaries = (param: any) => {
//   const { columns, data } = param;
//   const sums: any[] = [];
//   columns.forEach((column: any, index: any) => {
//     if (index === 0) {
//       sums[index] = "合计";
//       return;
//     }
//     if (index === 1 || index === 2 || index === 3 || index === 4 || index === 5) {
//       sums[index] = "";
//     } else {
//       const values = data.map((item: any) => Number(item[column.property]));
//       if (!values.every((value: any) => isNaN(value))) {
//         sums[index] = `${values.reduce((prev: any, curr: any) => {
//           const value = Number(curr);
//           if (!isNaN(value)) {
//             return prev + curr;
//           } else {
//             return prev;
//           }
//         }, 0)}`;
//       } else {
//         sums[index] = "";
//       }
//     }
//   });

//   return sums;
// };
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

.el-table .warning-row2 {
  background-color: rgb(88, 199, 78);
  color: white;
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
</style>
