<template>
  <el-card shadow="hover">
    <!-- <el-button @click="resetDateFilter">清除日期过滤器</el-button>
      <el-button @click="clearFilter">清除所有过滤器</el-button> -->
    <Auths :value="['btn.add']">
      <el-button @click="exportExcel()" type="success">导出</el-button>
    </Auths>
    <el-button @click="selectparts()" type="success">查询</el-button>

    <!-- :row-class-name="tableRowClassName" -->
    <el-table
      id="outTable"
      v-loading="state.loading"
      :data="state.partslist"
      :ref="inspectionrecord"
      border
      align="center"
      height="600"
      style="width: 100%"
      header-align="center"
      max-height="400"
      fit
      :row-style="{ height: '10px' }"
      :cell-style="{ padding: '5px 0' }"
      size="mini"
    >
      <el-table-column prop="id" label="序号" fixed width="50" align="center">
      </el-table-column>
      <el-table-column prop="inspecter" label="巡检人" width="70" align="center">
      </el-table-column>

      <el-table-column prop="inspect_area" label="巡检区域" width="120" align="center">
      </el-table-column>
      <el-table-column
        prop="start_inspect_date"
        width="140"
        align="center"
        label="巡检开始时间"
      >
      </el-table-column>
      <el-table-column
        prop="end_inspect_date"
        width="140"
        align="center"
        label="巡检结束时间"
      >
      </el-table-column>
      <el-table-column prop="subtime" width="80" align="center" label="巡检时长">
      </el-table-column>
      <el-table-column prop="remark" label="备注" min-width="180" align="center">
      </el-table-column>
      <!-- 
      <el-table-column label="操作" align="center" min-width="120">
        <template #default="scope">
          <Auths :value="['btn.add']">
            <el-button
              type="primary"
              @click="onOpenEditMenu(scope.row)"
              icon="el-icon-edit"
              circle
            ></el-button>
            <el-button
              type="warning"
              @click="onTabelRowDel(scope.row)"
              icon="el-icon-delete"
              circle
            ></el-button>
          </Auths>
        </template>
      </el-table-column> -->
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { ElMessage } from "element-plus";
import { ref, reactive, onMounted, toRefs } from "vue";
import service from "/@/utils/request";
import { formatDate111, subtimeminutes, subtimeminutes1 } from "/@/utils/formatTime";
import { exportTable } from "/@/utils/exportExcel";
const inspectionrecord = ref();
const state = reactive({
  partslist: [],
  loading: false,
});

console.log("时间差");

const initinspectrecord = () => {
  service
    .get("/getinspectionrecord")
    .then((res) => {
      state.partslist = res.data.map((item: any) => {
        return {
          id: item[0],
          start_inspect_date: formatDate111(item[1]),
          end_inspect_date: formatDate111(item[2]),
          inspecter: item[3],
          inspect_area: item[4],
          remark: item[6],
          subtime: subtimeminutes1(formatDate111(item[1]), formatDate111(item[2])),
        };
      });
      console.log("state.partslist巡检时间长");
      console.log(state.partslist);
    })
    .catch((err) => {
      ElMessage({
        message: err.data,
        type: "error",
      });
    });
};

onMounted(initinspectrecord);

const onOpenEditMenu = (row?: any) => {};
const onTabelRowDel = (row?: any) => {};

const exportExcel = (row?: any) => {
  exportTable("#outTable", `${formatDate111(new Date())}巡检记录`);
};
const selectparts = (row?: any) => {};
</script>

<style lang="less">
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
