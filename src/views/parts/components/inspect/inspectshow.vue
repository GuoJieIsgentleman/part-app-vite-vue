<template>
  <div class="system-menu-container">
    <el-dialog
      :title="state.area + '巡检明细'"
      v-model="state.isShowDialog"
      width="769px"
      show-close="false"
      destroy-on-close
      close="closedialog"
    >
      <div v-if="state.isshowmaintenance1_data">
        <span> <el-tag type="warning"> 保养件未确认明细</el-tag></span>
        <el-table
          :data="state.maintenance1_data"
          style="width: 100%"
          border
          :cell-class-name="addClass"
        >
          <el-table-column prop="id" label="序号" width="60" align="center">
          </el-table-column>
          <el-table-column prop="type" label="备件类型" width="60" align="center">
          </el-table-column>
          <el-table-column prop="spec" label="型号" width="200" align="center">
          </el-table-column>
          <el-table-column prop="use_part_name" label="名称" width="140" align="center">
          </el-table-column>
          <el-table-column
            prop="use_procline"
            label="使用产线"
            width="140"
            align="center"
          >
          </el-table-column>
          <el-table-column prop="user" label="领用人" width="140" align="center">
          </el-table-column>
          <el-table-column prop="use_date" label="领用时间" width="140" align="center">
          </el-table-column>
          <el-table-column prop="use_count" label="保养数量" width="100" align="center">
          </el-table-column>
          <el-table-column prop="maintenanceman" label="保养人" width="70" align="center">
          </el-table-column>
          <el-table-column prop="useconfirm" label="确认人" width="70" align="center">
          </el-table-column>
        </el-table>
      </div>
      <div class="" v-if="state.isshowmaintenance_data">
        <span> <el-tag type="warning"> 保养件未保养明细</el-tag></span>
        <el-table
          :data="state.maintenance_data"
          style="width: 100%"
          border
          :cell-class-name="addClass"
        >
          <el-table-column prop="id" label="序号" width="60" align="center">
          </el-table-column>
          <el-table-column align="center" prop="type" label="备件类型" width="60">
          </el-table-column>
          <el-table-column align="center" prop="spec" label="型号" width="200">
          </el-table-column>
          <el-table-column align="center" prop="use_part_name" label="名称" width="140">
          </el-table-column>
          <el-table-column
            align="center"
            prop="use_procline"
            label="使用产线"
            width="140"
          >
          </el-table-column>
          <el-table-column align="center" prop="user" label="领用人" width="140">
          </el-table-column>
          <el-table-column align="center" prop="use_date" label="领用时间" width="140">
          </el-table-column>
          <el-table-column align="center" prop="use_count" label="保养数量" width="100">
          </el-table-column>
          <el-table-column align="center" prop="maintenanceman" label="保养人" width="70">
          </el-table-column>
          <el-table-column align="center" prop="useconfirm" label="确认人" width="70">
          </el-table-column>
        </el-table>
      </div>

      <div class="" v-if="state.isshowrepair_data">
        <span> <el-tag type="danger"> 外修件未申请外修</el-tag></span>
        <el-table
          :data="state.repair_data"
          style="width: 100%"
          border
          :cell-class-name="addClass1"
        >
          <el-table-column prop="id" label="序号" width="60" align="center">
          </el-table-column>
          <el-table-column prop="type" label="备件类型" width="60" align="center">
          </el-table-column>
          <el-table-column prop="spec" label="型号" width="200" align="center">
          </el-table-column>
          <el-table-column prop="use_part_name" label="名称" width="120" align="center">
          </el-table-column>
          <el-table-column prop="use_procline" label="使用产线" width="80" align="center">
          </el-table-column>
          <el-table-column prop="use_date" label="领用时间" width="140" align="center">
          </el-table-column>
          <el-table-column prop="use_count" label="外修数量" width="120" align="center">
          </el-table-column>
          <el-table-column prop="applicant" label="外修申请人" width="130" align="center">
          </el-table-column>
          <el-table-column prop="receipt" label="收货人" width="80" align="center">
          </el-table-column>
          <el-table-column prop="tryout" label="试机人" width="80" align="center">
          </el-table-column>

          <el-table-column prop="useconfirm" label="确认人" width="80" align="center">
          </el-table-column>
        </el-table>
      </div>
      <div class="" v-if="state.isshowrepair1_data">
        <span> <el-tag type="danger"> 外修件回厂未试机明细</el-tag></span>
        <el-table
          :data="state.repair1_data"
          style="width: 100%"
          border
          :cell-class-name="addClass1"
        >
          <el-table-column prop="id" label="序号" width="60" align="center">
          </el-table-column>
          <el-table-column prop="type" label="备件类型" width="60" align="center">
          </el-table-column>
          <el-table-column prop="spec" label="型号" width="200" align="center">
          </el-table-column>
          <el-table-column prop="use_part_name" label="名称" width="120" align="center">
          </el-table-column>
          <el-table-column prop="use_procline" label="使用产线" width="80" align="center">
          </el-table-column>
          <el-table-column prop="use_date" label="领用时间" width="140" align="center">
          </el-table-column>
          <el-table-column prop="use_count" label="外修数量" width="120" align="center">
          </el-table-column>
          <el-table-column prop="applicant" label="外修申请人" width="130" align="center">
          </el-table-column>
          <el-table-column prop="receipt" label="收货人" width="80" align="center">
          </el-table-column>
          <el-table-column prop="tryout" label="试机人" width="80" align="center">
          </el-table-column>

          <el-table-column prop="useconfirm" label="确认人" width="80" align="center">
          </el-table-column>
        </el-table>
      </div>
      <div class="" v-if="state.isshowrepair2_data">
        <span> <el-tag type="danger"> 外修件未回厂明细</el-tag></span>
        <el-table
          :data="state.repair2_data"
          style="width: 100%"
          border
          :cell-class-name="addClass1"
        >
          <el-table-column prop="id" label="序号" width="60" align="center">
          </el-table-column>
          <el-table-column prop="type" label="备件类型" width="60" align="center">
          </el-table-column>
          <el-table-column prop="spec" label="型号" width="200" align="center">
          </el-table-column>
          <el-table-column prop="use_part_name" label="名称" width="120" align="center">
          </el-table-column>
          <el-table-column prop="use_procline" label="使用产线" width="80" align="center">
          </el-table-column>
          <el-table-column prop="use_date" label="领用时间" width="140" align="center">
          </el-table-column>
          <el-table-column prop="use_count" label="外修数量" width="120" align="center">
          </el-table-column>
          <el-table-column prop="applicant" label="外修申请人" width="130" align="center">
          </el-table-column>
          <el-table-column prop="receipt" label="收货人" width="80" align="center">
          </el-table-column>
          <el-table-column prop="tryout" label="试机人" width="80" align="center">
          </el-table-column>

          <el-table-column prop="useconfirm" label="确认人" width="80" align="center">
          </el-table-column>
        </el-table>
      </div>

      <div class="">
        <span><el-tag type="success"> 备件明细</el-tag></span>
        <span>
          <el-select clearable  v-model="state.shelf" filterable placeholder="存放货架" clearble  @change="getinfo">
            <el-option v-for="item in state.shelfs" :key="item['value']" :label="item['label']" :value="item['value']">
            </el-option>
          </el-select>
        </span>
        <el-table
          :data="state.part_data1"
          style="width: 100%"
          :cell-class-name="addClass2"
          v-if="state.isshowpart_data"
          border
          height="400"
          show-summary
        >
          <el-table-column prop="id" label="序号" width="60" align="center">
          </el-table-column>
          <el-table-column prop="type" label="备件类型" width="60" align="center">
          </el-table-column>
          <el-table-column prop="part_name" label="名称" width="120" align="center">
          </el-table-column>
          <el-table-column prop="part_spec" label="型号" width="200" align="center">
          </el-table-column>

          <el-table-column prop="balance" label="库存" width="50" align="center">
          </el-table-column>
          <el-table-column prop="original" label="原有" width="50" align="center">
          </el-table-column>
          <el-table-column prop="area" label="存放区域" width="185" align="center">
        
          </el-table-column>
          <el-table-column prop="partimgsrc" label="图片展示" width="200" align="center">
                  <template #default="scope">
                    <div v-if="scope.row.partimgsrc != ''">
                      <el-image
                        style="width: 80px; height: 80px"
                        :preview-src-list="[scope.row.partimgsrc]"
                        :src="scope.row.partimgsrc"
                      >
                      </el-image>
                    </div>
                    <div v-else>
                      无图  
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="操作" align="center" min-width="120">
            <template #default="scope">
              <Auths :value="['btn.edit']" class="displayStyle">
                <el-button type="primary"  @click="onOpenEditMenu(scope.row, scope.$index)">编辑
                </el-button>
              </Auths>

            </template>
          </el-table-column>
        </el-table>
      </div>
      <div>
        <span>巡检备注</span>
        <el-input type="textarea" v-model="state.remark" placeholder=""></el-input>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog()">取消</el-button>
          <el-button type="primary" @click="saveinspectlog()">确认</el-button>
        </span>
      </template>
    </el-dialog>
    <UpdateArea ref="UpdateAreaRef" />
    <EditMenu ref="editMenuRef" @senddata="setdata" />
  </div>
