<template>
  <div class="system-menu-container">
    <el-dialog title="新增菜单" v-model="isShowDialog" width="500px">
      <el-form :model="ruleForm" size="small" label-width="80px">
        <el-row :gutter="35">
          <!-- <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="是否缓存">
              <el-select
                v-model="ruleForm.meta.isKeepAlive"
                placeholder="请选择是否缓存"
                clearable
                class="w100"
              >
                <el-option label="是" value="true"></el-option>
                <el-option label="否" value="false"></el-option>
              </el-select>
            </el-form-item>
          </el-col> -->

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
            <el-form-item label="用户名">
              <el-input v-model="ruleForm.username" placeholder="用户名" clearable>
              </el-input>
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
              <el-select v-model="ruleForm.role" placeholder="更改角色">
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
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel" size="small">取 消</el-button>
          <el-button type="primary" @click="onSubmit" size="small">新 增</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { reactive, toRefs, onMounted, inject } from "vue";
import IconSelector from "/@/components/iconSelector/index.vue";
import service from "/@/utils/request";
import { ElMessage } from "element-plus";
// import { setBackEndControlRefreshRoutes } from "/@/router/backEnd";
export default {
  name: "systemAddMenu",
  components: { IconSelector },
  setup() {
    const state = reactive({
      isShowDialog: false,
      /**
       * 参数请参考 `/src/router/route.ts` 中的 `dynamicRoutes` 路由菜单格式（请注意参数类型！）
       * 受到 `element plus` 类型 `string/number/object` 影响，不可使用 `:value="true"`
       * 的写法，所以传值到后台时，需要转换成布尔值，否则页面可能出现玄学。
       * 路由权限标识为数组格式，基本都需要自行转换类型
       */
      ruleForm: {
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
        role: "",
        rolelist: [],
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
    const openDialog = (row?: object) => {
      console.log(row);
      state.isShowDialog = true;
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
      //检测 并且提交
      service
        .get("adduser", {
          params: {
            username: state.ruleForm.username,
            password: state.ruleForm.password,
            role: state.ruleForm.role,
          },
        })
        .then((res) => {
          console.log("onSubmit回复");
          console.log(res);
          if (res.data == "添加成功") {
            ElMessage.success("添加成功");
          } else {
            ElMessage.warning(res.data);
          }

          inituseData();
        });

      console.log(state.ruleForm); // 数据，请注意需要转换的类型
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
