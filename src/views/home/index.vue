<template>
  <div class="home-container">
    <el-row :gutter="15">
      <el-col :sm="6" class="mb15">
        <div class="home-card-item home-card-first">
          <div class="flex-margin flex">
            <img :src="getUserInfos.photo" />
            <div class="home-card-first-right ml15">
              <div class="flex-margin">
                <div class="home-card-first-right-title">
                  {{ currentTime }}，{{
                    getUserInfos.userName === "" ? "test" : getUserInfos.userName
                  }}！
                </div>
                <div class="home-card-first-right-msg mt5">
                  {{ getUserInfos.userName === "admin" ? "管理员" : "普通用户" }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
      <!-- <el-col :sm="6" class="mb15">
        <div class="home-card-item home-card-first">
          <div class="flex-margin flex">
            <div ref="partchart"></div>
          </div>
        </div>
      </el-col> -->
      <el-col :sm="6" class="mb15" v-for="(v, k) in state.topCardItemList" :key="k">
        <div class="home-card-item home-card-item-box" :style="{ background: v.color }">
          <div class="home-card-item-flex">
            <div class="home-card-item-title pb3">{{ v.title }}</div>
        
            <div class="home-card-item-title-num pb6">
              {{ v.titleNum }}
            </div>
            <div class="home-card-item-tip pb3">{{ v.tip }}</div>
     
          </div>
          <i :class="v.icon" :style="{ color: v.iconColor }"></i>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import {
  ref,
  toRefs,
  reactive,
  onMounted,
  nextTick,
  computed,
  getCurrentInstance,
  watch,
} from "vue";
import * as echarts from "echarts";
import { CountUp } from "countup.js";
import { formatAxis } from "/@/utils/formatTime";
import { useStore } from "/@/store/index";
import service from "/@/utils/request";
// import { topCardItemList, environmentList, activitiesList } from "./mock";

    const partcount: any = ref(0);
    const userecordcount: any = ref(0);
    const maintenancecount: any = ref(0);
    const repaircount: any = ref(0);
    const scrapcount: any = ref(0);
    const version: any = ref(0);

    const { proxy } = getCurrentInstance() as any;
    const store = useStore();
    const state = reactive({
      myCharts: [],
      topCardItemList: [
        {
          title: "版本号",
          titleNum: version,
          tip: "在场人数",
          tipNum: "911",
          color: "#995911",
          iconColor: "#F86C6B",
          icon: "iconfont icon-jinridaiban",
        },
        {
          title: "总库存",
          titleNum: partcount,
          tip: "在场人数",
          tipNum: "911",
          color: "#F95959",
          iconColor: "#F86C6B",
          icon: "iconfont icon-jinridaiban",
        },
        {
          title: "领用记录",
          titleNum: userecordcount,
          tip: "在场人数",
          tipNum: "911",
          color: "#F95959",
          iconColor: "#F86C6B",
          icon: "iconfont icon-jinridaiban",
        },
        {
          title: "保养记录",
          titleNum: maintenancecount,
          tip: "使用中",
          tipNum: "611",
          color: "#8595F4",
          iconColor: "#92A1F4",
          icon: "iconfont icon-AIshiyanshi",
        },
        {
          title: "外修记录",
          titleNum: repaircount,
          tip: "通过人数",
          tipNum: "911",
          color: "#FEBB50",
          iconColor: "#FDC566",
          icon: "iconfont icon-shenqingkaiban",
        },
        {
          title: "报废记录",
          titleNum: scrapcount,
          tip: "通过人数",
          tipNum: "911",
          color: "#FEBB50",
          iconColor: "#FDC566",
          icon: "iconfont icon-shenqingkaiban",
        },
      ],
    });

    //获取版本号
    const getversion = () => {};

    // 获取用户信息 vuex
    const getUserInfos: any = computed(() => {
      return store.state.userInfos.userInfos;
    });
    // 当前时间提示语
    const currentTime = computed(() => {
      return formatAxis(new Date());
    });
    // 初始化数字滚动
    const initNumCountUp = () => {
      nextTick(() => {
        new CountUp("titleNum1", Math.random() * 10000).start();
        new CountUp("titleNum2", Math.random() * 10000).start();
        new CountUp("titleNum3", Math.random() * 10000).start();
        new CountUp("tipNum1", Math.random() * 1000).start();
        new CountUp("tipNum2", Math.random() * 1000).start();
        new CountUp("tipNum3", Math.random() * 1000).start();
      });
    };
    onMounted(async () => {
      initNumCountUp();
      
      let { data: userecordcount1 } = await service.get("/getuserecordcount");
      userecordcount.value = userecordcount1[0][0];
      let { data: partcount1 } = await service.get("/getpartcount");
      partcount.value = partcount1[0][0];
      let { data: maintenancecount1 } = await service.get("/getmaintenancecount");
      maintenancecount.value = maintenancecount1[0][0];
      let { data: scrapcount1 } = await service.get("/getscrapcount");
      scrapcount.value = scrapcount1[0][0];
      let { data: repaircount1 } = await service.get("/getrepaircount");
      repaircount.value = repaircount1[0][0];

      plus.runtime.getProperty(plus.runtime.appid, function (inf: any) {
        //wgtVer=inf.version;

        version.value = inf.version;
      });
      // initHomeLaboratory();
      // initHomeOvertime();
      // initEchartsResize();
    });
    // 监听 vuex 中的 tagsview 开启全屏变化，重新 resize 图表，防止不出现/大小不变等
    // watch(
    //   () => store.state.tagsViewRoutes.isTagsViewCurrenFull,
    //   () => {
    //     nextTick(() => {
    //       for (let i = 0; i < state.myCharts.length; i++) {
    //         state.myCharts[i].resize();
    //       }
    //     });
    //   }
    // );
  
</script>

<style scoped lang="scss">
.home-container {
  overflow-x: hidden;
  .home-card-item {
    width: 100%;
    height: 103px;
    background: gray;
    border-radius: 4px;
    transition: all ease 0.3s;
    &:hover {
      box-shadow: 0 2px 12px 0 rgb(0 0 0 / 10%);
      transition: all ease 0.3s;
    }
  }
  .home-card-item-box {
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    &:hover {
      i {
        right: 0px !important;
        bottom: 0px !important;
        transition: all ease 0.3s;
      }
    }
    i {
      position: absolute;
      right: -10px;
      bottom: -10px;
      font-size: 70px;
      transform: rotate(-30deg);
      transition: all ease 0.3s;
    }
    .home-card-item-flex {
      padding: 0 20px;
      color: white;
      .home-card-item-title,
      .home-card-item-tip {
        font-size: 13px;
      }
      .home-card-item-title-num {
        font-size: 18px;
      }
      .home-card-item-tip-num {
        font-size: 13px;
      }
    }
  }
  .home-card-first {
    background: white;
    border: 1px solid #ebeef5;
    display: flex;
    align-items: center;
    img {
      width: 60px;
      height: 60px;
      border-radius: 100%;
      border: 2px solid var(--color-primary-light-5);
    }
    .home-card-first-right {
      flex: 1;
      display: flex;
      flex-direction: column;
      .home-card-first-right-msg {
        font-size: 13px;
        color: gray;
      }
    }
  }
  .home-monitor {
    height: 200px;
    .flex-warp-item {
      width: 50%;
      height: 100px;
      display: flex;
      .flex-warp-item-box {
        margin: auto;
        height: auto;
        text-align: center;
      }
    }
  }
  .home-warning-card {
    height: 292px;
    ::v-deep(.el-card) {
      height: 100%;
    }
  }
  .home-dynamic {
    height: 200px;
    .home-dynamic-item {
      display: flex;
      width: 100%;
      height: 60px;
      overflow: hidden;
      &:first-of-type {
        .home-dynamic-item-line {
          i {
            color: orange !important;
          }
        }
      }
      .home-dynamic-item-left {
        text-align: right;
        .home-dynamic-item-left-time1 {
        }
        .home-dynamic-item-left-time2 {
          font-size: 13px;
          color: gray;
        }
      }
      .home-dynamic-item-line {
        height: 60px;
        border-right: 2px dashed #dfdfdf;
        margin: 0 20px;
        position: relative;
        i {
          color: var(--color-primary);
          font-size: 12px;
          position: absolute;
          top: 1px;
          left: -6px;
          transform: rotate(46deg);
          background: white;
        }
      }
      .home-dynamic-item-right {
        flex: 1;
        .home-dynamic-item-right-title {
          i {
            margin-right: 5px;
            border: 1px solid #dfdfdf;
            width: 20px;
            height: 20px;
            border-radius: 100%;
            padding: 3px 2px 2px;
            text-align: center;
            color: var(--color-primary);
          }
        }
        .home-dynamic-item-right-label {
          font-size: 13px;
          color: gray;
        }
      }
    }
  }
}
</style>
