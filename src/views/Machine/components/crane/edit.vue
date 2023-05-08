<template>
    <div class="system-menu-container">
        <el-dialog title="编辑菜单" v-model="state.isShowDialog" width="769px" :before-close="handleClose">
            <el-form :model="state" size="small" label-width="80px">
                <el-row :gutter="35">
                    <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
                        <el-form-item label="记录">
                            <div v-if="state.rowdata.partimgsrc != null">
                                <!-- <img :src="ruleForm.imgsrc" alt="" style="height: 40%; width: 40%" /> -->
                                <el-upload class="avatar-uploader" :auto-upload="false" :multiple="false" ref="upload1"
                                    :action="
                                        'https://www.ssxyf.cn:5556/Crane_img_uploadfile?imgid=' +
                                        state.id +
                                        '&&time1=' +
                                        new Date().getTime().toString()
                                    " :show-file-list="false" :on-success="handleAvatarSuccess"
                                    :before-upload="beforeAvatarUpload" :on-change="onchange">
                                    <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
                                    <img v-if="state.imageUrl == ''" :src="state.rowdata.partimgsrc" class="avatar" />
                                    <img v-else :src="state.imageUrl" class="avatar" />

                                </el-upload>
                            </div>
                            <div v-else>
                                <el-upload class="avatar-uploader" :multiple="false" :auto-upload="false" :action="
                                    'https://www.ssxyf.cn:5556/Crane_img_uploadfile?imgid=' +
                                    state.id +
                                    '&&time1=' +
                                    new Date().getTime().toString()
                                " :show-file-list="false" :on-success="handleAvatarSuccess" ref="upload1"
                                    :on-change="onchange" :before-upload="beforeAvatarUpload">
                                    <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
                                    <img v-if="state.imageUrl" :src="state.imageUrl" class="avatar" />

                                    <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                                </el-upload>
                                <!-- <img :src="scope.row.partimgsrc" alt="" /> -->
                            </div>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="35">
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="更换日期">
                            <el-input v-model="state.rowdata.update_date" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="产线">

                            <el-select v-model="state.rowdata.shift" class="m-2" placeholder="产线" size="large">
                                <el-option v-for="item in state.use_proline_options" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="更换位置">
                            <el-row>


                                <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                                    <el-select v-model="state.rowdata.location" class="m-2" placeholder="天车名称" size="large">
                                        <el-option v-for="item in state.crane_name_options" :key="item.value"
                                            :label="item.label" :value="item.value" />
                                    </el-select>
                                </el-col>
                                <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                                    <el-select v-model="state.rowdata.location" class="m-2" placeholder="(南钩/北钩)"
                                        size="large">
                                        <el-option v-for="item in state.location_l_rs" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-col>
                            </el-row>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="故障描述">
                            <el-input v-model="state.rowdata.description" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="规格型号">
                            <el-input v-model="state.rowdata.models" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>

                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="长度(米)">
                            <el-input v-model="state.rowdata.clength" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="更换人">
                            <el-input v-model="state.rowdata.operator" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>


                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="类别">
                            <el-select v-model="state.rowdata.craneType" class="m-2" placeholder="类别" size="large">
                                <el-option v-for="item in state.craneTypes" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>

                </el-row>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="onCancel" size="small">取 消</el-button>
                    <el-button type="primary" @click="onSubmit" :loading="state.issave" size="small">保存</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>
  
<script lang="ts" setup>
import { compress, compressAccurately } from "image-conversion";
import { reactive, toRefs, ref, inject } from "vue";

import service from "/@/utils/request";
import { ElMessage } from "element-plus";
import { formatDate111 } from "/@/utils/formatTime";
import { store } from "/@/store";
import { Session } from "/@/utils/storage";
import { init } from "echarts";
import { UploadFile } from "element-plus/lib/el-upload/src/upload.type";

// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";

//编辑框根据权限显示是否让编辑 班长

const isdisabled = ref(true);


const state = reactive({
    isShowDialog: false,
    usernmae: Session.get("userInfo").userName,
    issave: false,
    imgsrc: '',
    id: '',
    imageUrl: '',
    rowdata: {} as showdata,
    location_l_rs: [{
        value: "南钩",
        label: "南钩",
    },
    {
        value: "北钩",
        label: "北钩",
    },],
    craneType: '',
    craneTypes: [
        {
            value: "链条",
            label: "链条",
        },
        {
            value: "钢丝绳",
            label: "钢丝绳",
        },
    ],
    location_l_r: '',
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
});



type showdata = {
    clength: string
    confirmer: string
    craneType: string
    description: string
    id: string
    location: string
    models: string
    operator: string
    partimgsrc: string
    shift: string
    update_date: string

}



const upload1 = ref();
const handleAvatarSuccess = (res: any, file: any) => {
    // state.imageUrl = URL.createObjectURL(file.raw);
    // state.imageUrl = URL.createObjectURL(file.raw);

    ElMessage({
        type: "success",
        message: "上传成功",
    });

};
const beforeAvatarUpload = (file: any) => {
    const isJPG = file.type === "image/jpeg";
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isJPG) {
        ElMessage.error("图片必须为JPG格式");
    }


    // return isJPG && isLt2M;
    //压缩
    return new Promise((resolve: any) => {
        compressAccurately(file, {
            size: 200,
            width: 500,
            height: 500,
        }).then((res: any) => {
            console.log(res);
            resolve(res);
        });
    });
};

// 打开弹窗
const openDialog = (rowData: showdata) => {
    console.log('rowData', rowData);
    state.isShowDialog = true
    state.rowdata = rowData

};
// 关闭弹窗
const closeDialog = (row?: object) => {

    state.isShowDialog = false;
    initForm();
};

// 取消
const onCancel = () => {
    state.imageUrl = ''
    closeDialog();
    initForm();
};


// 新增
defineExpose({ openDialog });
const emit = defineEmits(["senddata", 'initlog']);


const onSubmit = () => {
    // 做保存 更新表的操作

    service.get('update_crane_log', {
        params: {
            rowData: JSON.stringify(state.rowdata)
        }
    }).then(async res => {

        console.log('res', res);

        ElMessage({
            type: 'success',
            message: res.data.msg
        })

        state.id = res.data.id

        console.log('state.id', state.id);

        console.log('更新完成开始上传图片');




        await upload1.value.submit()
        state.imgsrc = ''
        state.imageUrl = ''
        handleClose()


    }).catch(err => {

        ElMessage({
            type: 'warning',
            message: err
        })

        handleClose()
    })

};
// 表单初始化，方法：`resetFields()` 无法使用
const initForm = () => {
    state.rowdata = {} as showdata
};
const handleClose = () => {
    state.isShowDialog = false
    state.imageUrl = ''
    initForm()
    emit('initlog')
};




const onchange = (uploadFile: UploadFile) => {
    console.log('文件状态改变', uploadFile);
    state.imageUrl = URL.createObjectURL(uploadFile.raw);

}

</script>
<style lang="less">
.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.avatar-uploader .el-upload:hover {
    border-color: #409eff;
}

.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
}

.avatar {
    width: 160px;
    height: 160px;
    display: block;
}
</style>
  