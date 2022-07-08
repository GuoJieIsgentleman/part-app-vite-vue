<script setup lang="ts">
import { ref, reactive, h, onMounted } from "vue";
import table2excel from "js-table2excel";
import { formatDate111 } from "/@/utils/formatTime";
import service from "/@/utils/request";
import { ElMessage, ElMessageBox } from "element-plus";
import { exportTable } from "/@/utils/exportExcel";
// import { setExport2Excel } from "../../utils/excel.js";
import FileSaver from "file-saver";
import * as XLSX from "xlsx";
const state = reactive({
  column: [
    { title: "序号", key: "index", type: "text" },
    { title: "区域", key: "area", type: "text" },
    { title: "类别", key: "type", type: "text" },
    { title: "备件名称", key: "machine_name", type: "text" },
    { title: "圆镀一线", key: "YD_01", type: "text" },
    { title: "圆镀二线", key: "YD_02", type: "text" },
    { title: "圆镀三线", key: "YD_03", type: "text" },
    { title: "圆镀四线", key: "YD_04", type: "text" },
    { title: "圆镀五线", key: "YD_05", type: "text" },
    { title: "圆镀六线", key: "YD_06", type: "text" },
    { title: "方镀一线", key: "FD_01", type: "text" },
    { title: "方镀二线", key: "FD_02", type: "text" },
    { title: "方镀三线", key: "FD_03", type: "text" },
  ],
  partslist: [] as any,
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
  ],
  selectprolince: "",
  loading: "",
  line: "",
  spanArr: [] as any,
  pos: 0,
});

const exportExcel1 = () => {
  table2excel(
    state.column,
    state.partslist,
    `${formatDate111(new Date())}机修产线汇总.xlsx`
  );
};

const exportExcel2 = () => {
  var dd = document.querySelector("#outtable");
  console.log(dd)
};

const exportClick = () => {
  var wb = XLSX.utils.table_to_book(document.querySelector("#outtable")); //关联don节点
  /* get binary string as output */
  var wbout = XLSX.write(wb, {
    bookType: "xlsx",
    bookSST: true,
    type: "array",
  });
  try {
    FileSaver.saveAs(
      new Blob([wbout], {
        type: "application/octet-stream",
      }),
      "机修备件明细.xlsx"
    ); //自定义文件名
  } catch (e) {
    if (typeof console !== "undefined") console.log(e, wbout);
  }
  return wbout;
};

onMounted(() => {
  getpartslist();
});

const getpartslist = () => {
  service
    .get("getMachine_proclineSummary")
    .then((res) => {
      console.log(res);
      state.partslist = res.data.map((item: any) => {
        return {
          area: item[0],
          machine_name: item[1],
          YD_01: item[2],
          YD_02: item[3],
          YD_03: item[4],
          YD_04: item[5],
          YD_05: item[6],
          YD_06: item[7],
          FD_01: item[8],
          FD_02: item[9],
          FD_03: item[10],
        };
      });

      getSpanArr();
    })
    .catch((err) => {
      ElMessageBox({ type: "error", message: "异常err" + err });
    });
};

const objectSpanMethod1 = ({ row, column, rowIndex, columnIndex }: any) => {
  if (columnIndex == 1) {
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

const getSpanArr = () => {
  state.spanArr = [];
  state.pos = 0;
  console.log("state.partslist");
  console.log(state.partslist);
  let order = 1;
  state.partslist.map((item: any, i: any) => {
    if (i === 0) {
      state.spanArr.push(1);
      state.pos = 0;
      state.partslist[i].order = order;
    } else {
      // 判断当前元素与上一个元素是否相同
      if (item.area === state.partslist[i - 1].area) {
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
};
</script>

<template>
  <div class="system-menu-container">
    <el-card shadow="always">
      <el-row :gutter="50">
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>

        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.add']">
            <el-button @click="exportExcel1()" type="primary" plain>导出</el-button>
          </Auths>
        </el-col>
      </el-row>
      <br />

      <el-table
        id="outtable"
        v-loading="state.loading"
        :data="state.partslist"
        border
        align="center"
        heigth="500"
        header-align="center"
        max-height="500"
        fit
        :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }"
        row-key="id"
        :span-method="objectSpanMethod1"
      >
        <el-table-column label="镀锌车间设备台账清单" align="center" width="auto">
          <el-table-column type="index" fixed width="50" align="center">
          </el-table-column>
          <!-- <el-table-column prop="procline" label="产线" width="80" align="center">
          </el-table-column> -->
          <el-table-column prop="area" width="80" label="区域" align="center">
          </el-table-column>
          <el-table-column prop="type" label="类别" width="100" align="center">
          </el-table-column>

          <el-table-column prop="machine_name" align="center" label="名称" width="auto">
          </el-table-column>

          <!-- <el-table-column
            prop="machine_spesc"
            align="center"
            label="规格型号"
            width="auto"
          > -->
          <el-table-column prop="YD_01" align="center" label="圆镀一线" width="auto">
          </el-table-column>
          <el-table-column prop="YD_02" align="center" label="圆镀二线" width="auto">
          </el-table-column>
          <el-table-column prop="YD_03" align="center" label="圆镀三线" width="auto">
          </el-table-column>
          <el-table-column prop="YD_04" align="center" label="圆镀四线" width="auto">
          </el-table-column>
          <el-table-column prop="YD_05" align="center" label="圆镀五线" width="auto">
          </el-table-column>

          <el-table-column prop="YD_06" align="center" label="圆镀六线" width="auto">
          </el-table-column>

          <el-table-column prop="FD_01" align="center" label="方镀一线" width="auto">
          </el-table-column>
          <el-table-column prop="FD_02" align="center" label="方镀二线" width="auto">
          </el-table-column>
          <el-table-column prop="FD_03" align="center" label="方镀三线" width="auto">
          </el-table-column>
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
      <!-- <el-pagination
        :page-sizes="[20, 40, 60, 80]"
        :page-size="100"
        layout="total, sizes, prev, pager, next, jumper"
        :total="state.total"
      >
      </el-pagination> -->
    </el-card>
  </div>
</template>

<style lang="scss" scoped>
#outtable > div.el-table__header-wrapper > table > thead > tr:nth-child(1) > th > div {
  font-size: 50px;
  size: 50px;
}
</style>