</template>

<script lang="ts" setup>
 
import { reactive, toRefs, onUnmounted, inject,ref } from "vue";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";
import { formatDate111, subtimeminutes, subtimeminutes1 } from "/@/utils/formatTime";
import { Session } from "/@/utils/storage";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
import UpdateArea from './updateArea.vue'  
import EditMenu from "/@/views/parts/components/parts/editMenu.vue";   
const UpdateAreaRef=ref()

const  updateArea=(row:any)=>{
    console.log('row',row);
    UpdateAreaRef.value.openDialog(row)
    


}

const editMenuRef=ref()

const setdata = (v: any, v1: any) => {
  //set table 值

};  

const onOpenEditMenu = (row: object, index: any) => {
  // console.log("索引值" + index);
  // console.log(state.partslist[index]);
  // console.log("---------------------------------------");
  // console.log(row);

  editMenuRef.value.openDialog(row, index);
};


      


const state = reactive({
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
  isshowtag: false,
  area: "",
  isshowpart_data: false,
  isshowmaintenance_data: false,
  isshowmaintenance1_data: false,
  isshowrepair_data: false,
  isshowrepair1_data: false,
  isshowrepair2_data: false,
  isShowDialog: false,
  maintenance_data: [],
  maintenance1_data: [],
  repair_data: [],
  repair1_data: [],
  repair2_data: [],
  part_data: [],
  part_data1: [],
  resdata: [] as any,
  remark: "",
  cardid: "",
  time: "",
  inspectstarttime: formatDate111(new Date()),
});



