<template>
  <div class="system-menu-container">
    <el-card shadow="hover">


      <el-row :gutter="35">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.add']">
            <el-button @click="onOpenAddMenu()" type="success">添加电器备件</el-button>
          </Auths>
        </el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="0" :sm="12" :md="12" :lg="6" :xl="6"></el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="6" :xl="6">
          <Auths :value="['btn.add']">
            <el-button @click="exportExcel1()" type="primary">导出</el-button>
          </Auths>
        </el-col>
      </el-row>
      <el-row :gutter="24">
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12">

        </el-col>
        <el-col :span="12" :xs="12" :sm="12" :md="12" :lg="12" :xl="12"> </el-col>
      </el-row>


      <el-select v-model="selected" filterable remote reserve-keyword placeholder="区域请输入关键词进行搜索"
        :remote-method="remoteMethod" :loading="loading" clearable>
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>

      <el-select @change="getpartname" v-model="state.part_type_value" filterable placeholder="备件类型" clearable>
        <el-option v-for="item in state.ruleForm.usetype" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>

      <el-select v-model="state.part_name_value" @change="getspesc" filterable placeholder="备件名称" clearable>
        <el-option v-for="item in state.ruleForm.part_name" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>

      <el-select v-model="state.part_spec_value" filterable placeholder="规格型号" clearable>
        <el-option v-for="item in state.ruleForm.usespesc" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>

      <el-button @click="selectparts()" type="success">查询</el-button>


      <el-table id="outTable" v-loading="state.loading" :data="state.partslist" :ref="filterTable" border show
        align="center" height="600" style="width: 100%" header-align="center" max-height="900" fit
        :row-style="{ height: '10px' }" :cell-style="{ padding: '5px 0' }" size="mini" show-summary
        :summary-method="getSummaries" row-key="id">
        <el-table-column type="index" label="序号" fixed width="50" align="center">
        </el-table-column>
        <el-table-column prop="part_name" label="备件名称" width="180" align="center">
        </el-table-column>

        <el-table-column prop="part_spec" label="规格型号" width="180" align="center">
        </el-table-column>

        <el-table-column prop="partimgsrc" label="图片展示" width="200" align="center">

          <template #default="scope">
            <div v-if="scope.row.partimgsrc">
              <el-image style="width: 100px; height: 100px" :src="scope.row.partimgsrc"
                :preview-src-list="[scope.row.partimgsrc]">
              </el-image>
            </div>
            <div v-else>
              无图
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="area" min-width="150" align="center" label="搁置产线区域">
        </el-table-column>
        <el-table-column prop="balance" label="结存剩余（台)" min-width="100" align="center">
        </el-table-column>
        <el-table-column prop="original" label="原有数量（台)" min-width="100" align="center">
        </el-table-column>

        <el-table-column prop="type" label="备件类型" width="100" align="center">
        </el-table-column>
        <el-table-column prop="site_use" label="使用部位" width="100" align="center">
        </el-table-column>
        <el-table-column prop="remark" label="备注" width="100" align="center">
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="120">
          <template #default="scope">

            <Auths :value="['btn.edit']" class="displayStyle">
              <el-button size="small" type="primary" v-if="scope.row['isShow']"
                @click="onOpenEditMenu(scope.row, scope.$index)">编辑</el-button>
            </Auths>

            <Auths :value="['btn.del']" class="displayStyle">
              <el-button size="small" type="warning" @click="onTabelRowDel(scope.row, scope.$index)">
                删除
              </el-button>
            </Auths>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页栏 -->
      <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
        :page-size="state.pagesize" :page-sizes="state.pagearray" layout="total, sizes, prev, pager, next, jumper"
        :total="state.total" prev-text="上一页" next-text="下一页" :current-page="state.currentPage"
        :page-count="state.pagecount" />
    </el-card>
    <AddMenu ref="addMenuRef" />
    <EditMenu ref="editMenuRef" @senddata="setdata" />
  </div>
</template>

<script lang="ts" setup>
import table2excel from "js-table2excel";
import Auths from "/@/components/auth/auths.vue";
import AddMenu from "./components/machine/addMenu.vue";
import EditMenu from "./components/machine/editMenu.vue";
import service from "/@/utils/request";
import { ref, reactive, onMounted } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { formatDate111 } from "/@/utils/formatTime";
import { Session } from "/@/utils/storage";
const addMenuRef = ref();

const editMenuRef = ref();

const loading = ref(false)

const selected = ref(null)

const options = ref<Array<ListItem>>()


//-----------------远程搜索--------------------

interface ListItem {
  value: string
  label: string
}

const remoteMethod = async (query: string) => {

  if (query !== '') {
    loading.value = true;
    setTimeout(async () => {
      loading.value = false;
      let { data } = await service.get("hg_getMachineUsearea", {
        params: {
          query: query
        }
      })
      options.value = data.filter((item: Array<string>) => {
        return item[0].toLowerCase().includes(query.toLowerCase())
      }).map((item: string[]) => {
        return {
          value: item[0],
          label: item[0]
        }
      })



    }, 200);
  } else {
    options.value = [];
  }

}

//-------------------------------------


// 打开新增菜单弹窗
const onOpenAddMenu = () => {
  addMenuRef.value.openDialog();
};


