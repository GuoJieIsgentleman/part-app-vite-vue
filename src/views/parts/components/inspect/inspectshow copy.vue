<template>
  <div class="system-menu-container">
    <el-dialog title="巡检明细" v-model="state.isShowDialog" width="769px">
      <el-table
        :data="state.maintenance_data"
        style="width: 100%"
        v-if="state.isshowmaintenance_data"
      >
        <el-table-column prop="prop" label="label" width="width"> </el-table-column>
      </el-table>
      <el-table
        :data="state.repair_data"
        style="width: 100%"
        v-if="state.isshowrepair_data"
      >
        <el-table-column prop="prop" label="label" width="width"> </el-table-column>
      </el-table>
      <el-table :data="state.part_data" style="width: 100%">
        <el-table-column prop="prop" label="label" width="width"> </el-table-column>
      </el-table>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="state.isShowDialog = false">取消</el-button>
          <el-button type="primary" @click="state.isShowDialog = false">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, onBeforeUpdate, defineEmits } from "vue";
import service from "/@/utils/request";

const state = reactive({
  isshowmaintenance_data: false,
  isshowrepair_data: false,
  isShowDialog: false,
  maintenance_data: [],
  repair_data: [],
  part_data: [],
  resdata: [] as any,
});

onBeforeUpdate(() => {});

const change1 = () => {
  console.log("执行了change");
};

// 打开弹窗
const openDialog = (row?: any) => {
  console.log(row);
  state.isShowDialog = true;
  getinspection(row);
};
// 关闭弹窗
const closeDialog = (row?: object) => {
  console.log(row);
  state.isShowDialog = false;
};
// 是否内嵌下拉改变
// const onSelectIframeChange = () => {
// 	if (state.ruleForm.meta.isIframe === 'true') {
// 		state.ruleForm.isLink = 'true';
// 	} else {
// 		state.ruleForm.isLink = '';
// 	}
// };
// 取消
const onCancel = () => {
  closeDialog();
  initForm();
};
// 新增
const initForm = () => {};

const getinspection = (v: String) => {
  service
    .get("/getinspection", {
      params: {
        cardid: v,
      },
    })
    .then((res) => {
      state.resdata = res.data;
      console.log("state.resdata");
      console.log(state.resdata);
      if (state.resdata["maintenance_data"].length > 0) {
        state.maintenance_data = state.resdata["maintenance_data"].map((item: any) => {
          return {
            id: item[0],
            user: item[1],
            use_area: item[2],
            type: item[3],
            spec: item[4],
            use_part_name: item[5],
            use_count: item[6],
            use_procline: item[14],
          };
        });
        state.isshowmaintenance_data = true;
      }

      if (state.resdata["repair_data"].length > 0) {
        state.repair_data = state.resdata["repair_data"].map((item: any) => {
          return {
            id: item[0],
            user: item[1],
            use_area: item[2],
            type: item[3],
            spec: item[4],
            use_part_name: item[5],
            use_count: item[6],
            use_procline: item[17],
          };
        });
        state.isshowrepair_data = true;
      }
      if (state.resdata["part_data"].length > 0) {
        state.part_data = state.resdata["part_data"].map((item: any) => {
          return {
            id: item[0],
            part_name: item[1],
            part_spec: item[2],
            area: item[3],
            balance: item[4],
            original: item[5],
            type: item[7],
          };
        });
      }
      console.log(state.part_data);
    });
};
</script>
