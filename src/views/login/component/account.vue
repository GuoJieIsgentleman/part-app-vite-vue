<template>
  <el-form class="login-content-form">
    <el-form-item>
      <el-input
        type="text"
        placeholder="请输入账号"
        prefix-icon="el-icon-user"
        v-model="ruleForm.userName"
        clearable
        autocomplete="off"
      >
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-input
        :type="isShowPassword ? 'text' : 'password'"
        placeholder="请输入密码"
        prefix-icon="el-icon-lock"
        v-model="ruleForm.password"
        autocomplete="off"
      >
        <template #suffix>
          <i
            class="iconfont el-input__icon login-content-password"
            :class="isShowPassword ? 'icon-yincangmima' : 'icon-xianshimima'"
            @click="isShowPassword = !isShowPassword"
          >
          </i>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item>
      <!-- <el-row :gutter="15">
        <el-col :span="16">
          <el-input
            type="text"
            maxlength="4"
            :placeholder="$t('message.account.accountPlaceholder3')"
            prefix-icon="el-icon-position"
            v-model="ruleForm.code"
            clearable
            autocomplete="off"
          ></el-input>
        </el-col>
        <el-col :span="8">
          <div class="login-content-code">
            <span class="login-content-code-img">1234</span>
          </div>
        </el-col>
      </el-row> -->
    </el-form-item>
    <el-form-item>
      <el-button
        type="primary"
        class="login-content-submit"
        round
        @click="onSignIn"
        :loading="loading.signIn"
      >
        <span>{{ $t("message.account.accountBtnText") }}</span>
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import { toRefs, reactive, defineComponent, computed, getCurrentInstance } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { useI18n } from "vue-i18n";
import { initFrontEndControlRoutes } from "/@/router/frontEnd";
import { initBackEndControlRoutes } from "/@/router/backEnd";
import { useStore } from "/@/store/index";
import { Session } from "/@/utils/storage";
import { formatAxis } from "/@/utils/formatTime";
import service from "/@/utils/request";
import { NextLoading } from '/@/utils/loading';
export default defineComponent({
  name: "login",
  setup() {
    const { t } = useI18n();
    const { proxy } = getCurrentInstance() as any;
    const store = useStore();
    const route = useRoute();
    const router = useRouter();
    const state = reactive({
      isShowPassword: false,
      ruleForm: {
        userName: "",
        password: "",

        code: "1234",
      },
      loading: {
        signIn: false,
      },
    });
    // 时间获取
    const currentTime = computed(() => {
      return formatAxis(new Date());
    });
    // 登录

    const onSignIn = () => {


      if(state.ruleForm.userName=="" ||state.ruleForm.password==""){
        ElMessage({type:'warning',message:'请输入用户名或者密码'})
        return
      }


      state.loading.signIn = true;
      //验证密码账号
      service
        .post("/Verify", {
          userName: state.ruleForm.userName,
          password: state.ruleForm.password,
        })
        .then(  (res:any) => {
          if (res.data.flag == "success") {
            // admin 页面权限标识，对应路由 meta.auth，用于控制路由的显示/隐藏
            let adminAuthPageList: Array<string> = ["admin"];
            // admin 按钮权限标识
            let adminAuthBtnList: Array<string> = [
              "btn.add",
              "btn.del",
              "btn.edit",
              "btn.link",
            ];
            
            console.log('res account',res);
            

            // test 页面权限标识，对应路由 meta.auth，用于控制路由的显示/隐藏
            let defaultAuthPageList: Array<string> = [res.data.auth];
            // test 按钮权限标识
            let defaultAuthBtnList: Array<string> = JSON.parse(res.data.btn_auth);
           
            // 用户信息模拟数据
            const userInfos = {
              userName: state.ruleForm.userName,
              photo:
                state.ruleForm.userName === "admin"
                  ? "http://61.185.74.251:5556/static/avatar/use.jpg"
                  : "http://61.185.74.251:5556/static/avatar/use.jpg",
              time: new Date().getTime(),
              authPageList: defaultAuthPageList,
              authBtnList: defaultAuthBtnList,
              areainfo: JSON.parse(res.data.areainfo),
              btn_auth: JSON.parse(res.data.btn_auth),
            };

            // 存储 token 到浏览器缓存
            Session.set("token", Math.random().toString(36).substr(0));
            // 存储用户信息到浏览器缓存
            Session.set("userInfo", userInfos);

            // 1、请注意执行顺序(存储用户信息到vuex)
            store.dispatch("userInfos/setUserInfos", userInfos);

            // if (!store.state.themeConfig.themeConfig.isRequestRoutes) {
            //   // 前端控制路由，2、请注意执行顺序
            //   await initFrontEndControlRoutes();
            //   signInSuccess();
            // } else {

           // 模拟后端控制路由，isRequestRoutes 为 true，则开启后端控制路由
             // 添加完动态路由，再进行 router 跳转，否则可能报错 No match found for location with path "/"
            //   await initBackEndControlRoutes();
            //   // 执行完 initBackEndControlRoutes，再执行 signInSuccess
            //   signInSuccess();
            // }

            // 模拟后端控制路由，isRequestRoutes 为 true，则开启后端控制路由
            // 添加完动态路由，再进行 router 跳转，否则可能报错 No match found for location with path "/"
            initBackEndControlRoutes();
            // 执行完 initBackEndControlRoutes，再执行 signInSuccess
            signInSuccess();
          } else {
            ElMessage({
              showClose: true,
              message: res.data,
              type: "error",
            });
            state.loading.signIn = !state.loading.signIn;
          }
        })
        .catch((err:any) => {
          console.log("err");
          console.log(err);

          state.loading.signIn = !state.loading.signIn;
          ElMessage({
            showClose: true,
            message: err.data,
            type: "error",
          });
        });
    };
    // 登录成功后的跳转
    const signInSuccess = async () => {
      // 初始化登录成功时间问候语
      console.log("进行跳转0");
      let currentTimeInfo = currentTime.value;
      // 登录成功，跳到转首页
      // 添加完动态路由，再进行 router 跳转，否则可能报错 No match found for location with path "/"
      // 如果是复制粘贴的路径，非首页/登录页，那么登录成功后重定向到对应的路径中
      await initBackEndControlRoutes();
      
      if (route.query?.redirect) {
        console.log('route.query?.redirect',route.query?.redirect);
        
        router.push({
          path: route.query?.redirect as string,
          query:
            Object.keys(route.query?.params as any).length > 0
              ? JSON.parse(route.query?.params as any)
              : "",
        });
      } else {
        console.log('router.push("/")',router.push("/"));
        

        router.push("/");
      }
      // 登录成功提示
      // setTimeout(() => {
      //   // 关闭 loading
      //   state.loading.signIn = true;
      //   const signInText = t("message.signInText");
      //   ElMessage.success(`${currentTimeInfo}，${signInText}`);
      //   // 修复防止退出登录再进入界面时，需要刷新样式才生效的问题，初始化布局样式等(登录的时候触发，目前方案)
      //   proxy.mittBus.emit("onSignInClick");
      // }, 300);
      state.loading.signIn = true;
			const signInText = t('message.signInText');
			ElMessage.success(`${currentTimeInfo}，${signInText}`);
			// 添加 loading，防止第一次进入界面时出现短暂空白
			NextLoading.start();
    };
    return {
      currentTime,
      onSignIn,
      ...toRefs(state),
    };
  },
});
</script>

<style scoped lang="scss">
.login-content-form {
  margin-top: 20px;
  .login-content-password {
    display: inline-block;
    width: 25px;
    cursor: pointer;
    &:hover {
      color: #909399;
    }
  }
  .login-content-code {
    display: flex;
    align-items: center;
    justify-content: space-around;
    .login-content-code-img {
      width: 100%;
      height: 40px;
      line-height: 40px;
      background-color: #ffffff;
      border: 1px solid rgb(220, 223, 230);
      color: #333;
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 5px;
      text-indent: 5px;
      text-align: center;
      cursor: pointer;
      transition: all ease 0.2s;
      border-radius: 4px;
      user-select: none;
      &:hover {
        border-color: #c0c4cc;
        transition: all ease 0.2s;
      }
    }
  }
  .login-content-submit {
    width: 100%;
    letter-spacing: 2px;
    font-weight: 300;
    margin-top: 15px;
  }
}
</style>
