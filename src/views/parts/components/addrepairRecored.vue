<template>
  <div class="system-menu-container">
    <el-dialog
      title="新增外修记录"
      v-model="isShowDialog"
      width="769px"
      close-on-press-escape
      :destroy-on-close="true"
      @close="closeDialog"
    >
      <el-form :model="ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用人">
              <el-input v-model="ruleForm.user" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="使用产线">
              <el-select
                v-model="ruleForm.model"
                key
                placeholder=""
                @change="gettype(ruleForm.model)"
              >
                <el-option
                  v-for="item in ruleForm.userarea"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
              <!-- <el-input v-model="ruleForm.use_area" placeholder clearable></el-input> -->
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件类型">
              <el-select
                v-model="ruleForm.model1"
                placeholder=""
                @change="getspesc(ruleForm.model1)"
              >
                <el-option
                  v-for="item in ruleForm.usetype"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
              <!-- <el-input v-model="ruleForm.use_area" placeholder clearable></el-input> -->
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件型号">
              <el-select
                v-model="ruleForm.model2"
                placeholder=""
                @change="getpartname(ruleForm.model2)"
              >
                <el-option
                  v-for="item in ruleForm.usespesc"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
              <!-- <el-input v-model="ruleForm.use_area" placeholder clearable></el-input> -->
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件名称">
              <el-select
                v-model="ruleForm.model3"
                placeholder=""
                @change="getbalance(ruleForm.model3)"
              >
                <el-option
                  v-for="item in ruleForm.part_name"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用数量">
              <el-input placeholder="请输入数量" v-model="ruleForm.use_count">
                <template #prepend>区域库存为:{{ ruleForm.balance }}</template>
              </el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原因">
              <!-- <el-input placeholder v-model="ruleForm.user_remark"></el-input> -->
              <!-- <el-select v-model="model" placeholder="">
                <el-option
                  v-for="item in userarea"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select> -->
              <el-input placeholder="原因" v-model="ruleForm.reason"> </el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备注">
              <el-input placeholder v-model="ruleForm.user_remark"></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="领用时间">
              <el-date-picker
                class="el-date-table"
                v-model="ruleForm.use_date"
                type="datetime"
                value-format="YYYY-MM-DD HH:mm:ss"
                placeholder="选择日期时间"
              >
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="确认人">
              <el-input v-model="ruleForm.confirm" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer
        ><span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="issave" size="small"
            >保存</el-button
          >
        </span></template
      >
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { reactive, toRefs, onUnmounted, inject } from "vue";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";

// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
export default {
  name: "systemAddRecoredMenu",
  setup() {
    const state = reactive({
      value: "",
      issave: false,
      isShowDialog: false,
      shortcuts: [
        {
          text: "今天",
          value: new Date(),
        },
        {
          text: "昨天",
          value: () => {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24);
            return date;
          },
        },
        {
          text: "一周前",
          value: () => {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
            return date;
          },
        },
      ],
      /**
       * 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式（请注意参数类型！）
       * 受到 `element plus` 类型 `string/number/object` 影响，不可使用 `:value="true"`
       * 的写法，所以传值到后台时，需要转换成布尔值，否则页面可能出现玄学。
       * 路由权限标识为数组格式，基本都需要自行转换类型
       */
      ruleForm: {
        confirm: "",
        model: "",
        model1: "",
        model2: "",
        model3: "",
        reason: "",
        balance: 0,
        userarea: [],
        usetype: [],
        usespesc: [],
        part_name: [],
        user: "",
        use_area: "",
        use_part_name: "",
        use_count: 0,
        user_remark: "",
        use_date: "",
      },
    });

    const gettype = async (value?: any) => {
      console.log("进来了");
      console.log(value);

      //通过area 找type

      let { data: type } = await service.get("/api/gettype", { params: { area: value } });

      state.ruleForm.usetype = type.map((item: any) => {
        return {
          value: item[0],
          label: item[0],
        };
      });
    };

    const getspesc = async (value?: any) => {
      console.log("进来了");
      console.log(value);

      //通过area 找type

      let { data: type } = await service.get("/api/getspesc", {
        params: { area: state.ruleForm.model, type: value },
      });

      state.ruleForm.usespesc = type.map((item: any) => {
        return {
          value: item[2],
          label: item[2],
        };
      });
    };

    const getpartname = async (value?: any) => {
      //通过area 找type

      let { data: partname } = await service.get("/api/getpartname", {
        params: {
          area: state.ruleForm.model,
          type: state.ruleForm.model1,
          spec: state.ruleForm.model2,
        },
      });

      console.log("partname");

      state.ruleForm.part_name = partname.map((item: any) => {
        return {
          value: item[1],
          label: item[1],
          count: item[4],
        };
      });
    };

    const getbalance = async (value?: any) => {
      let { data: balance } = await service.get("/api/getbalance", {
        params: {
          area: state.ruleForm.model,
          type: state.ruleForm.model1,
          spec: state.ruleForm.model2,
          part_name: value,
        },
      });

      console.log("balance");
      console.log(balance);
      state.ruleForm.balance = balance[0][4];
    };

    // 打开弹窗

    const openDialog = async (row?: object) => {
      state.isShowDialog = true;

      // 领用区域获取
      let { data: res } = await service.get(`/api/getusearea`);
      console.log(res);
      state.ruleForm.userarea = res.map((item: any) => {
        return {
          value: item[0],
          label: item[0],
        };
      });
    };
    // 关闭弹窗
    const closeDialog = (row?: object) => {
      initForm();
      state.isShowDialog = false;
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
      closeDialog();
      initForm();
    };
    // 新增

    const initrepair: any = inject("initrepair");
    const onSubmit = async () => {
      //验证处理

      if (state.ruleForm.use_count <= state.ruleForm.balance) {
        if (state.ruleForm.balance <= 0) {
          ElMessage.warning("库存不足");
          state.ruleForm.use_count = 0;
        } else {
          //提交 保存  做非空验证
          let { data: res } = await service.get("/api/addrepair", {
            params: {
              user: state.ruleForm.user,
              area: state.ruleForm.model,
              type: state.ruleForm.model1,
              spec: state.ruleForm.model2,
              part_name: state.ruleForm.model3,
              use_count: state.ruleForm.use_count,
              reason: state.ruleForm.reason,
              use_date: state.ruleForm.use_date,
              confirm: state.ruleForm.confirm,
            },
          });
          closeDialog();
        }
      } else {
        ElMessage.warning("领用件数不能大于库存件数，请重新输入");
        state.ruleForm.use_count = 0;
      }

      // let { data: res } = await service.get("/api/adduserecord", {
      //   params: {
      //     ruleForm: state.ruleForm,
      //   },
      // });

      // 数据，请注意需要转换的类型
      // 关闭弹窗
      //给父组件发送 调用方法 刷新数据
      initrepair();
      //setBackEndControlRefreshRoutes(); // 刷新菜单，未进行后端接口测试
    };
    // 表单初始化，方法：`resetFields()` 无法使用
    const initForm = () => {
      state.ruleForm.user = "";
      state.ruleForm.use_area = "";
      state.ruleForm.use_part_name = "";
      state.ruleForm.use_count = 0;
      state.ruleForm.user_remark = "";
      (state.value = ""),
        (state.ruleForm.model = ""),
        (state.ruleForm.model1 = ""),
        (state.ruleForm.model2 = ""),
        (state.ruleForm.model3 = ""),
        (state.ruleForm.userarea = []),
        (state.ruleForm.usetype = []),
        (state.ruleForm.usespesc = []),
        (state.ruleForm.part_name = []);
      state.ruleForm.use_date = "";
      state.ruleForm.balance = 0;
      state.ruleForm.reason = "";
    };
    0;
    return {
      openDialog,
      closeDialog,
      onCancel,
      onSubmit,
      ...toRefs(state),
      gettype,
      getspesc,
      getpartname,
      getbalance,
    };
  },
};
</script>
