"use strict";
exports.__esModule = true;
exports.getMenuOther = exports.getMenuAdmin = void 0;
var request_1 = require("/@/utils/request");
/**
 * 后端控制菜单模拟json，路径在 https://gitee.com/lyt-top/vue-next-admin-images/tree/master/menu
 * 后端控制路由，isRequestRoutes 为 true，则开启后端控制路由
 */
/**
 * 获取后端动态路由菜单(admin)
 * @link 参考：https://gitee.com/lyt-top/vue-next-admin-images/tree/master/menu
 * @param params 要传的参数值，非必传
 * @returns 返回接口数据
 */
function getMenuAdmin(params) {
    return request_1["default"]({
        url: '/getroutes',
        // url: '/api/getroutes',
        method: 'get',
        params: params
    });
}
exports.getMenuAdmin = getMenuAdmin;
/**
 * 获取后端动态路由菜单(test)
 * @link 参考：https://gitee.com/lyt-top/vue-next-admin-images/tree/master/menu
 * @param params 要传的参数值，非必传
 * @returns 返回接口数据
 */
function getMenuOther(params) {
    return request_1["default"]({
        url: '/getroutes',
        method: 'get',
        params: params
    });
}
exports.getMenuOther = getMenuOther;
