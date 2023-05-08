<template>
  <div class="system-menu-container">
    <el-dialog
      title="确认信息"
      v-model="state.isShowDialog"
      width="769px"
      :destroy-on-close="true"
    >
      <el-form :model="state.ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="类型">
              <el-input v-model="state.partsdetail.type" clearable disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="名称">
              <el-input disabled v-model="state.partsdetail.use_part_name" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="型号">
              <el-input disabled v-model="state.partsdetail.spec" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="结存数量">
              <el-input disabled v-model="state.ruleForm.balance" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原有数量">
              <el-input disabled v-model="state.ruleForm.original" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="保养数量">
              <el-input disabled v-model="state.partsdetail.use_count" clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="处理类型">
              <el-select v-model="state.ruleForm.scrap" placeholder="处理类型" @change="selectChange">
                <el-option
                  v-for="item in state.ruleForm.scrapOption"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原搁置区域">
              <el-input disabled v-model="state.partsdetail.use_area" clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="18" :xl="12">
            <el-form-item label="新搁置区域" label-width="80">
                 
              <el-row>
                  <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="8" :xl="12">
                    <el-select  :disabled="state.ruleForm.scrap == '报废' ? true : false" v-model="state.floor" filterable placeholder="存放楼层" clearable>
                      <el-option v-for="item in state.floors" :key="item['value']" :label="item['label']"
                        :value="item['value']">
                      </el-option>
                    </el-select>
                  </el-col>
                  <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="8" :xl="12">
                    <el-select :disabled="state.ruleForm.scrap == '报废' ? true : false" v-model="state.shelf" filterable placeholder="存放架编号" clearable>
                      <el-option v-for="item in state.shelfs" :key="item['value']" :label="item['label']"
                        :value="item['value']">
                      </el-option>
                    </el-select>
                  </el-col>
                  <el-col class="mb20"  :xs="24" :sm="12" :md="12" :lg="6" :xl="12">
                    <el-select :disabled="state.ruleForm.scrap == '报废' ? true : false" v-model="state.num" filterable placeholder="存放位置编号" clearable>
                      <el-option v-for="item in 5" :key="item" :label="item" :value="item">
                        {{ item }}
                      </el-option>
                    </el-select>
                  </el-col>

                  <el-col class="mb20" :xs="24" :sm="18" :md="18" :lg="18" :xl="18">
                   {{state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + '-' + state.num}}
                  </el-col>
                </el-row>
              <!-- <el-select
                v-model="ruleForm.area"
                placeholder="搁置区域"
                :disabled="ruleForm.scrap == '报废' ? true : false"
              >
                <el-option
                  v-for="item in ruleForm.areaArr"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select> -->
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="成套名称">
              <el-input
                :disabled="state.ruleForm.scrap != '成套' ? true : false"
                v-model="state.ruleForm.machine_part_name"
                clearable
                placeholder="选择成套后填写成套名称"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="state.ruleForm.name" placeholder="班长名" clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer
        ><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button
            type="primary"
            @click="onSubmit(state.ruleForm.name)"
            :loading="state.issave"
            size="small"
            >确定</el-button
          >
        </span></template
      >
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import {
  reactive,
  toRefs,
  defineEmits,
  defineExpose,
  inject,
  onMounted,
  onUnmounted,
} from "vue";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
import service from "/@/utils/request";
import { formatDate111 } from "/@/utils/formatTime";

