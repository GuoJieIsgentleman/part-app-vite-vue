<template>
    <div class="system-menu-container">
        <el-dialog title="班长确认信息" @close="initform" v-model="isShowDialog" width="769px">
            <el-form :model="FormData" size="small" label-width="80px">

                <el-row :gutter="35">
                    <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
                        <el-form-item label="确认人">
                            <el-input v-model="confirm" placeholder></el-input>
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
import { ElMessage } from 'element-plus';
import { ref } from 'vue';
import service from '/@/utils/request';


const FormData = ref<any>()

const confirm = ref('')

const isShowDialog = ref(false)


const id = ref<number>()
const openDialog = (row: any, index: number) => {
    isShowDialog.value = true
    FormData.value = row
    id.value = row.id
}


const issave = ref(false)

const initform = () => {
    isShowDialog.value = false
    confirm.value = ''

}

const emits = defineEmits(['init'])


const onCancel = () => {
    isShowDialog.value = false
    confirm.value = ''
}

const onSubmit = () => {
    issave.value = true

    if (confirm.value == '') {
        ElMessage({
            type: 'warning',
            message: '请填写确认人'
        })
        return
    }

    service.get('crane_confirm', {
        params: {
            name: confirm.value,
            id: id.value
        }
    }).then(res => {
        ElMessage({
            type: 'success',
            message: '保存成功'
        })

        emits('init')

    }).catch(err => {
        ElMessage({
            type: 'warning',
            message: err
        })
    })
    issave.value = false

    isShowDialog.value = false

}
defineExpose({ openDialog })



</script>

<style scoped></style>