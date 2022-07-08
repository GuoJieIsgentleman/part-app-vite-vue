<template>
  <ElConfigProvider :locale="locale">
    <router-view v-show="getThemeConfig.lockScreenTime !== 0" />
    <el-dialog
      title="提示"
      v-model="state.VersionFlag"
      width="30%"
      :before-close="handleClose"
    >
      <span>有新版本 当前版本{{ state.version }}点击确认更新</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="state.VersionFlag = false">取 消</el-button>
          <el-button type="primary" @click="download">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    <LockScreen v-if="getThemeConfig.isLockScreen" />
    <Setings ref="setingsRef" v-show="getThemeConfig.lockScreenTime !== 0" />

    <CloseFull />
  </ElConfigProvider>
</template>

<script lang="ts">
import {
  computed,
  ref,
  getCurrentInstance,
  onBeforeMount,
  onMounted,
  onUnmounted,
  nextTick,
  defineComponent,
  watch,
  reactive,
  toRefs,
} from "vue";
import { useRoute } from "vue-router";
import { useStore } from "./store/index.ts";
import { useTitle } from "./utils/setWebTitle";
import { Local } from "./utils/storage.ts";
import setIntroduction from "./utils/setIconfont";
import LockScreen from "./layout/lockScreen/index.vue";
import Setings from "./layout/navBars/breadcrumb/setings.vue";
import CloseFull from "./layout/navBars/breadcrumb/closeFull.vue";

import { ElMessage, ElMessageBox, ElConfigProvider } from "element-plus";
import zhcn from "element-plus/lib/locale/lang/zh-cn";
import service from "./utils/request";
export default defineComponent({
  name: "app",
  components: { LockScreen, Setings, CloseFull },
  setup() {
    const state: any = reactive({
      VersionFlag: false,
      VersionExplain: "",
      Website: "",
      myVersion: "",
      version: "",
    });
    const locale = zhcn;
    const dialogVisible = ref(false);
    const handleClose = (done: any) => {
      ElMessageBox.confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {
          // catch
        });
    };

    const plusReady = async () => {
      plus.runtime.getProperty(plus.runtime.appid, function (inf: any) {
        //wgtVer=inf.version;

        state.version = inf.version;
        console.log("vue  state.version");
        console.log(state.version);
      });

      let { data: res } = await service.get("/getVersion");
      console.log(res);
      state.VersionExplain = res.app_info;
      console.log("当前版本");
      console.log(state.version);
      console.log(state.VersionExplain);
      state.Website = res.app_download;
      console.log("当前下载路径");
      console.log(state.Website);

      if (state.VersionExplain != state.version) {
        console.log("需要更新吗");
        state.VersionFlag = true;
      }
    };

    const update1 = () => {
      if (window.plus) {
        plusReady();
      } else {
        document.addEventListener("plusready", plusReady, false);
      }
    };
    const download = () => {
      let wgtVer = state.version;

      // , {
      //   params: {
      //     appid: plus.runtime.appid,
      //     appname: "beijian",
      //   },
      // }
      plus.nativeUI.showWaiting("下载更新文件...");
      plus.downloader
        .createDownload(
          state.Website,
          { filename: "_doc/update/" },
          function (d: any, status: any) {
            if (status == 200) {
              console.log("下载更新文件成功：" + d.filename);
              plus.nativeUI.showWaiting("安装更新文件...");
              plus.runtime.install(
                d.filename,
                {},
                function () {
                  plus.nativeUI.closeWaiting();
                  plus.nativeUI.alert("应用资源更新完成！", function () {
                    plus.runtime.restart();
                  });
                },
                function (e) {
                  plus.nativeUI.closeWaiting();
                  plus.nativeUI.alert("安装更新文件失败[" + e.code + "]：" + e.message);
                  if (e.code == 10) {
                    plus.nativeUI.alert("请清除临时目录");
                  }
                }
              );
            } else {
              plus.nativeUI.alert("下载失败！");
            }
            plus.nativeUI.closeWaiting();
          }
        )
        .start();
    };
    onBeforeMount(update1);
    const { proxy } = getCurrentInstance() as any;
    const setingsRef = ref();
    const route = useRoute();
    const store = useStore();
    const title = useTitle();
    // 获取布局配置信息
    const getThemeConfig = computed(() => {
      return store.state.themeConfig.themeConfig;
    });
    // 布局配置弹窗打开
    const openSetingsDrawer = () => {
      setingsRef.value.openDrawer();
    };
    // 设置初始化，防止刷新时恢复默认
    onBeforeMount(() => {
      // 设置批量第三方 icon 图标
      setIntroduction.cssCdn();
      // 设置批量第三方 js
      setIntroduction.jsCdn();
    });
    // 页面加载时
    onMounted(() => {
      nextTick(() => {
        // 监听布局配置弹窗点击打开
        proxy.mittBus.on("openSetingsDrawer", () => {
          openSetingsDrawer();
        });
        // 获取缓存中的布局配置
        if (Local.get("themeConfig")) {
          store.dispatch("themeConfig/setThemeConfig", Local.get("themeConfig"));
          document.documentElement.style.cssText = Local.get("themeConfigStyle");
        }
      });
    });

    // 页面销毁时，关闭监听布局配置
    onUnmounted(() => {
      proxy.mittBus.off("openSetingsDrawer", () => {});
    });
    // 监听路由的变化，设置网站标题
    watch(
      () => route.path,
      () => {
        title();
      }
    );
    return {
      setingsRef,
      getThemeConfig,
      handleClose,
      state,
      dialogVisible,
      update1,
      download,
      locale,
    };
  },
});
</script>