const sendflag = () => {
  emit("sendflag", true);
};
const emit = defineEmits(["sendflag"]);
const saveinspectlog = () => {
  if (state.remark == "") {
    ElMessage({ type: "warning", message: "请填写巡检备注" });
  } else {
    service
      .get("/saveinspectlog", {
        params: {
          inspectdate: state.inspectstarttime,
          inspecter: Session.get("userInfo").userName,
          remark: state.remark,
          cardid: state.cardid,
          inspect_area: state.area,
        },
      })
      .then((res:any) => {
        ElMessage({
          type: "success",
          message: `巡检完成，本次巡检时间为${subtimeminutes1(
            state.inspectstarttime,
            res.data["endtime"]
          )}分钟`,
        });
        sendflag();
        initdialog();
        state.isShowDialog = false;
      })
      .catch((err:any) => {
        ElMessage({
          type: "warning",
          message: err.data,
        });
      });
  }
};
const initdialog = () => {
  state.isShowDialog = false;
  state.isshowmaintenance_data = false;
  state.isshowmaintenance1_data = false;
  state.isshowpart_data = false;
  state.isshowrepair_data = false;
  state.isshowrepair1_data = false;
  state.isshowrepair2_data = false;
  state.isshowtag = false;
  state.maintenance_data = [];
  state.repair_data = [];
  state.resdata = [];
  state.part_data = [];
  state.remark = "";
};
// 打开弹窗
const openDialog = (row?: any, time?: any, flag?: Boolean) => {
  state.isShowDialog = true;
  state.inspectstarttime = time;

  getinspection(row);
};

