<template>
    <div>

        <el-card class="box-card" ref="elcard">

            <el-row :gutter="20">
                <el-col :span="4" :xs="24" :sm="12" :md="12" :lg="3" :xl="6">
                    <div class="grid-content ep-bg-purple">
                        <el-button @click="openDialog">新增记录</el-button>
                    </div>
                </el-col>

                <el-col :span="18" :xs="12" :sm="12" :md="12" :lg="19" :xl="12">
                    <div class="grid-content ep-bg-purple">

                        <el-date-picker size="mini" class="timestyle" v-model="state.starttime" type="datetime"
                            placeholder="选择开始日期" format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD HH:mm:ss">
                        </el-date-picker>
                        <el-date-picker size="mini" v-model="state.endtime" type="datetime" placeholder="选择结束日期"
                            format="YYYY-MM-DD HH:mm:ss" value-format="YYYY-MM-DD HH:mm:ss">
                        </el-date-picker>
                        <el-select size="small" v-model="state.procline" class="m-2" placeholder="产线">
                            <el-option v-for="item in state.use_proline_options" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                        <el-select size="small" v-model="state.crane_name" class="m-2" placeholder="天车名称">
                            <el-option v-for="item in state.crane_name_options" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>

                        <el-button @click="find" type="primary">查询</el-button>
                    </div>
                </el-col>

                <el-col :span="1" :xs="24" :sm="12" :md="12" :lg="1" :xl="12">
                    <div class="grid-content ep-bg-purple">
                        <el-button @click="exportExcel1()" type="primary">导出所有数据</el-button>
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="16">
                    <div class="grid-content ep-bg-purple" />
                </el-col>
                <el-col :span="8">
                    <div class="grid-content ep-bg-purple" />
                </el-col>
            </el-row>

            <el-table :key="state.key" :data="state.tableData" style="width: 100%;height: 100%;">
                <el-table-column type='index' label="序号" width="50" align="center" />

                <el-table-column style="font-size:40px" label="车间钢丝绳及链条更换记录" header-align='center'
                    header-row-class-name="header-style">
                    <el-table-column prop="shift" label="产线" width="100" align="center" />
                    <el-table-column prop="location" label="更换情况" width="140" align="center"> </el-table-column>
                    <el-table-column prop="description" label="故障描述" width="230" align="center" />
                    <el-table-column prop="models" label="规格型号" width="120" align="center" />
                    <el-table-column prop="clength" label="长度/米" align="center" width="80" />
                    <el-table-column prop="operator" label="更换人" width="100" align="center" />

                    <el-table-column prop="partimgsrc" label="图片展示" width="200" align="center">
                        <template #default="scope">

                            <div v-if="scope.row.partimgsrc">
                                <el-image style="width: 100px; height: 100px" :src="scope.row.partimgsrc">
                                </el-image>
                            </div>
                            <div v-else>
                                无图
                                <!-- <img :src="scope.row.partimgsrc" alt="" /> -->
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="确认人(班长签字)" align="center" width="120">
                        <template #default="scope">
                            <Auths :value="['btn.edit']" class="displayStyle">

                                <el-button :disabled="!(scope.row.confirmer == '' || scope.row.confirmer == null)"
                                    type="primary" @click="confirm(scope.row, scope.$index)">{{
                                        scope.row.confirmer == '' || scope.row.confirmer == null ? '待确认' : scope.row.confirmer +
                                    '已确认'

                                    }}
                                </el-button>
                            </Auths>


                        </template>
                    </el-table-column>
                    <el-table-column prop="craneType" label="类别" width="120" align="center" />
                    <el-table-column prop="update_date" label="更换日期" width="150" align="center" />
                    <el-table-column prop="update_date" label="操作" width="150" align="center">
                        <template #default="scope">
                            <Auths :value="['btn.edit']" class="displayStyle">
                                <el-button type="primary" @click="editRow(scope.row)">编辑</el-button>
                            </Auths>
                            <Auths :value="['btn.edit']" class="displayStyle">
                                <el-button type="danger" @click="delRow(scope.row)">删除</el-button>
                            </Auths>
                        </template>
                    </el-table-column>
                </el-table-column>
            </el-table>

            <el-pagination :background=true v-model:currentPage="currentPage4" v-model:page-size="pageSize4"
                :page-sizes="state.pages" layout="total, sizes, prev, pager, next, jumper" :total="state.total"
                @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </el-card>
        <Add_crane_log @updatelog="updateCranelog" ref="add_crane" />
        <Confirm ref="ConfirmRef" @init="init" />

        <Edit ref="editref" @initlog="init" />
    </div>
</template>

<script setup lang="ts">

import Edit from './components/crane/edit.vue'
import Auths from "/@/components/auth/auths.vue";
import { ref, reactive, unref, onMounted, toRefs, provide } from 'vue';
import Add_crane_log from './components/crane/add_crane_log.vue'
import { formatDate111 } from '/@/utils/formatTime';
import service from '/@/utils/request';
import table2excel from "js-table2excel";
import Confirm from './components/crane/confirm.vue'
import { ElMessage, ElMessageBox } from 'element-plus';
const value = ref('')

