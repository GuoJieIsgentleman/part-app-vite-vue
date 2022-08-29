<template>
  <div class="system-user-container">



          <el-row :gutter="20">
            <el-col  :xs="6" :sm="5" :md="5" :lg="3" :xl="3">
              <el-button plain size="mini" type="primary" @click="onOpenAddMenu()">新增用户</el-button>
            </el-col>
                <el-col  :xs="2" :sm="5" :md="5" :lg="3" :xl="3">
           
            </el-col>
            <el-col :xs="10" :sm="5" :md="5" :lg="5" :xl="5">
              <el-select v-model="state.name" filterable remote reserve-keyword placeholder="输入用户名"
                :remote-method="getUserName" :loading="loading">
                <el-option v-for="item in state.userNames" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-col>
            <el-col :xs="3" :sm="3" :md="3" :lg="3" :xl="3">
              <el-button size="mini" type="primary" @click="findUser()">查询</el-button>
            </el-col>
          </el-row>
          <br/>
    <el-card shadow="hover">
     


        
          <el-table fit :data="state.tableData.data" stripe  border  style="width:800px ;">
            <el-table-column prop="id" label="ID" show-overflow-tooltip fixed
            ></el-table-column>

            <el-table-column prop="username" label="用户名" show-overflow-tooltip></el-table-column>
       
            <el-table-column prop="auth_name" label="角色" show-overflow-tooltip></el-table-column>
            <el-table-column prop="area" label="负责产线" show-overflow-tooltip></el-table-column>
            <el-table-column prop="inspect_area" label="巡检产线" show-overflow-tooltip></el-table-column>
            <el-table-column prop="path" label="操作" width="90">
              <template #default="scope">
                <el-button size="mini" type="text" @click="onOpenEditMenu(scope.row)">修改</el-button>
                <el-button size="mini" type="text" @click="onRowDel(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
            :page-size="state.pagesize" :page-sizes="state.pagearray" @prev-click="prev()" @next-click="next()"
            layout="total, sizes, prev, pager, next, jumper" :total="state.total" prev-text="上一页" next-text="下一页"
            :page-count="state.pagecount" />
      
    
    </el-card>

    <AddMenu ref="addMenuRef" />
    <EditMenu ref="editMenuRef" />

  </div>
</template>

<script lang="ts" setup>
import AddMenu from "./component/adduseMenu.vue";
import EditMenu from "./component/edituseMenu.vue";
import service from "/@/utils/request";
import { reactive, onMounted, ref, provide } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";

const loading = ref(false)
const value = ref<string[]>([])

const getUserName = () => {


  service.get('getusers', {
    params: {
      userName: state.name

    }
  }).then((res: any) => {

    state.userNames = res.data.map((item: any) => {
      return {
        value: item[1],
        label: item[1]

      }
    })
  })
}

const findUser = () => {
  service.get('getusers', {
    params: {
      userName: state.name

    }
  }).then((res: any) => {

    state.tableData.data = res.data.map((item: any) => {
      return {
        id: item[0],
        passwd: item[2],
        username: item[1],
        role: item[3],
        auth_name: item[8],
        area: item[5],
        inspect_area: item[6]
      };
    });
  })
}

const state: any = reactive({
  pagearray: [10, 20, 30, 40, 50],
  pagecount: 0,
  loading: false,
  total: 0,
  tableData: {
    data: [],

    param: {
      pageNum: 1,

    },


  },
  pagesize: 10,
  userNames: [],
  name: ""
});

const addMenuRef = ref();
const editMenuRef = ref();

onMounted(() => {
  inituser();

});
const inituser = () => {
  //置0
  state.partslist = [];
  console.log("执行了 initpart");

  reciveparts(10, 1);
};

const handleSizeChange = (val: any) => {
  console.log("每页" + val);
  state.pagesize = val;
  reciveparts(state.pagesize, 1);
  //初始化 页数
};





onMounted(() => {
  reciveparts(10, 1)
});

const reciveparts = (page?: any, pagesize?: any) => {
  let res = service
    .get("/getusers", {
      params: {
        currentpagecount: page,
        pagesize: pagesize,
      },
    })
    .then((res: any) => {


      if (res.data != null) {
        state.pagecount = res.data.pages;
        state.total = res.data.total;
        state.loading = false;

        state.tableData.data = res.data.data1.map((item: any) => {
          return {
            id: item[0],
            passwd: item[2],
            username: item[1],
            role: item[3],
            auth_name: item[8],
            area: item[5],
            inspect_area: item[6]
          };
        });
      }
      console.log("state.tableData.data");
      console.log(state.tableData.data);
    })
    .catch((err: any) => {
      ElMessage({ type: "error", message: err.data });
    });
};

// // 初始化表格数据
const inituseData = () => {
  //获取用户数据
  reciveparts(10, 1)
};

provide("inituseData", inituseData);

// 当前行删除
const onRowDel = (row: any) => {
  //删除
  ElMessageBox.confirm("此操作将永久删除, 是否继续?", "提示", {
    confirmButtonText: "删除",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      service
        .get("/updateuser", {
          params: {
            username: row["username"],
            role: row["role"],
            flag: "删除",
          },
        })
        .then((res: any) => {
          ElMessage.success(res.data);
        });
      reciveparts(10, 1);
    })
    .catch((err: any) => {
      ElMessage.error(err.data);
    });
};

const onOpenAddMenu = (row?: object) => {
  addMenuRef.value.openDialog(row);
};

const onOpenEditMenu = (row: object) => {
  console.log('传递之前的row',row);
  

  editMenuRef.value.openDialog(row);
};
// 分页改变
const onHandleSizeChange = (val: number) => {
  state.pageSize = val;
  console.log("每页" + val);
  state.tableData.pageSize = val;
  reciveparts(state.pageSize, 1);
};
// 分页改变
const handleCurrentChange = (val: any) => {
  console.log("改变页数" + val);
  reciveparts(state.pagesize, val);
};
// 页面加载时

</script>

<style scoped lang="scss">
.system-user-container {
  .system-user-search {
    text-align: right;
  }

  .system-user-photo {
    width: 40px;
    height: 40px;
    border-radius: 100%;
  }
}


.el-table__body-wrapper::-webkit-scrollbar-thumb {
  background-color: #ddd;

  border-radius: 10px;
}


.el-table__body-wrapper::-webkit-scrollbar {
  width: 20px; // 横向滚动条
  height: 20px; // 纵向滚动条 必写
}

.el-table .el-table-column {
  justify-content: center;

  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  table-layout: fixed;
}
</style>