defineExpose({ openDialog });
// 关闭弹窗
const closeDialog = (row?: object) => {
  state.isShowDialog = false;
  sendflag();
  //关闭NFC

  initdialog();
};
// 是否内嵌下拉改变
// const onSelectIframeChange = () => {
// 	if (state.ruleForm.meta.isIframe === 'true') {
// 		state.ruleForm.isLink = 'true';
// 	} else {
// 		state.ruleForm.isLink = '';
// 	}
// };
// 取消
const onCancel = () => {
  initForm();
  closeDialog();
};
// 新增

const initForm = () => {};
const getinspection = (v: String) => {
  service
    .get("/getinspection", {
      params: {
        cardid: v,
      },
    })
    .then((res:any) => {
      state.resdata = res.data;
      console.log("state.resdata");
      console.log(state.resdata);

      state.area = state.resdata["area"];
      state.cardid = state.resdata["cardid"];
      if (state.resdata["maintenance_data"].length > 0) {
        state.maintenance_data = state.resdata["maintenance_data"].map((item: any) => {
          if (item[10] == "" && item[9] == "") {
            return {
              id: item[0],
              user: item[1],
              use_area: item[2],
              use_date: formatDate111(item[8]),
              type: item[3],
              spec: item[4],
              use_part_name: item[5],
              use_count: item[6],
              useconfirm: item[9],
              maintenanceman: item[10],
              use_procline: item[14],
            };
          }
        });

        state.maintenance_data = state.maintenance_data.filter((ele) => ele != undefined);
        state.maintenance1_data = state.resdata["maintenance_data"].map((item: any) => {
          if (item[9] == "" && item[10] != "") {
            return {
              id: item[0],
              user: item[1],
              use_area: item[2],
              use_date: formatDate111(item[8]),
              type: item[3],
              spec: item[4],
              use_part_name: item[5],
              use_count: item[6],
              useconfirm: item[9],
              maintenanceman: item[10],
              use_procline: item[14],
            };
          }
        });

        state.maintenance1_data = state.maintenance1_data.filter(
          (ele) => ele != undefined
        );

        if (state.maintenance_data.length > 0 && state.maintenance_data[0] != undefined) {
          state.isshowmaintenance_data = true;
        }
        if (
          state.maintenance1_data.length > 0 &&
          state.maintenance1_data[0] != undefined
        ) {
          state.isshowmaintenance1_data = true;
        }
      }

      if (state.resdata["repair_data"].length > 0) {
        state.repair_data = state.resdata["repair_data"].map((item: any, index: any) => {
          if (item[10] == "" && item[11] == "" && item[12] == "" && item[12] == "") {
            console.log("123");

            return {
              id: item[0],
              user: item[1],
              use_area: item[2],
              type: item[3],
              spec: item[4],
              use_part_name: item[5],
              use_count: item[6],
              use_date: formatDate111(item[8]),
              applicant: item[10],
              tryout: item[11],
              receipt: item[12],
              useconfirm: item[9],
              use_procline: item[18],
            };
          }
        });
        state.repair_data = state.repair_data.filter((ele) => ele != undefined);
        // console.log("state.repair_data");
        // console.log(state.repair_data);
        state.repair1_data = state.resdata["repair_data"].map((item: any) => {
          if (item[10] != "" && item[11] == "" && item[12] != "" && item[9] == "") {
            return {
              id: item[0],
              user: item[1],
              use_area: item[2],
              type: item[3],
              spec: item[4],
              use_part_name: item[5],
              use_count: item[6],
              use_date: formatDate111(item[8]),
              applicant: item[10],
              tryout: item[11],
              receipt: item[12],
              useconfirm: item[9],
              use_procline: item[18],
            };
          }
        });
        state.repair1_data = state.repair1_data.filter((ele) => ele != undefined);
        // console.log("state.repair1_data");
        // console.log(state.repair1_data);
        state.repair2_data = state.resdata["repair_data"].map((item: any) => {
          if (item[10] != "" && item[11] == "" && item[12] == "" && item[9] == "") {
            return {
              id: item[0],
              user: item[1],
              use_area: item[2],
              type: item[3],
              spec: item[4],
              use_part_name: item[5],
              use_count: item[6],
              use_date: formatDate111(item[8]),
              applicant: item[10],
              tryout: item[11],
              receipt: item[12],
              useconfirm: item[9],
              use_procline: item[18],
            };
          }
        });
        state.repair2_data = state.repair2_data.filter((ele) => ele != undefined);
        if (state.repair_data.length > 0) {
          state.isshowrepair_data = true;
        }
        if (state.repair1_data.length > 0) {
          state.isshowrepair1_data = true;
        }
        if (state.repair2_data.length > 0) {
          state.isshowrepair2_data = true;
        }
 
      }

      if (state.resdata["part_data"].length > 0) {
        state.part_data = state.resdata["part_data"].map((item: any) => {
          return {
            id: item[0],
            part_name: item[1],
            part_spec: item[2],
            area: item[3],
            balance: item[4],
            original: item[5],
            type: item[7],
            partimgsrc:item[8]
          };
        });
        state.part_data1=state.part_data
        state.isshowpart_data = true;
      }

      // console.log(state.part_data);
    });
};

