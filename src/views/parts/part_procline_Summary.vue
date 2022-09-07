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
    { title: "备件类型", key: "type", type: "text" },
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
  partslist1: [] as any,
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
  selectType: '',
  Types: [
    {
      value: "减速机",
      label: "减速机",
    },
    {
      value: "升降涡轮蜗杆",
      label: "升降涡轮蜗杆",
    },
    {
      value: "液压马达",
      label: "液压马达",
    },
    {
      value: "转向机",
      label: "转向机",
    }]
});

const exportExcel1 = () => {
  table2excel(
    state.column,
    state.partslist,
    `${formatDate111(new Date())}电器产线汇总.xlsx`
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
    .get("getPart_proclineSummary")
    .then((res:any) => {
      console.log(res);
      state.partslist = res.data.map((item: any) => {
        return {
          area: item[0],
          type:item[1],
          machine_name: item[2],
          YD_01: item[3],
          YD_02: item[4],
          YD_03: item[5],
          YD_04: item[6],
          YD_05: item[7],
          YD_06: item[8],
          FD_01: item[9],
          FD_02: item[10],
          FD_03: item[11],
        };
      });
      state.partslist1=state.partslist
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


const getInfoByType = (val: any) => {


state.partslist1=state.partslist.filter((item:any)=>{
  return item.type.indexOf(val)!=-1
})
}
</script>

<template>
  <div class="system-menu-container">
         <el-row :gutter="50">
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6">
          <el-select v-model="state.selectType" clearable placeholder="选择类型" @change="getInfoByType">
              <el-option v-for="item in state.Types" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
        </el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>

        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.export']">
            <el-button @click="exportExcel1()" type="primary" plain>导出</el-button>
          </Auths>
        </el-col>
      </el-row>
      <br />

    <el-card shadow="always">
 
      <el-table
        id="outtable"
        v-loading="state.loading"
        :data="state.partslist1"
        border
        stripe
        align="center"
        heigth="500"
        header-align="center"
        max-height="500"
        fit
        style="width:100% ;"
        :highlight-current-row="true"
        :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }"
        row-key="id"
        :span-method="objectSpanMethod1"
      >
     
          <el-table-column type="index"  width="50" align="center"  fixed>
          </el-table-column>
  
          <el-table-column  prop="area" width="80" label="区域" align="center" fixed>
          </el-table-column>
        
            <el-table-column  prop="type" width="80" label="备件类型" align="center" >
          </el-table-column>
          <el-table-column prop="machine_name" align="center" label="名称" width="200" >
          </el-table-column>

          <!-- <el-table-column
            prop="machine_spesc"
            align="center"
            label="规格型号"
            width="auto"
          > -->
          <el-table-column prop="YD_01" align="center" label="圆镀一线" width="210">
          </el-table-column>
          <el-table-column prop="YD_02" align="center" label="圆镀二线" width="210">
          </el-table-column>
          <el-table-column prop="YD_03" align="center" label="圆镀三线" width="210">
          </el-table-column>
          <el-table-column prop="YD_04" align="center" label="圆镀四线" width="210">
          </el-table-column>
          <el-table-column prop="YD_05" align="center" label="圆镀五线" width="210">
          </el-table-column>

          <el-table-column prop="YD_06" align="center" label="圆镀六线" width="210">
          </el-table-column>

          <el-table-column prop="FD_01" align="center" label="方镀一线" width="210">
          </el-table-column>
          <el-table-column prop="FD_02" align="center" label="方镀二线" width="210">
          </el-table-column>
          <el-table-column prop="FD_03" align="center" label="方镀三线" width="210">
          </el-table-column>
      
      </el-table>
  
    </el-card>
  </div>
</template>

<style lang="scss" scoped>
#outtable > div.el-table__header-wrapper > table > thead > tr:nth-child(1) > th > div {
  font-size: 50px;
  size: 50px;
}
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


</style>
