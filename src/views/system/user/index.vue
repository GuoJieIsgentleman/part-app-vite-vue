<template>
  <div class="system-user-container">
    <el-card shadow="hover">
      <el-button size="mini" type="primary" @click="onOpenAddMenu()">新增</el-button>
      <el-table :data="state.tableData.data" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" show-overflow-tooltip></el-table-column>

        <el-table-column
          prop="username"
          label="用户名"
          show-overflow-tooltip
        ></el-table-column>
        <!-- <el-table-column label="头像" show-overflow-tooltip>
          <template #default="scope">
            <el-image
              class="system-user-photo"
              :src="scope.row.photo"
              :preview-src-list="[scope.row.photo]"
            >
            </el-image>
          </template>
        </el-table-column> -->

        <el-table-column
          prop="auth_name"
          label="角色"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          prop="area"
          label="负责产线"
          show-overflow-tooltip
        ></el-table-column>

        <el-table-column prop="path" label="操作" width="90">
          <template #default="scope">
            <el-button size="mini" type="text" @click="onOpenEditMenu(scope.row)"
              >修改</el-button
            >
            <el-button size="mini" type="text" @click="onRowDel(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="onHandleSizeChange"
        @current-change="onHandleCurrentChange"
        class="mt15"
        :pager-count="5"
        :page-sizes="[10, 20, 30]"
        :current-page="state.tableData.param.pageNum"
        background
        :page-size="state.tableData.param.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="state.tableData.total"
      >
      </el-pagination>
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

const state: any = reactive({
  tableData: {
    data: [],
    total: 0,
    loading: false,
    param: {
      pageNum: 1,
      pageSize: 10,
    },
  },
});

const addMenuRef = ref();
const editMenuRef = ref();

// 初始化表格数据
const inituseData = async () => {
  //获取用户数据

  let { data: res } = await service.get("/getusers");

  console.log("用户数据");
  console.log(res);
  state.tableData.data = res.map((item: any) => {
    return {
      id: item[0],
      username: item[1],
      role: item[3],
      auth_name: item[7],
      area: item[5],
    };
  });

  state.tableData.total = state.tableData.data.length;
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
        .then((res) => {
          ElMessage.success(res.data);
        });
      inituseData();
    })
    .catch((err) => {
      ElMessage.error(err.data);
    });
};
// 打开新增菜单弹窗
const onOpenAddMenu = (row?: object) => {
  console.log("onOpenAddMenu");
  console.log(row);
  addMenuRef.value.openDialog(row);
};
// 打开编辑菜单弹窗
const onOpenEditMenu = (row: object) => {
  console.log("onOpenEditMenu");
  console.log(row);
  editMenuRef.value.openDialog(row);
};
// 分页改变
const onHandleSizeChange = (val: number) => {
  state.tableData.param.pageSize = val;
};
// 分页改变
const onHandleCurrentChange = (val: number) => {
  state.tableData.param.pageSize = val;
};
// 页面加载时

onMounted(inituseData);
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
</style>
