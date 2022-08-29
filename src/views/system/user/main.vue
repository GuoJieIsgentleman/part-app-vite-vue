



<template>
    <div>


        <el-card shadow="hover">
            <div>
                <el-button size="mini" type="primary" @click="onOpenAddMenu()">新增角色</el-button>

            </div>

            <el-table style="width:300px ;" :highlight-current-row=true ref="roleTable" row-class-name="setTableStyle"
                :data="state.tableData.data" border stripe @cell-click="rowclick">
                <el-table-column type='index'></el-table-column>

                <el-table-column prop="auth_name" label="角色" width="auto"></el-table-column>

                <el-table-column prop="path" label="操作" width="90">
                    <template #default="scope">
                        <!-- <el-button size="mini" type="text" @click="onOpenEditMenu(scope.row)">修改</el-button> -->
                        <el-button size="mini" type="text" @click="onRowDel(scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
                :page-sizes="state.pagearray" @prev-click="prev()" @next-click="next()"
                layout="total, sizes, prev, pager, next, jumper" :total="state.total" prev-text="上一页" next-text="下一页"
                :page-count="state.pagecount" />





            <div>
                <el-drawer ref="elDrawer" v-model="visible" title="角色授权" direction="rtl" custom-class="demo-drawer"
                    close-on-press-escape show-close size="40%">

                    <el-tree ref="tree" :data="state.menus1" 
                        show-checkbox 
                        node-key="id" 
                        :default-expand-all=true
                        :default-checked-keys="[31]" 
                        :props="state.defaultProps" />
                    <el-button size="mini" type="primary" @click="saveMenu()">保存</el-button>
                </el-drawer>
                
            </div>




        </el-card>
        <AddRole ref="AddRoleRef" />
    </div>
</template>
<script setup lang="ts">
import AddRole from "./component/addRole.vue";

import service from "/@/utils/request";
import { reactive, onMounted, ref, provide, nextTick } from "vue";
import { ElMessage, ElMessageBox, ElTree } from "element-plus";
import { number } from "@intlify/core-base";



const AddRoleRef: any = ref();



const visible = ref(false)

const test = () => {
    state.checkedList.length = 0

}



const tree:any = ref()

const roleTable: any = ref()
const state: any = reactive({
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
    defaultProps: {
        children: 'children',
        label: 'menu_name',
    },
    expandList: [],
    checkedList: [],
    data: [
        {
            id: 1,
            label: 'Level one 1',
            children: [
                {
                    id: 4,
                    label: 'Level two 1-1',
                    children: [
                        {
                            id: 9,
                            label: 'Level three 1-1-1',
                        },
                        {
                            id: 10,
                            label: 'Level three 1-1-2',
                        },
                    ],
                },
            ],
        },
        {
            id: 2,
            label: 'Level one 2',
            children: [
                {
                    id: 5,
                    label: 'Level two 2-1',
                },
                {
                    id: 6,
                    label: 'Level two 2-2',
                },
            ],
        },
        {
            id: 3,
            label: 'Level one 3',
            children: [
                {
                    id: 7,
                    label: 'Level two 3-1',
                },
                {
                    id: 8,
                    label: 'Level two 3-2',
                },
            ],
        },
    ]
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


        state.menus1 = listToTree(state.menus)

        //  state.menus1 = generateOptions(state.menus)


        console.log('state.menus1', state.menus1);



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


    if (column.no != 1) {
        console.log('column.no', column.no);

        return
    }
    let arr3:any=[]
    let arr2:any=[]
   


    console.log('CheckedKeys', arr3);

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

            if (item[2] != null) {
                arr.push(item[0])
            }
        })
        visible.value = true
         
         //等待抽屉显示出来才开始渲染  所以没显示之前 都没有这个组件 引用 无效
         //所以方法也就失效了


         let temp:any=[1,3,5];
         arr=arr.map((e:any)=>{
            return e.toString()
         })
         nextTick(()=>{
            console.log('arr',  arr);
          
            console.log('temp',temp);
            tree.value.setCheckedKeys(arr, false)

            setTimeout(()=>{

            },100)

             console.log('getCheckedKeys', tree.value.getCheckedKeys(true));
              console.log('渲染完成的 tree ',tree);
         })
       

        

        





    }).catch((err: any) => {

    })
}


const saveMenu = () => {



    let arr1 = tree.value.getCheckedKeys()
    let arr2 = tree.value.getHalfCheckedKeys()
    Array.prototype.push.apply(arr1, arr2)
    console.log('arr1',arr1);
    // service.get('/updateUserRole', {
    //     params: {
    //         auth_list: JSON.stringify(arr1),
    //         current_authcode: state.current_authcode
    //     }
    // }).then((res: any) => {
    //     console.log(res);
    //     visible.value = false
    //     ElMessage({
    //         type: 'success',
    //         message: res.data
    //     })

    //     tree.value.setCheckedKeys([],false)


    // }).catch((err: any) => {

    // })

}
onMounted(() => {
    inituser();

});


onMounted(() => {
    reciveparts(10, 1)
});
const inituser = () => {
    //置0
    state.partslist = [];


    reciveparts(10, 1);
};

const handleSizeChange = (val: any) => {

    state.pagesize = val;
    reciveparts(state.pagesize, 1);
    //初始化 页数
};



const reciveparts = (page?: any, pagesize?: any) => {
    let res = service
        .get("/getroles", {
            params: {
                currentpagecount: page,
                pagesize: pagesize,
            },
        })
        .then((res: any) => {
            if (res != null) {
                state.pagecount = res.data.pages;
                state.total = res.data.total;
                state.loading = false;
                state.tableData.data = res.data.data1.map((item: any) => {
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
    reciveparts(10, 1)
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
                    reciveparts(10, 1);
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
// 打开编辑菜单弹窗

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