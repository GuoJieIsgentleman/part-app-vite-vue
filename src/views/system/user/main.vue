



<template>
    <div>


        <el-card shadow="hover">
            <div>
                <el-button size="mini" type="primary" @click="onOpenAddMenu()">新增角色</el-button>

            </div>

            <el-table style="width:800px ;" :highlight-current-row=true ref="roleTable" row-class-name="setTableStyle"
                :data="state.tableData.data" border stripe @cell-click="rowclick">
                <el-table-column type="index" width="50" />
                <el-table-column prop="auth_name" label="角色" width="auto"></el-table-column>
                <el-table-column prop="auth_code" label="编码" width="180"></el-table-column>

                <el-table-column prop="path" label="操作" width="90">
                    <template #default="scope">
                        <!-- <el-button size="mini" type="text" @click="onOpenEditMenu(scope.row)">修改</el-button> -->
                        <el-button size="mini" type="text" @click="onRowDel(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
                :page-sizes="state.pagearray" layout="total, sizes, prev, pager, next, jumper" :total="state.total"
                prev-text="上一页" next-text="下一页" :page-count="state.pagecount" />





            <div>
                <el-drawer ref="elDrawer" v-model="visible" title="角色授权" direction="rtl" custom-class="demo-drawer"
                    close-on-press-escape show-close size="40%">

                    <el-tree @node-click="nodeClick" ref="tree" :data="state.menus1" show-checkbox node-key="id"
                        :default-expand-all=true :default-checked-keys="[31]" :props="state.defaultProps" />
                    <el-button size="mini" type="primary" @click="saveMenu()">保存</el-button>
                </el-drawer>

            </div>




        </el-card>
        <AddRole ref="AddRoleRef" />
        <el-dialog v-model="state.btnDialog" title="菜单按钮">

            <div style="width:300px ;display: flex;">

                <el-checkbox-group v-model="state.checked1" v-for="item in state.checkes">
                    <el-checkbox :label="item" :key="item">{{ item }}</el-checkbox>
                </el-checkbox-group>


            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="state.btnDialog = false">Cancel</el-button>
                    <el-button size="mini" type="primary" @click="saveBtn()">保存</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>
<script setup lang="ts">
import AddRole from "./component/addRole.vue";

import service from "/@/utils/request";
import { reactive, onMounted, ref, provide, nextTick } from "vue";
import { ElMessage, ElMessageBox, ElTree } from "element-plus";
const AddRoleRef: any = ref();



const visible = ref(false)

const nodeClick = (node: any, prop: any, event: any) => {
    console.log('节点被点击后node', node);
    console.log('节点被点击后prop', prop);
    console.log('节点被点击后event', event);

    //打开菜单按钮
    state.btnDialog = true
}

const saveBtn = () => {
    console.log(state.checked1);

}



const tree: any = ref()

const roleTable: any = ref()
const state: any = reactive({

    checkes: ['增加', '删除', '导出'],
    checked1: [],
    checked2: false,
    btnDialog: false,
    current_authcode: "", //当前点击的权限code
    menus: [
    ],
    menus1: [
    ] as any,
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
    currentPage: 1,
    defaultProps: {
        children: 'children',
        label: 'menu_name',
    },
    expandList: [],
    checkedList: [],
    temp_row: null,
});


onMounted(() => {
    // 1 先获取所有的菜单 并且生成树状结构
    // 2 通过返回的角色 对menus 重新赋值 并且 扩展的 数字 和 默认选中的数组
    // 3 保存的时候再把 选中的 数组 生成  权限id 和 权限code
    //4 后台根据 权限code 判断是否增加 新的权限
    service.get('/getUserRoles'
    ).then((res: any) => {
        console.log('res', res);
        state.menus = res.data.map((item: any) => {
            return {
                id: item[0],
                menu_name: item[1] + "--" + item[0],
                name: item[4],
                parentname: item[8]
            }
        })
        //展示树形结构

        console.log('log menus', state.menus);

        state.menus1 = listToTree(state.menus)

        console.log('log menus1', state.menus1);
    }).catch((err: any) => {

    })
})
const listToTree = (arr: any) => {
    let array: any = []
    arr.forEach((item: any) => { // 遍历对象数组   
        let tem: any = []
        for (var i in item) {
            tem[i] = item[i]
        }

        tem.children = arr.filter((info: any) =>
            info.parentname === tem.name)

        // 找到每个对象的子节点 
        if (tem.parentname === null) {
            array.push(tem) // 将一层节点放入新数组中
        }
    })


    return array //循环结束，返回结果
}

