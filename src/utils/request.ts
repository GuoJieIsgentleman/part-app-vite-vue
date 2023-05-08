import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import router, { resetRoute } from '../router';
import { formatDate111, subtimeminutes } from './formatTime';


import { Session } from './storage';

// 配置新建一个 axios 实例

const service = axios.create({

  //baseURL: 'http://116.132.45.150:6900',//邯郸

  baseURL: 'https://www.ssxyf.cn:5556', //陕西友发
  //baseURL: 'http://192.168.3.17:9999', //ceshi
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});


// 添加请求拦截器
service.interceptors.request.use(
  (config) => {
    if (Session.get('token')) {
      config.headers.common['Authorization'] = `${Session.get('token')}`;
    }
    console.log("登陆时间", Session.get('timestamp'))
    console.log("现在时间", formatDate111(new Date()))
    console.log("时间差", subtimeminutes(Session.get('timestamp')))

    if (subtimeminutes(Session.get('timestamp')) > 30) {
      ElMessage.success("超过30分钟未操作 请重新登录")
      Session.clear(); // 清除缓存/token等
      resetRoute(); // 删除/重置路由


      //   window.location.href="http://192.168.56.1:10000/#/login";
      router.push("/login");
    }
    return config;
  },
  (error) => {
    // 对请求错误做些什么
    console.log('请求错误');
    return Promise.reject(error);
  }
);

// 添加响应拦截器
service.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么

    const res = response.data;



    return response;



  },
  (error) => {
    // 对响应错误做点什么

    console.log('error')
    console.log(error)
    if (error.message.indexOf('timeout') != -1) {
      ElMessage.error('网络超时');
    } else if (error.message == 'Network Error') {


      ElMessage.error('网络连接错误');


    } else {
      if (error.response.data) ElMessage.error(error.response.statusText);
      else ElMessage.error('接口路径找不到');
    }
    return Promise.reject(error);
  }
);

// 导出 axios 实例
export default service;