const addClass = ({ row, column, rowIndex, columnIndex }: any) => {
  if (row) {
    return "warning-row";
  }
};
const addClass1 = ({ row, column, rowIndex, columnIndex }: any) => {
  if (row) {
    return "warning-row1";
  }
};
const addClass2 = ({ row, column, rowIndex, columnIndex }: any) => {
  if (row) {
    return "warning-row2";
  }
};


const getinfo=(val:any)=>{

console.log('val',val);

state.part_data1=state.part_data.filter((item:any)=>{
   
          return  item.area.indexOf(val)!=-1
})

}
</script>

<style lang="less">
.el-table .warning-row {
  background-color: rgb(230, 162, 60);
  color: rgb(0, 0, 0);
}
.el-table .warning-row1 {
  background-color: rgb(245, 108, 108);
  color: rgb(34, 10, 10);
}
.el-table .warning-row2 {
  background-color: rgb(103, 194, 58);
  color: rgb(28, 1, 1);
}

.warning-row el-table__header-wrapper > table > thead > tr > th > div {
  background-color: rgb(230, 162, 60) !important;
}

.warning-row1 el-table__header-wrapper > table > thead > tr > th > div {
  background-color: rgb(245, 108, 108) !important;
}

.warning-row2 el-table__header-wrapper > table > thead > tr > th > div {
  background-color: rgb(103, 194, 58) !important;
}

section
  > section
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > main
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > div
  > div
  > button
  > span {
  font-size: 50px;
  position: relative;
}
section
  > section
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > main
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > div
  > div
  > button {
  margin: 6% 6%;
}

section
  > section
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > main
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > div
  > div
  > div
  > div
  > div
  > div.el-dialog__body
  > div
  > span
  > span {
  font-size: 30px;
  padding: 10px;
  height: 50px;
}
section
  > section
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > main
  > div
  > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default
  > div
  > div
  > div
  > div
  > div
  > div
  > div.el-dialog__body
  > div:nth-child(1)
  > div
  > div.el-table__header-wrapper
  > table
  > thead {
  background-color: rgb(230, 162, 60);
}
</style>
