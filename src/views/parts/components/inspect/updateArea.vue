<template>
    <div>
        <el-dialog v-model="state.ishow" title="更新存放区域">
    <el-form :model="state.form">
      <el-form-item label="新的存放区域" >
        <el-input v-model="state.area"   :placeholder="state.row.area" autocomplete="off" />
      </el-form-item>
    
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="state.ishow = false">Cancel</el-button>
        <el-button type="primary" @click="submit()"
          >Confirm</el-button
        >
      </span>
    </template>
  </el-dialog>  
    </div>
</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus';
import {ref,reactive,toRefs} from 'vue'
import service from '/@/utils/request';
import { Session } from '/@/utils/storage';

const state=reactive({
    ishow:false,
    row:null as any,
    area:'',
    form:{

    }
})


const openDialog=(row:any)=>{
    state.row=row
    state.ishow=true
}


const submit=()=>{
    if(state.area==''){
        ElMessage({type:'warning',message:'请填写新的区域'})
        return
    }

    service.get('updatepart',{
        params:{
            id:state.row.id,
            area:state.area,
            username:Session.get('userinfo').userName,
            flag:'巡检区域更换'
        }
    }).then((res:any)=>{
        ElMessage({type:'success',message:res.data})
        init()
        state.ishow=false
    }).catch((err:any)=>{
        ElMessage({type:'error',message:'出错'})
    })

}

const init=()=>{
    state.area=''
    state.form={}
    state.row=null
}

defineExpose({openDialog})

const closeDialog=()=>{
    state.ishow=false
}

</script>

<style lang="scss" scoped>

</style>