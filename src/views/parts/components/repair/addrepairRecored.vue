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
              <el-select v-model="ruleForm.model" key placeholder="">
                <el-option
                  v-for="item in use_proline_options"
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
              <el-input v-model="ruleForm.model1" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件型号">
              <el-input v-model="ruleForm.model2" placeholder clearable></el-input>
            </el-form-item>
          </el-col>
          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="备件名称">
              <el-input v-model="ruleForm.model3" placeholder clearable></el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="外修数量">
              <el-input placeholder="请输入数量" v-model="ruleForm.use_count"> </el-input>
            </el-form-item>
          </el-col>

          <el-col class="mb20" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="原因">
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
              <el-input
                :disabled="true"
                v-model="ruleForm.use_date"
                placeholder=""
              ></el-input>
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

import { formatDate111 } from "/@/utils/formatTime";
import { Session } from "/@/utils/storage";

// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
export default {
  name: "systemAddRecoredMenu",
  setup() {
    const state = reactive({
      options: [
        {
          value: "保养",
          label: "保养",
        },
        {
          value: "外修",
          label: "外修",
        },
        {
          value: "报废",
          label: "报废",
        },
        {
          value: "设备整改",
          label: "设备整改",
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
        },
        {
          value: "圆镀料场",
          label: "圆镀料场",
        },
        {
          value: "方镀料场",
          label: "方镀料场",
        },
        {
          value: "锌锭库天车",
          label: "锌锭库天车",
        },
        {
          value: "锅炉房",
          label: "锅炉房",
        },
        {
          value: "换热站",
          label: "换热站",
        },
        {
          value: "空压机房",
          label: "空压机房",
        },
        {
          value: "配电室",
          label: "配电室",
        },
      ],
      value: "",
      issave: false,
      isShowDialog: false,

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

        user: Session.get("userInfo").userName,

        use_area: "",
        use_part_name: "",
        use_count: 0,
        user_remark: "",
        use_date: formatDate111(new Date()),
      },
    });

    //

    // 打开弹窗

    const openDialog = async (row?: object) => {
      state.isShowDialog = true;

      // 领用区域获取

      let { data: res } = await service.get(`/getusearea`);

      console.log(res);
      state.ruleForm.userarea = res.map((item: any) => {
        return {
          value: item[0],
          label: item[0],
        };
      });

      state.ruleForm.use_date = formatDate111(new Date());
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

    const onSubmit = () => {
      //验证处理

      if (
        state.ruleForm.use_count <= 0 ||
        state.ruleForm.model1 == "" ||
        state.ruleForm.model2 == "" ||
        state.ruleForm.model3 == ""
      ) {
        ElMessage({ type: "error", message: "请正确填写各个选项" });
        //提交 保存  做非空验证
      } else {
        let res = service
          .get("/addrepair", {
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

              flag: "无库存备件外修",
            },
          })
          .then((res) => {
            ElMessage({ type: "success", message: res.data });
            initrepair();
            closeDialog();
            initForm();
          });
      }
    };

    // let { data: res } = await service.get("/adduserecord", {
    //   params: {
    //     ruleForm: state.ruleForm,
    //   },
    // });

    // 数据，请注意需要转换的类型
    // 关闭弹窗
    //给父组件发送 调用方法 刷新数据

    //setBackEndControlRefreshRoutes(); // 刷新菜单，未进行后端接口测试

    // 表单初始化，方法：`resetFields()` 无法使用
    const initForm = () => {
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

    return {
      openDialog,
      closeDialog,
      onCancel,
      onSubmit,
      ...toRefs(state),

      // gettype,
      // getspesc,
      // getpartname,
      // getbalance,
    };
  },
};
</script>