const ConfirmRef = ref()

const editref = ref()
const find = () => {
    getCranelog(state.pageSize4, 1)
}


const updateCranelog = (arg: any) => {
    getCranelog(10, 1)

}

const getDate = (value: any) => {
    console.log('value', formatDate111(value));

}





const init = () => {


    getCranelog(state.pageSize4, 1)
}


const pageval = ref()

const elcard = ref()



const add_crane = ref()

const state = reactive({
    starttime: '',
    endtime: '',
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
        }
    ],
    date: '',
    procline: '',
    crane_name: '',
    crane_name_options: [
        {
            value: "拆包天车",
            label: "拆包天车",
        },
        {
            value: "上料天车",
            label: "上料天车",
        },
        {
            value: "洗料天车",
            label: "洗料天车",
        },
        {
            value: "炉前天车",
            label: "炉前天车",
        },
        {
            value: "水槽天车",
            label: "水槽天车",
        },
        {
            value: "出库天车",
            label: "出库天车",
        },
        {
            value: "新锭库天车",
            label: "新锭库天车",
        },
    ],
    start: 0,
    end: 0,
    pages: [10, 20, 30, 40],
    total: 0,
    pageSize4: 10,
    currentPage4: 0,
    tableData: [],
    key: 0,
    column: [
        { title: "序号", key: "id", type: "text" },
        { title: "更换日期", key: "update_date", type: "text" },
        { title: "白班/夜班", key: "shift", type: "text" },
        { title: "更换位置(南钩/北钩)", key: "location", type: "text" },
        { title: "故障描述", key: "description", type: "text" },
        { title: "规格型号", key: "models", type: "text" },
        { title: "长度/米", key: "clength", type: "text" },
        { title: "更换人", key: "operator", type: "text" },
        { title: "图片展示", key: "partimgsrc", type: "image", width: 200, height: 200 },
        { title: "确认人(班长签字)", key: "confirmer", type: "text" },
        { title: "备注", key: "remark", type: "text" },
    ],
})

const handleSizeChange = (val: any) => {


    getCranelog(val, 1)
}
const handleCurrentChange = (val: any) => {
    pageval.value = val

    getCranelog(state.pageSize4, val)

}
let { currentPage4, pageSize4, total } = toRefs(state)


const openDialog = () => {
    add_crane.value.openDialog()
}









const getCranelog = async (pagesize: number, currentPage: number) => {


    let res = await service.post('get_crane_log', {
        crane: {
            starttime: state.starttime == null ? "" : state.starttime,
            endtime: state.endtime == null ? "" : state.endtime,
            procline: state.procline,
            crane_name: state.crane_name
        },
        pages: {
            pagesize: pagesize,
            currentPage: currentPage
        }

    })

    state.total = res.data.total

    state.tableData = res.data.data.map((item: any) => {
        return {
            id: item[0],
            update_date: formatDate111(item[1]),
            shift: item[2],
            location: item[3],
            description: item[4],
            models: item[5],
            clength: item[6],
            operator: item[7],
            confirmer: item[8],
            craneType: item[9],
            partimgsrc: item[10]
        }
    })




}

onMounted(() => {
    getCranelog(10, 1)
})





//导出
const exportExcel1 = async () => {
    let res = await service.post('get_crane_log')
    //console.log('alllog', res);

    let count = 1
    // console.log(table2excel);
    //导出所有数据
    table2excel(
        state.column,
        res.data.data.map((item: any) => {
            return {
                id: count++,
                update_date: formatDate111(item[1]),
                shift: item[2],
                location: item[3],
                description: item[4],
                models: item[5],
                clength: item[6],
                operator: item[7],
                confirmer: item[8],
                remark: item[9],
                partimgsrc: item[10]
            }
        })
        ,
        `${formatDate111(new Date())}镀锌天车钢丝绳更换记录.xlsx`
    );
};

const confirm = (row: any, index: number) => {

    console.log('row', row);
    console.log('index', index);

    ConfirmRef.value.openDialog(row, index)
}


const editRow = (rowData: any) => {

    editref.value.openDialog(rowData);
}



const delRow = (rowData: any) => {

    ElMessageBox.confirm("此操作将永久删除天车记录, 是否继续?", "提示", {
        confirmButtonText: "删除",
        cancelButtonText: "取消",
        type: "warning",
    })
        .then(() => {

            service
                .get("/deleteCrane_log", {
                    params: {
                        id: rowData.id,
                    },
                })
                .then((res) => {
                    ElMessage({
                        message: res.data,
                        type: "success",
                    });
                    init()
                    //初始化
                })
                .catch((err) => {
                    ElMessage({
                        message: err.data,
                        type: "warning",
                    });
                });
        })
        .catch(() => { });

}






const submit = () => {



}

</script>

<style scoped lang="scss">
.displayStyle {
    display: inline-block;
    margin: 2px;

}
</style>