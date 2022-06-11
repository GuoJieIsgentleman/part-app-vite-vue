"use strict";
exports.__esModule = true;
var axios_1 = require("axios");
var element_plus_1 = require("element-plus");
var storage_1 = require("/@/utils/storage");
// 配置新建一个 axios 实例
var service = axios_1["default"].create({
    baseURL: 'http://61.185.74.251:5556',
    timeout: 50000,
    headers: { 'Content-Type': 'application/json' }
});
// 添加请求拦截器
service.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么 token
    // console.log('config')
    // console.log(config.baseURL)
    // ElMessage({
    //   showClose: true,
    //   message: `${config.baseURL}${config.url}`,
    //   type: "success",
    // });
    if (storage_1.Session.get('token')) {
        config.headers.common['Authorization'] = "" + storage_1.Session.get('token');
    }
    return config;
}, function (error) {
    // 对请求错误做些什么
    console.log('请求错误');
    return Promise.reject(error);
});
// 添加响应拦截器
service.interceptors.response.use(function (response) {
    // 对响应数据做点什么
    var res = response.data;
    if (res.code && res.code !== 0) {
        // `token` 过期或者账号已在别处登录
        if (res.code === 401 || res.code === 4001) {
            storage_1.Session.clear(); // 清除浏览器全部临时缓存
            window.location.href = '/'; // 去登录页
            element_plus_1.ElMessageBox.alert('你已被登出，请重新登录', '提示', {})
                .then(function () { })["catch"](function () { });
        }
        return Promise.reject(service.interceptors.response);
    }
    else {
        return response;
    }
}, function (error) {
    // 对响应错误做点什么
    console.log('error');
    console.log(error);
    if (error.message.indexOf('timeout') != -1) {
        element_plus_1.ElMessage.error('网络超时');
    }
    else if (error.message == 'Network Error') {
        element_plus_1.ElMessage.error('网络连接错误');
    }
    else {
        if (error.response.data)
            element_plus_1.ElMessage.error(error.response.statusText);
        else
            element_plus_1.ElMessage.error('接口路径找不到');
    }
    return Promise.reject(error);
});
// 导出 axios 实例
exports["default"] = service;
