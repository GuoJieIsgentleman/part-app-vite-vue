<template>
  <div class="system-menu-container">
    <el-card shadow="hover">

      <!-- <el-button icon="el-icon-plus" @click="onOpenAddMenu()" type="success"
              >新增外修记录</el-button
            > -->

      <el-row :gutter="20">
        <el-col :span="6" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
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
            <el-option v-for="item in state.useareas" :key="item['value']" :label="item['label']" :value="item['value']">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="6" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
          <Auths :value="['btn.add']">
            <el-button @click="exportExcel()" type="primary" plain>导出</el-button>
          </Auths>
        </el-col>

      </el-row>
      <el-button type="primary" @click="find">查询</el-button>
      <el-button @click="getalluse()" type="success" plain>查询全部记录</el-button>
      <el-button @click="getuse()" type="success" plain>查询未确认</el-button>
      <el-table id="outTable" v-loading="state.loading" :data="state.partslist" border stripe align="center" heigth="300"
        style="width: 100%" header-align="center" max-height="400" fit :row-style="{ height: '10px' }"
        :cell-style="{ padding: '5px 0' }">
        <el-table-column prop="id" label="序号" fixed width="50" align="center">
        </el-table-column>

        <el-table-column prop="user" label="领用人" width="100" align="center">
        </el-table-column>

        <el-table-column prop="use_area" label="领用区域" width="120" align="center">
        </el-table-column>
        <el-table-column prop="use_procline" label="使用产线" width="110" align="center">
        </el-table-column>
        <el-table-column prop="type" label="备件类型" width="80" align="center">
        </el-table-column>
        <el-table-column prop="use_part_name" label="报废备件名称" width="180" align="center">
        </el-table-column>
        <el-table-column prop="spec" label="报废备件型号" width="180" align="center">
        </el-table-column>
        <el-table-column prop="site_use" label="使用部位" width="180" align="center">
        </el-table-column>
        <el-table-column prop="use_date" label="领用时间" width="140" align="center">
        </el-table-column>
        <el-table-column lumn prop="use_count" label="报废数量" width="80" align="center">
        </el-table-column>

        <el-table-column prop="useconfirm" label="确认" width="140" align="center">
          <template #default="scope">

            <el-button type="success" :disabled="scope.row.useconfirm == null ? false : true"
              @click="openscarpconfirmref(scope.row)">{{
                scope.row.useconfirm == null
                ? "待确认"
                : scope.row.useconfirm + "已确认"
              }}</el-button>
          </template>
        </el-table-column>

        <el-table-column prop="useconfirmdate" label="确认时间" width="140" align="center">
        </el-table-column>
        <el-table-column prop="user_reason" label="原因" width="180" align="center">
        </el-table-column>
        <el-table-column prop="remark" label="备注" width="180" align="center">
        </el-table-column>


      </el-table>
      <!-- 分页栏 -->
      <el-pagination :page-sizes="[20, 40, 60, 80]" :page-size="100" layout="total, sizes, prev, pager, next, jumper"
        :total="79">
      </el-pagination>
    </el-card>

    <Scarpconfirm ref="scarpconfirmref" />

  </div>
</template>

<script lang="ts" setup>

import Scarpconfirm from "./components/scrap/scarpconfirm.vue";

import service from "/@/utils/request";
import { ref, reactive, onMounted, toRefs, provide } from "vue";

import { formatDate111 } from "/@/utils/formatTime";

import { exportTable } from "/@/utils/exportExcel";
import { use_proline_options, getElectrontype, ListItem, getElectronArea } from "/@/hooks/getHgInfo";
const exportExcel = () => {
  exportTable("#outTable", `${formatDate111(new Date())}备件报废明细`);
};


const scarpconfirmref = ref();


// 打开新增菜单弹窗
const openscarpconfirmref = (row?: any) => {
  scarpconfirmref.value.openDialog(row);
};



const state = reactive({
  use_proline_options: [] as Array<ListItem>,
  selectarea: "",
  useareas: [] as Array<ListItem>,
  selectprolince: "",
  start: "",
  end: "",
  loading: true,
  selectvalue: "",
  value: "",
  partslist: [],
  filterTable: null,
  save: false,
  total: 0,
  options: [
    {
      value: "补",
      label: "补",
    },
    {
      value: "不补",
      label: "不补",
    },
  ],
});

onMounted(async () => {
  state.use_proline_options = await use_proline_options()

  state.useareas = await getElectronArea()
})



const conversion = (res: any) => {

  state.partslist = res.map((item: any[]) => {
    return {
      id: item[0],
      user: item[1],
      use_area: item[2],
      type: item[3],
      spec: item[4],
      use_part_name: item[5],
      site_use: item[6],
      use_count: item[7],
      use_reason: item[8],
      use_date: formatDate111(item[9]),
      useconfirm: item[10],
      use_procline: item[11],
      useconfirmdate: formatDate111(item[12]),
      remark: item[13],
      create_date: item[14]
    };
  });


}


const initscrap = async (flag?: any) => {
  let { data: res } = await service.post("/hg_getscrap", {
    flag: flag,
  });

  if (res != null) {
    state.loading = false;
  }
  conversion(res)

  state.total = state.partslist.length;

};
provide("initscrap", initscrap);
onMounted(initscrap);
const getuse = () => {
  //未确认记录
  initscrap("noconfirm");
};

const getalluse = () => {
  //所有记录
  initscrap("all");
};

const find = () => {

  service.post("/hg_getscrap", {
    flag1: "筛选查询",
    start: state.start,
    end: state.end,
    prolince: state.selectprolince,
    area: state.selectarea,
  })
    .then((res) => {

      if (res != null) {
        state.loading = false;
      }
      conversion(res)

      state.total = state.partslist.length;
    })
    .catch((err) => { });
};
</script>

<style scoped lang="scss">
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
</style>
