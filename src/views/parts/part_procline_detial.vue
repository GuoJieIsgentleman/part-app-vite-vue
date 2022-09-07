<script setup lang="ts">
import { ref, reactive, h, onMounted } from "vue";
import table2excel from "js-table2excel";
import { formatDate111 } from "/@/utils/formatTime";
import service from "/@/utils/request";
import { ElMessage, ElMessageBox } from "element-plus";
import AddMenu from "./components/part_procline/addMenu.vue";
import UpdateMenu from "./components/part_procline/updateMenu.vue";
import { Session } from "/@/utils/storage";
import Auths from "/@/components/auth/auths.vue";
const AddMenuref = ref();
const UpdateMenuref = ref();
const onOpenAddMenu = () => {
  AddMenuref.value.openDialog();
};

const onOpenEditMenu = (row: object, index: any) => {
  console.log(row);
  UpdateMenuref.value.openDialog(row, index);
};

const onTabelRowDel = (row: any, index: any) => {
  ElMessageBox.confirm("此操作将永久删除备件信息, 是否继续?", "提示", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      console.log(row);
      service
        .get("/deletemachine_procline_detail", {
          params: {
            id: row.id,
            username: Session.get("userInfo").userName,
          },
        })
        .then((res) => {
          ElMessage({
            message: res.data,
            type: "success",
          });
        })
        .catch((err) => {
          ElMessage({
            message: err.data,
            type: "warning",
          });
        });
    })
    .catch(() => { });
};

