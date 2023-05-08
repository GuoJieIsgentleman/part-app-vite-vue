<template>
    <div class="system-menu-container">
        <el-dialog title="钢丝绳记录的添加" @close="initform" v-model="state.isShowDialog" width="769px">
            <el-form :model="state" size="small" label-width="80px">

                <el-row :gutter="35">
                    <el-col :span="6" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="天车维修图片">
                            <el-upload class="avatar-uploader" ref="upload" :on-change="imgpreivew" :auto-upload="false"
                                :action="
                                    'https://www.ssxyf.cn:5556/Crane_img_uploadfile?imgid=' +
                                    state.id +
                                    '&&time1=' +
                                    new Date().getTime().toString()
                                " :show-file-list="false" :on-success="handleAvatarSuccess"
                                :before-upload="beforeAvatarUpload">
                                <!-- <img v-if="ruleForm.imageUrl" :src="ruleForm.imageUrl" class="avatar" /> -->
                                <img v-if="state.imageUrl" :src="state.imageUrl" class="imgstyle" />
                                <el-icon v-else class="avatar-uploader-icon">待上传</el-icon>
                                <!-- <ElIcon v-else class="el-icon-plus avatar-uploader-icon"></ElIcon> -->
                            </el-upload>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="更换日期">
                            <el-input v-model="new_date" placeholder clearable disabled></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="产线">

                            <el-select v-model="state.shift" class="m-2" placeholder="产线" size="large">
                                <el-option v-for="item in state.use_proline_options" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="更换位置">
                            <el-row>


                                <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                                    <el-select v-model="location" class="m-2" placeholder="天车名称" size="large">
                                        <el-option v-for="item in state.crane_name_options" :key="item.value"
                                            :label="item.label" :value="item.value" />
                                    </el-select>
                                </el-col>
                                <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                                    <el-select v-model="state.location_l_r" class="m-2" placeholder="(南钩/北钩)" size="large">
                                        <el-option v-for="item in state.location_l_rs" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-col>
                            </el-row>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="故障描述">
                            <el-input v-model="description" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="规格型号">
                            <el-input v-model="models" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>

                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="长度(米)">
                            <el-input v-model="clength" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="更换人">
                            <el-input v-model="operator" placeholder clearable></el-input>
                        </el-form-item>
                    </el-col>


                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="类别">
                            <el-select v-model="craneType" class="m-2" placeholder="类别" size="large">
                                <el-option v-for="item in state.craneTypes" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </el-form-item>
                    </el-col>


                </el-row>

            </el-form><template #footer><span class="dialog-footer">
                    <el-button @click="onCancel" size="small">取 消</el-button>
                    <el-button type="primary" @click="onSubmit" :loading="issave" size="small">保存</el-button>
                </span></template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">

import { ElIcon, ElMessage } from 'element-plus';
import { compressAccurately } from 'image-conversion';
import { onMounted, reactive, ref, toRefs } from 'vue';
import { formatDate111 } from '/@/utils/formatTime';
import service from '/@/utils/request';
import { Session } from '/@/utils/storage';






const state = reactive({
    id: '',
    imageUrl: '',
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
    isShowDialog: false,
    new_date: formatDate111(new Date()),
    models: '',
    location: '',
    description: '',
    clength: '',
    operator: Session.get("userInfo").userName,
    confirmer: '',
    remark: '',
    issave: false,
    shift: ''
})






let { shift, craneType, new_date, isShowDialog, models, location, description, clength, operator, confirmer, remark, issave } = toRefs(state)
const openDialog = (row?: object) => {
    state.isShowDialog = true;
};


const closeDialog = (row?: object) => {
    console.log(row);
    state.isShowDialog = false;
    initform()
};


const onCancel = () => {
    closeDialog()
}






const onSubmit = () => {

    if (state.models === '' || state.location == '' || state.location_l_r == '') {
        ElMessage({
            type: 'warning',
            message: '请完善信息'
        })
        return
    }

    service.post('add_crane_log', {

        new_date: state.new_date,
        models: state.models,
        location: state.location + state.location_l_r,
        description: state.description,
        clength: state.clength,
        operator: state.operator,
        confirmer: state.confirmer,
        craneType: state.craneType,
        shift: state.shift

    }).then((res: any) => {
        console.log('生成的id');


        state.isShowDialog = false
        ElMessage({
            type: 'success',
            message: res.data.msg
        })

        state.id = res.data.id

        console.log('state.id', state.id);


        upload.value.submit();

        emits('updatelog', { flag: 'success' })

        initform()
    }).catch((err: any) => {

    })
}

const initform = () => {
    state.confirmer = ''
    state.description = ''
    state.isShowDialog = false
    state.issave = false
    state.clength = ''
    state.models = ''
    state.new_date = formatDate111(new Date())
    state.shift = ''
    state.remark = ''
    state.location = ''
    state.operator = ''
}


const emits = defineEmits(['updatelog'])


defineExpose({ openDialog });


const upload = ref()

const handleAvatarSuccess = (res: any, file: any) => {
    state.imageUrl = URL.createObjectURL(file.raw);
    // ElMessage({
    //   type: "success",
    //   message: "上传成功",
    // });
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
        // compress(file, 100).then((res) => {
        //   console.log(res);
        //   resolve(res);
        // });

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
const imgpreivew = (file: any) => {
    //图片的raw 转换为url
    state.imageUrl = URL.createObjectURL(file.raw);
};

</script>

<style scoped >
.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 5px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 20px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
    vertical-align: center;
    top: 50%;
}


.imgstyle {
    width: 80px;
    height: 80px;
}
</style>