const handleSizeChange = (val: any) => {
  state.pagesize = val;
  //初始化 页数
  selectparts()
};
const handleCurrentChange = (val: any) => {

  state.currentPage = val;

  selectparts()

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
  state.partslist[v1].site_use = v[0][4];
  state.partslist[v1].balance = v[0][5];
  state.partslist[v1].original = v[0][6];
  state.partslist[v1].remark = v[0][7];
  state.partslist[v1].type = v[0][8];
  state.partslist[v1].partimgsrc = v[0][9];

};

const state = reactive({
  currentPage: 1,
  areainfo: Session.get("userInfo").areainfo,
  column: [
    { title: "序号", key: "id", type: "text" },
    { title: "备件名称", key: "part_name", type: "text" },
    { title: "规格型号", key: "part_spec", type: "text" },
    { title: "使用部位", key: "site_use", type: "text" },
    { title: "图片展示", key: "partimgsrc", type: "image", width: 200, height: 200 },
    { title: "搁置产线区域", key: "area", type: "text" },
    { title: "结存剩余（台)", key: "balance", type: "text" },
    { title: "原有数量（台)", key: "original", type: "text" },
    { title: "备件类型", key: "type", type: "text" },
  ],
  pagearray: [10, 20, 30, 40, 50],
  ruleForm: {
    usetype: [] as Array<ListItem>,
    userarea: [] as Array<ListItem>,
    part_name: [] as Array<ListItem>,
    usespesc: [] as Array<ListItem>,
  },
  part_spec_options: [] as any[],
  part_spec_value: null,
  part_name_value: null,
  part_area_value: null,
  part_type_value: null,

  loading: true,

  part_name_options: [] as any[],
  part_area_options: [] as any[],
  part_type_options: [] as any[],
  part_spec: [],

  partslist: [] as any,
  partslist1: [] as any,
  filterTable: null,
  save: false,
  total: 0,
  pagecount: 0,
  pagesize: 10,
  rowdata: [],
});
const filterTable = (el: any) => { };


const checkIsShow = (area: any) => {





  return true;
};

//通过分页返回值

const initpart = () => {
  //置0
  state.partslist = [];
  state.currentPage = 1
  state.pagesize = 10
  selectparts()
};

//----------------------------------
const gettype = async () => {
  //通过area 找type

  let { data: type } = await service.get("/hg_getMachineType");
  state.ruleForm.usetype = type.map((item: any) => {
    return {
      value: item[0] == null ? '' : item[0],
      label: item[0] == null ? '' : item[0],
    };
  });



};

//----------------------------------
const getpartname = async () => {
  //通过area 找type

  let { data: partname } = await service.get("/hg_getMachinePartName", {
    params: {
      type: state.part_type_value,

    },
  });



  state.ruleForm.part_name = partname.map((item: any) => {
    return {
      value: item[0],
      label: item[0],

    };
  });
};

const getspesc = async () => {
  //通过area 找type

  let { data: type } = await service.get("/hg_getMachineSpesc", {
    params: {
      use_part_name: state.part_name_value,
      type: state.part_type_value,
    },
  });

  state.ruleForm.usespesc = type.map((item: any) => {
    return {
      value: item[0],
      label: item[0],
    };
  });
};

onMounted(() => {
  initpart();
  gettype();
});


// 删除当前行
const onTabelRowDel = (row: any, index: any) => {
  ElMessageBox.confirm("此操作将永久删除备件信息, 是否继续?", "提示", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    service
      .get("/hg_deleteMachine", {
        params: {
          id: row.id,
        },
      })
      .then((res: any) => {
        ElMessage({
          message: res.data,
          type: "success",
        });

        initpart();
      })
      .catch((err: any) => {
        ElMessage({
          message: err.data,
          type: "warning",
        });
      });
  })
    .catch(() => { });
};


const conversion = (data: any) => {
  state.partslist = data.map((item: any) => {
    return {
      id: item[0],
      part_name: item[1],
      part_spec: item[2],
      area: item[3],
      site_use: item[4],
      balance: item[5],
      original: item[6],
      remark: item[7],
      type: item[8],
      partimgsrc: item[9],
      isShow: checkIsShow(item[3])

    }
  })
}

const selectparts = async () => {

  let { data } = await service.post("/hg_getMachineParts", {

    part_spec: state.part_spec_value,
    part_name: state.part_name_value,
    area: selected.value,
    type: state.part_type_value,
    currentPage: state.currentPage,
    pageSize: state.pagesize

  })

  state.total = data.total_count
  state.pagecount = data.pages
  console.log('res', data);

  state.loading = false;

  conversion(data.result)




};





const exportExcel1 = () => {

  table2excel(state.column, state.partslist, `${formatDate111(new Date())}备件明细.xlsx`);
};

const getSummaries = (param: any) => {
  const { columns, data } = param;
  const sums: any = [];
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

<style lang="scss" scoped >
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


.el-table .warning-row {
  background-color: rgb(235, 36, 36);
  color: white;
}

.el-table .warning-row2 {
  background-color: rgb(88, 199, 78);
  color: white;
}

.el-table .success-row {
  --el-table-tr-background-color: var(--el-color-success-lighter);
}

.el-table tbody tr:hover>td {
  background-color: #96b7dc !important;
  color: black;
}

#app>section>div.el-backtop {
  cursor: pointer;
  z-index: 5;
  right: 40px;
  bottom: 40px;
  top: 500px;
}

.displayStyle {

  display: inline-block;

}
</style>
