<template>
  <div class="system-menu-container">
    <el-card shadow="hover">
      <!-- <el-button @click="resetDateFilter">清除日期过滤器</el-button>
      <el-button @click="clearFilter">清除所有过滤器</el-button> -->

      <el-row :gutter="35">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.tooling_add']">
            <el-button @click="onOpenAddMenu()" type="success">添加工装明细</el-button>
          </Auths>
        </el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.tooling_export']">
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
        :cell-class-name="addClass"
        show-summary
        :summary-method="getSummaries"
        row-key="id"
      >
        <el-table-column type="index" label="序号" fixed width="50" align="center">
        </el-table-column>
        <el-table-column prop="part_name" label="备件名称" width="180" align="center">
        </el-table-column>

        <el-table-column prop="part_spec" label="规格型号" width="180" align="center">
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
          label="结存剩余（台)"
          min-width="100"
          align="center"
        >
        </el-table-column>
        <el-table-column
          prop="original"
          label="原有数量（台)"
          min-width="100"
          align="center"
        >
        </el-table-column>
        <el-table-column prop="type" label="备件类型" width="100" align="center">
        </el-table-column>

        <el-table-column label="操作" align="center" min-width="120">
          <template #default="scope">
            <Auths :value="['btn.edit']" class="displayStyle">
              <el-button
                type="primary"
                @click="onOpenEditMenu(scope.row, scope.$index)"
                icon="el-icon-edit"
            
              ></el-button>
            </Auths>

            <Auths :value="['btn.del']"  class="displayStyle">
              <el-button
                type="warning"
                @click="onTabelRowDel(scope.row, scope.$index)"
                icon="el-icon-delete"
               
              ></el-button>
            </Auths>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :page-sizes="state.pagearray"
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
    <AddMenu ref="addMenuRef" />
    <EditMenu ref="editMenuRef" @senddata="setdata" />
  </div>
</template>

<script lang="ts" setup>
import table2excel from "js-table2excel";
import Auths from "/@/components/auth/auths.vue";
import AddMenu from "/@/views/Tooling_management/components/tooling_detail/addMenu.vue";
import EditMenu from "/@/views/Tooling_management/components/tooling_detail/editMenu.vue";
import service from "/@/utils/request";
import { ref, reactive, onMounted, toRefs, onUnmounted } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { formatDate111 } from "/@/utils/formatTime";
import { exportTable } from "/@/utils/exportExcel";
import { Session } from "/@/utils/storage";
const addMenuRef = ref();
const editMenuRef = ref();

// 打开新增菜单弹窗
const onOpenAddMenu = () => {
  addMenuRef.value.openDialog();
};
// 打开编辑菜单弹窗

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

const onOpenEditMenu = (row: object, index: any) => {
  editMenuRef.value.openDialog(row, index);
};

const setdata = (v: any, v1: any) => {
  //set table 值
  state.partslist[v1].id = v[0][0];
  state.partslist[v1].part_name = v[0][1];
  state.partslist[v1].part_spec = v[0][2];
  state.partslist[v1].area = v[0][3];
  state.partslist[v1].balance = v[0][4];
  state.partslist[v1].original = v[0][5];
  state.partslist[v1].remark = v[0][6];
  state.partslist[v1].type = v[0][7];
  state.partslist[v1].partimgsrc = v[0][8];
  state.partslist[v1].connection = v[0][9];
};

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
const filterTable = (el: any) => {};

const getusearea = async () => {
  console.log("执行了 gettooling_usearea");
  let { data: res } = await service.get(`/gettooling_usearea`);
  console.log(res);
  state.ruleForm.userarea = res.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
};

const reciveparts = (page?: any, pagesize?: any) => {
  let res = service
    .get("/gettooling_detail", {
      params: {
        currentpagecount: page,
        pagesize: pagesize,
      },
    })
    .then((res) => {
      console.log(res);
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
            isShow: checkIsShow(item[3]), //
          };
        });
      }
      console.log("state.partslist");
      console.log(state.partslist);
    })
    .catch((err) => {
      ElMessage({ type: "error", message: err.data });
    });
};

//检查是否能显示
const checkIsShow = (area: any) => {
  let flag = false;

  if (Session.get("userInfo").areainfo == "") {
    return flag;
  }

  if (Session.get("userInfo").authPageList[0] == "admin") {
    return true;
  }
  if (Session.get("userInfo").areainfo) {
    state.areainfo.map((item: any) => {
      if (area.slice(0, 5) == item.slice(0, 5)) {
        flag = true;
      }
    });
  }
  console.log(`${area}+++++++++${flag}`);
  return flag;
};

//通过分页返回值

const initpart = () => {
  //置0
  state.partslist = [];
  console.log("执行了 init machine");
  getusearea();
  reciveparts(10, 1);
};

//----------------------------------
const gettype = async (value?: any) => {
  //通过area 找type

  let { data: type } = await service.get("/gettooling_type");

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

  let { data: partname } = await service.get("/gettooling_name", {
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

  let { data: type } = await service.get("/gettooling_spesc", {
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
const onTabelRowDel = (row: any, index: any) => {
  ElMessageBox.confirm("此操作将永久删除备件信息, 是否继续?", "提示", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      console.log(row);

      console.log("发送删除请求");
      service
        .get("/deletetooling", {
          params: {
            id: row.id,
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

const selectparts = async () => {
  let { data: res } = await service.get("/selecttooling", {
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
      isShow: checkIsShow(item[3]),
    };
  });
};

const addClass = ({ row, column, rowIndex, columnIndex }: any) => {
  if (row.balance <= 1) {
    return "warning-row";
  }
};

const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}工装管理明细`);
};
const exportExcel1 = () => {
  console.log(table2excel);
  table2excel(
    state.column,
    state.partslist,
    `${formatDate111(new Date())}工装管理明细.xlsx`
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
    if (index === 1 || index === 2 || index === 3 || index === 4 || index === 5) {
      sums[index] = "";
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
.displayStyle{
  display: inline-block;
}
</style>
