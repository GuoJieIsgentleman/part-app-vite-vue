<template>
  <div class="system-menu-container">
    <el-dialog title="修改密码" v-model="isShowDialog" width="769px">
      <el-form :model="ruleForm" size="small" label-width="80px">
        <el-row>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="账号">
              <el-input v-model="userlist.username" disabled clearable> </el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="密码">
              <el-input
                v-model="ruleForm.password"
                placeholder="密码"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="角色">
              <el-select v-model="ruleForm.role" placeholder="选择角色">
                <el-option
                  v-for="item in ruleForm.rolelist"
                  :key="item['value']"
                  :label="item['label']"
                  :value="item['value']"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="区域授权">
              <el-select
                v-model="ruleForm.value1"
                multiple
                placeholder="Select"
                style="width: 240px"
              >
                <el-option
                  v-for="item in ruleForm.Responsible_area"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" size="small">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { reactive, toRefs, onMounted, inject } from "vue";
import IconSelector from "/@/components/iconSelector/index.vue";
import { useI18n } from "vue-i18n";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";
// import Message from "element-plus/lib/el-message/src/message";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
export default {
  name: "systemEditMenu2",
  components: { IconSelector },
  setup() {
    const { t } = useI18n();
    const state = reactive({
      userlist: [] as any,
      isShowDialog: false,
      /**
       * 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式（请注意参数类型！）
       * 受到 `element plus` 类型 `string/number/object` 影响，不可使用 `:value="true"`
       * 的写法，所以传值到后台时，需要转换成布尔值，否则页面可能出现玄学。
       * 路由权限标识为数组格式，基本都需要自行转换类型
       */
      ruleForm: {
        value1: "",
        Responsible_area: [
          {
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
            value: "方镀三线二楼",
            label: "方镀三线二楼",
          },
          {
            value: "圆镀四线一楼",
            label: "圆镀四线一楼",
          },
          {
            value: "圆镀四线二楼",
            label: "圆镀四线二楼",
          },
          {
            value: "南污水南库",
            label: "南污水南库",
          },
          {
            value: "南污水北库",
            label: "南污水北库",
          },
        ],
        name: "", // 路由名称
        component: "", // 组件地址
        isLink: "", // 是否外链
        menuSort: "", // 菜单排序
        meta: {
          title: "", // 菜单名称
          icon: "", // 菜单图标
          isHide: "", // 是否隐藏
          isKeepAlive: "", // 是否缓存
          isAffix: "", // 是否固定
          isLink: "", // 是否外链，开启外链条件，`1、isLink:true 2、链接地址不为空`
          isIframe: "", // 是否内嵌，开启条件，`1、isIframe:true 2、链接地址不为空`
          auth: "", // 路由权限标识（多个请用逗号隔开），最后转成数组格式
        },
        username: "",
        password: "",
        rolelist: [],
        role: "",
      },
    });

    onMounted(async () => {
      //获取角色
      let { data: res } = await service.get("/getrolelist");

      state.ruleForm.rolelist = res.map((item: any) => {
        return {
          value: item[2],
          label: item[1],
        };
      });

      console.log("获取橘色");
      console.log(res);
      // state.ruleForm.rolelist = res;
    });
    // 打开弹窗
    const openDialog = (row: any) => {
      state.userlist = row;
      state.ruleForm.role = state.userlist.role;
      state.isShowDialog = true;
      console.log("state.ruleForm.role111");
      console.log(state.ruleForm.role);
    };
    // 关闭弹窗
    const closeDialog = (row?: object) => {
      console.log(row);
      state.isShowDialog = false;
    };
    // 是否内嵌下拉改变
    const onSelectIframeChange = () => {
      if (state.ruleForm.meta.isIframe === "true") {
        state.ruleForm.isLink = "true";
      } else {
        state.ruleForm.isLink = "";
      }
    };
    // 取消
    const onCancel = () => {
      closeDialog();
      initForm();
    };
    // 新增
    const inituseData: any = inject("inituseData");
    const onSubmit = () => {
      console.log(state.ruleForm.value1); // 数据，请注意需要转换的类型

      console.log(state.ruleForm.value1.length); // 数据，请注意需要转换的类型

      for (let index = 0; index < state.ruleForm.value1.length; index++) {
        console.log(state.ruleForm.value1[index]);
      }
      console.log("state.ruleForm.role");
      console.log(state.ruleForm.role);

      //更新用户

      service
        .get("/updateuser", {
          params: {
            username: state.userlist.username,
            password: state.ruleForm.password,
            role: state.ruleForm.role,
            area: JSON.stringify(state.ruleForm.value1),
            flag: "编辑",
          },
        })
        .then((res) => {
          ElMessage.success(res.data);
        });
      inituseData();
      closeDialog(); // 关闭弹窗

      // setBackEndControlRefreshRoutes() // 刷新菜单，未进行后端接口测试
    };
    // 表单初始化，方法：`resetFields()` 无法使用
    const initForm = () => {
      state.ruleForm.name = "";
      state.ruleForm.component = "";
      state.ruleForm.isLink = "";
      state.ruleForm.menuSort = "";
      state.ruleForm.meta.title = "";
      state.ruleForm.meta.icon = "";
      state.ruleForm.meta.isHide = "";
      state.ruleForm.meta.isKeepAlive = "";
      state.ruleForm.meta.isAffix = "";
      state.ruleForm.meta.isLink = "";
      state.ruleForm.meta.isIframe = "";
      state.ruleForm.meta.auth = "";
    };
    return {
      openDialog,
      closeDialog,
      onSelectIframeChange,
      onCancel,
      onSubmit,
      ...toRefs(state),
    };
  },
};
</script>