const state = reactive({
  column: [
    { title: "序号", key: "id", type: "text" },
    { title: "产线", key: "procline", type: "text" },
    { title: "区域", key: "area", type: "text" },
    { title: "类别", key: "type", type: "text" },
    { title: "备件名称", key: "machine_name", type: "text" },
    { title: "规格型号", key: "machine_spesc", type: "text" },
    { title: "法兰盘外径", key: "FLP", type: "image", width: 200, height: 200 },
    { title: "轴对内径", key: "ZD", type: "image", width: 200, height: 200 },
    { title: "键槽", key: "JC", type: "image", width: 200, height: 200 },
    { title: "孔数", key: "KS", type: "image", width: 200, height: 200 },
    { title: "孔中心距", key: "KZXJ", type: "image", width: 200, height: 200 },
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
  Types:[],
  // Types: [
  //   {
  //     value: "减速机",
  //     label: "减速机",
  //   },
  //   {
  //     value: "升降涡轮蜗杆",
  //     label: "升降涡轮蜗杆",
  //   },
  //   {
  //     value: "液压马达",
  //     label: "液压马达",
  //   },
  //   {
  //     value: "转向机",
  //     label: "转向机",
  //   }]
});

const exportExcel1 = () => {
  table2excel(
    state.column,
    state.partslist,
    `${formatDate111(new Date())}机修产线明细.xlsx`
  );
};

const find = () => {
  getpartslist(state.selectprolince);
};




onMounted(() => {
  getpartslist("圆镀一线");
});

const getpartslist = (procline: String) => {
  service
    .get("getPart_proclinedetail", {
      params: {
        flag: "all",
        procline: procline,
      },
    })
    .then((res: any) => {
      if (res.data.length == 0) {
        ElMessageBox({ type: "error", message: "该区域没有机修使用件" });
        return;
      }
      console.log(res);
      state.partslist = res.data.map((item: any) => {
        return {
          id: item[0],
          procline: item[1],
          area: item[2],
          type: item[3],
          machine_name: item[4],
          machine_spesc: item[5],
          FLP: item[6],
          ZD: item[7],
          JC: item[8],
          KS: item[9],
          KZXJ: item[10],
        };
      });

      let temp=res.data.map((item: any) => {
        return {
          label:item[3],
          value:item[3]
        };
      });

    

      console.log('temp',quchong(temp,"label"));
       
      state.Types=quchong(temp,"label")
      state.partslist1 = state.partslist

      
      state.line = state.partslist[0]["procline"];
      getSpanArr();

    })
    .catch((err: any) => {
      ElMessageBox({ type: "error", message: "异常err" + err });
    });
};

const quchong=(temp:any,label:any)=>{
  var res:any = [];//去重复后的集合
            var tem:any = {};
            for (var i = 0; i < temp.length; i++) {
                if (!tem[temp[i][label]]) {
                    res.push(temp[i]);
                    tem[temp[i][label]] = 1;
                }
            }
            return res;

}

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

  let order = 1;
  state.partslist1.map((item: any, i: any) => {
    if (i === 0) {
      state.spanArr.push(1);
      state.pos = 0;
      state.partslist1[i].order = order;
    } else {
      // 判断当前元素与上一个元素是否相同
      if (item.area === state.partslist1[i - 1].area) {
        state.spanArr[state.pos] += 1;
        state.spanArr.push(0);
        state.partslist1[i]["order"] = state.partslist1[i - 1]["order"] = state.partslist1[
          i
        ]["order"]
          ? state.partslist1[i]["order"]
          : order;
      } else {
        state.spanArr.push(1);
        state.pos = i;
        order = order + 1;
        state.partslist1[i]["order"] = order;
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
    <el-card shadow="always">
      <el-row :gutter="50">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.add', 'btn.other']">
            <el-button @click="onOpenAddMenu()" type="danger">增加产线机修件</el-button>
          </Auths>
        </el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>

        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.add']">
            <el-button @click="exportExcel1()" type="primary" plain>导出</el-button>
          </Auths>
        </el-col>
      </el-row>
      <br />
      <el-row :gutter="12">
        <el-col :span="12" :xs="15" :sm="12" :md="12" :lg="6" :xl="12">
          <div>
            <el-select v-model="state.selectprolince" clearable placeholder="选择产线">
              <el-option v-for="item in state.use_proline_options" :key="item.value" :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </div>

        </el-col>
        <el-col :span="12" :xs="15" :sm="12" :md="12" :lg="6" :xl="12">
          <div>
            <el-select v-model="state.selectType" clearable placeholder="选择类型" @change="getInfoByType">
              <el-option v-for="item in state.Types" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </div>

        </el-col>
        <el-col class="mb20" :xs="12" :sm="12" :md="12" :lg="6" :xl="12">
          <el-button type="primary" @click="find()">查询</el-button>
        </el-col>
        <el-col class="mb20" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
      </el-row>

      <el-tag class="mx-1" effect="dark" style="size:30px ;">
        {{ state.line }}
      </el-tag>

      <el-table id="outtable" v-loading="state.loading" :data="state.partslist1" border align="center" heigth="500"
        header-align="center" max-height="500" fit :row-style="{ height: '10px' }" :cell-style="{ padding: '5px 0' }"
        row-key="id" :span-method="objectSpanMethod1">

        <el-table-column type="index" width="50" align="center" fixed>
        </el-table-column>

        <el-table-column prop="area" width="80" label="区域" align="center" fixed>
        </el-table-column>
        <el-table-column prop="type" label="备件类型" width="100" align="center" fixed>
        </el-table-column>

        <el-table-column prop="machine_name" align="center" label="名称" width="auto" fixed>
        </el-table-column>

        <el-table-column prop="machine_spesc" align="center" label="规格型号" width="auto">
        </el-table-column>
        <el-table-column prop="FLP" align="center" label="图1" width="100">
          <template #default="scope">
            <div v-if="scope.row.FLP != null">
              <el-image style="width: 100px; height: 100px" :preview-src-list="[scope.row.FLP]" :src="scope.row.FLP">
              </el-image>
            </div>
            <div v-else>无图</div>
          </template>
        </el-table-column>

        <el-table-column prop="ZD" align="center" label="图2" width="100">
          <template #default="scope">
            <div v-if="scope.row.ZD != null">
              <el-image style="width: 100px; height: 100px" :preview-src-list="[scope.row.ZD]" :src="scope.row.ZD">
              </el-image>
            </div>
            <div v-else>无图</div>
          </template>
        </el-table-column>

        <el-table-column prop="JC" align="center" label="图3" width="100">
          <template #default="scope">
            <div v-if="scope.row.JC != null">
              <el-image style="width: 100px; height: 100px" :preview-src-list="[scope.row.JC]" :src="scope.row.JC">
              </el-image>
            </div>
            <div v-else>无图</div>
          </template>
        </el-table-column>

        <el-table-column prop="KS" align="center" label="图4" width="100">
          <template #default="scope">
            <div v-if="scope.row.KS != null">
              <el-image style="width: 100px; height: 100px" :preview-src-list="[scope.row.KS]" :src="scope.row.KS">
              </el-image>
            </div>
            <div v-else>无图</div>
          </template>
        </el-table-column>

        <el-table-column prop="KZXJ" width="100" align="center" label="图5">
          <template #default="scope">
            <div v-if="scope.row.KZXJ != null">
              <el-image style="width: 100px; height: 100px" :preview-src-list="[scope.row.KZXJ]" :src="scope.row.KZXJ">
              </el-image>
            </div>
            <div v-else>无图</div>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="120">
          <template #default="scope">

            <Auths :value="['btn.edit']" class="displayStyle">
              <el-button type="primary" size="small" @click="onOpenEditMenu(scope.row, scope.$index)">编辑</el-button>
            </Auths>
            <Auths :value="['btn.del']" class="displayStyle">
              <el-button type="warning" size="small" @click="onTabelRowDel(scope.row, scope.$index)">删除</el-button>
            </Auths>

          </template>
        </el-table-column>

      </el-table>

    </el-card>
    <AddMenu ref="AddMenuref" />
    <UpdateMenu ref="UpdateMenuref" />
  </div>
</template>

<style lang="scss" scoped>
.displayStyle {
  display: inline-block;
}

body {
  touch-action: pan-y;
}
</style>