import { ElMessage } from "element-plus";

    const state = reactive({
      num: '',
  shelfArea: '',
  floor: '',
  floors: [   {
        value: "值班室一楼",
        label: "值班室一楼",
      },
      {
        value: "值班室二楼",
        label: "值班室二楼",
      },
      {
        value: "方镀三线一楼",
        label: "方镀三线一楼",
      },
      {
        value: "圆镀四线一楼",
        label: "圆镀四线一楼",
      },
      {
        value: "南污水南库",
        label: "南污水南库",
      }],
  shelf: '',
  shelfs: [
    {
      value: "1号架",
      label: "1号架",
    },
    {
      value: "2号架",
      label: "2号架",
    },
    {
      value: "3号架",
      label: "3号架",
    },
    {
      value: "4号架",
      label: "4号架",
    },
    {
      value: "5号架",
      label: "5号架",
    },
    {
      value: "6号架",
      label: "6号架",
    },
    {
      value: "7号架",
      label: "7号架",
    },
    {
      value: "8号架",
      label: "8号架",
    },
    {
      value: "9号架",
      label: "9号架",
    },
    {
      value: "10号架",
      label: "10号架",
    },
    {
      value: "11号架",
      label: "11号架",
    },
    {
      value: "12号架",
      label: "12号架",
    },
    {
      value: "13号架",
      label: "13号架",
    },
    {
      value: "14号架",
      label: "14号架",
    },
    {
      value: "15号架",
      label: "15号架",
    },
  ],
      issave: false,
      isShowDialog: false,
      ruleForm: {
        machine_part_name: "",

        name: "",
        remark: "",
        areaArr: [],
        area: "",

        scrapOption: [
          {
            value: "报废",
            label: "报废",
          },
          {
            value: "不报废",
            label: "不报废",
          },
          {
            value: "外修",
            label: "外修",
          },
          {
            value: "成套",
            label: "成套",
          },
        ],
        balance: 0,
        scrap: "",
        original: 0,
      },

      confirmvalue: "",
      partsdetail: [] as any,
    });


const selectChange=(val:any)=>{
  console.log('val',val);
  if(val=='报废'){
    state.floor =''
    state.shelf=''
    state.num=''
  }
}

    const getbalance = async () => {
      let { data: balance } = await service.get("/getbalance", {
        params: {
          area: state.partsdetail.use_area,
          type: state.partsdetail.type,
          spec: state.partsdetail.spec,
          part_name: state.partsdetail.use_part_name,
        },
      });

     
      if (balance.length > 0) {
        state.ruleForm.balance = balance[0][4];
        state.ruleForm.original = balance[0][5];
      }
    };

    //初始化 产线 区域
    onMounted(async () => {
      let { data: res } = await service.get("/getarea");
      state.ruleForm.areaArr = res.map((item: any) => {
        return {
          value: item[0],
          label: item[0],
        };
      });

    });
    // 打开弹窗
    const openDialog = async (row?: any) => {
  
      state.partsdetail = row;

      state.isShowDialog = true;

      getbalance();
    };

    defineExpose({openDialog})
    // 关闭弹窗
    const closeDialog = (row?: object) => {
      state.isShowDialog = false;
    };
    // 取消
    const onCancel = () => {
      closeDialog();
      initForm();
    };
    // 新增

    //确认提交
    const initmaintenance: any = inject("initmaintenance");

    const onSubmit = (v: any) => {
      if (v == "") {
        ElMessage.warning({
          message: "请重新输入",
          type: "warning",
        });
      } else if (state.partsdetail.maintenanceman == "") {
        ElMessage.warning({
          message: "保养人未确认",
          type: "warning",
        });
      } else {
        //更新确认人
        service
          .get("/updatemaintenance", {
            params: {
              //保养列表的id 不是parts 的id
              id: state.partsdetail.id,
              useconfirm: state.ruleForm.name,
              use_count: state.partsdetail.use_count,
              use_area: state.partsdetail.use_area,
              use_date: formatDate111(state.partsdetail.use_date),
              use_part_name: state.partsdetail.use_part_name,
              type: state.partsdetail.type,
              spec: state.partsdetail.spec,
              new_area: state.floor + state.shelf + state.shelf.substring(0, state.shelf.length - 2) + '-' + state.num,
              maintenanceman: state.partsdetail.maintenanceman,
              maintenance_date: state.partsdetail.maintenance_date,
              scrap: state.ruleForm.scrap,
              flag: state.partsdetail.remark,
              user: state.partsdetail.user,
              use_procline: state.partsdetail.use_procline,
              useconfirmdate: formatDate111(new Date()),
              machine_part_name: state.ruleForm.machine_part_name,
            },
          })
          .then((res) => {
            ElMessage.success({
              message: res.data,
              type: "success",
            });
            initmaintenance("all");
            closeDialog();
          })
          .catch((err) => {
            ElMessage.warning({
              message: err.data,
              type: "warning",
            });
          });
      }

      // 关闭弹窗
      // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
    };
    // 表单初始化，方法：`resetFields()` 无法使用
    const initForm = () => {
      state.ruleForm.name = "";
      // state.ruleForm.part_spec = "";
      state.ruleForm.area = "";
      // state.ruleForm.balance = "";
      // state.ruleForm.original = "";
      // state.ruleForm.remark = "";

      // state.ruleForm.type = "";
    };
    onUnmounted(initForm);
 
</script>