const rowclick = (row: any, column: any, event: any) => {
    console.log('点击后显示的table  row', row);

    //获取临时的row
    state.temp_row = row
    if (column.no != 1) {

        return
    }
    let arr3: any = []
    let arr2: any = []

    //返回id username 所对应的权限 赋值给 menus
    state.current_authcode = row.auth_code;
    let arr: any = []

    service.get('getUserRoles', {
        params: {
            auth_code: row.auth_code
        }
    }).then((res: any) => {

        //检索 已经被选中的数组
        res.data.forEach((item: any) => {

            if (item[5] != null) {
                arr.push(item[0])
            }
        })
        arr.push(31)
        visible.value = true

        //等待抽屉显示出来才开始渲染  所以没显示之前 都没有这个组件 引用 无效
        //所以方法也就失效了

        nextTick(() => {
            tree.value.setCheckedKeys(arr, false)


        })




    }).catch((err: any) => {

    })
}


const saveMenu = () => {



    let arr1 = tree.value.getCheckedKeys()
    let arr2 = tree.value.getHalfCheckedKeys()
    Array.prototype.push.apply(arr1, arr2)
    console.log('arr1', arr1);
    service.get('/updateUserRole', {
        params: {
            auth_list: JSON.stringify(arr1),
            current_authcode: state.current_authcode
        }
    }).then((res: any) => {
        console.log(res);
        visible.value = false
        ElMessage({
            type: 'success',
            message: res.data
        })

        tree.value.setCheckedKeys([], false)
        state.temp_row = null

    }).catch((err: any) => {

    })

}
onMounted(() => {
    inituser();

});


onMounted(() => {
    reciveparts()
});
const inituser = () => {
    //置0
    state.partslist = [];


    reciveparts();
};

const handleSizeChange = (val: any) => {
    state.pagesize = val;
    reciveparts();
    //初始化 页数
};



const reciveparts = () => {
    service.get("getroles", {
        params: {
            currentpagecount: state.currentPage,
            pagesize: state.pagesize,
        },
    })
        .then((res: any) => {
            console.log('分页获取权限', res);

            if (res != null) {
                state.pagecount = res.data.pages;
                state.total = res.data.total_count;
                state.loading = false;
                state.tableData.data = res.data.result.map((item: any) => {
                    return {
                        id: item[0],
                        auth_name: item[1],
                        auth_code: item[2]
                    };
                });
            }
            state.tableData.total = state.tableData.data.length;
        })
        .catch((err: any) => {
            ElMessage({ type: "error", message: err.data });
        });
};
provide('reciveparts', reciveparts)

// // 初始化表格数据
const inituseData = () => {
    //获取用户数据
    reciveparts()
};

provide("inituseData", inituseData);

// 当前行删除
const onRowDel = (row: any) => {
    //删除

    console.log('row', row);

    ElMessageBox.confirm("此操作将永久删除, 是否继续?", "提示", {
        confirmButtonText: "删除",
        cancelButtonText: "取消",
        type: "warning",
    })
        .then(() => {
            service
                .get("/deleteRole", {
                    params: {
                        auth_code: row["auth_code"],
                        auth_name: row["auth_name"],
                        id: row["id"],

                    },
                })
                .then((res: any) => {
                    ElMessage({ type: 'success', message: res.data });
                    reciveparts();
                });

        })
        .catch((err: any) => {
            ElMessage.error(err.data);
        });
};
// 打开新增菜单弹窗
const onOpenAddMenu = () => {


    AddRoleRef.value.openDialog();
};

// 分页改变
const handleCurrentChange = (val: any) => {
    console.log("改变页数" + val);

    state.currentPage = val
    reciveparts();
};
// 页面加载时
</script>


<style lang="scss" scoped>
.box {
    float: left;
    height: 500px;
    overflow: auto;

}


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


.el-checkbox {
    margin-left: 5%;
    margin-right: 25px;
    width: 240px; //根据内容设置宽度
    padding-left: 0px;
    text-align: left; //这个很关键，否则每一行都是居中状态
}

.box-card {
    overflow-y: scroll;
    height: 510px;
}

.rowstyle {
    background-color: aqua;
}
</style>    