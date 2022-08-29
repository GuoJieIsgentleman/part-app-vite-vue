

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

      <el-row :gutter="50">
        <el-col :span="12" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
          <el-select v-model="state.type" filterable placeholder="备件区域" clearable>
            <el-option v-for="item in state.types" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-col>

        <el-col :span="12" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
          <el-button type="primary" @click="find()">查询</el-button>
        </el-col>
      </el-row>

      <el-table id="outtable" v-loading="state.loading" style="width:1000px ;" :data="state.partslist" border
        align="center" heigth="500" header-align="center" max-height="500" fit :row-style="{ height: '20px' }"
        :cell-style="{ padding: '5px 0' }">
        <el-table-column label="产线库存数量对比" width="auto" align="center">
          <el-table-column type="index" fixed width="80" align="center">
          </el-table-column>
          <!-- <el-table-column prop="procline" label="产线" width="80" align="center">
          </el-table-column> -->
          <el-table-column prop="type" width="300" label="备件类型" align="center">
          </el-table-column>
          <el-table-column prop="name" width="300" label="备件名称" align="center">
          </el-table-column>
          <el-table-column prop="spec" width="300" label="规格型号" align="center">
          </el-table-column>
          <el-table-column prop="kucun" label="备件库存" width="80" align="center">
          </el-table-column>

          <el-table-column prop="cx" align="center" label="产线使用" width="80">
          </el-table-column>
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
     
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, h, onMounted } from "vue";
import table2excel from "js-table2excel";
import { formatDate111 } from "/@/utils/formatTime";
import service from "/@/utils/request";
import { ElMessage, ElMessageBox } from "element-plus";

const state = reactive({
  column: [
    { title: "备件名称", key: "name", type: "text" },
    { title: "型号", key: "spec", type: "text" },
    { title: "库存", key: "kucun", type: "text" },
    { title: "产线使用", key: "cx", type: "text" },
  ],
  partslist: [] as any,
  type: '',
  types: [],
  selectprolince: "",
  loading: "",
  spanArr: [] as any,
  pos: 0,

});

const onOpenAddMenu = () => { };
const exportExcel1 = () => {
  table2excel(
    state.column,
    state.partslist,
    `${formatDate111(new Date())}产线库存对比.xlsx`
  );
};

onMounted(() => {
  getTypes()
  getpartslist();

});



const getpartslist = () => {

  service
    .get("getmachine_contrast", {
      params: {
        machineType: state.type,

      },
    })
    .then((res: any) => {
      console.log("res产线对比返回值");
      console.log(res);
      if (res.data.length == 0) {
        ElMessageBox({ type: "error", message: "没有值" });
        return;
      }

      state.partslist = res.data.map((item: any) => {
        return {
          type: item[0],
          name: item[1],
          spec: item[2],
          kucun: item[3],
          cx: item[4],
        };
      });

      //getSpanArr();
      console.log("partslist");
      console.log(state.partslist);
    })
    .catch((err: any) => {
      ElMessageBox({ type: "error", message: "异常err" + err });
    });
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

const find = () => {
  getpartslist();
};



const getTypes = () => {
  service.get('getProclineMachineTypes').then((res: any) => {


    state.types = res.data.map((item: any) => {
      return {
        label: item[0],
        value: item[0]
      }
    })

    console.log('state.types', state.types);

  }).catch((err: any) => {
    ElMessage({ type: 'error', message: '返回出错' })
  })
}



</script>
<style lang="scss" scoped>
</style>
