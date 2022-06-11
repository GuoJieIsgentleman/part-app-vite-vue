"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
exports.resetRoute = exports.setAddRoute = exports.setFilterRouteEnd = exports.setFilterRoute = exports.setFilterMenuAndCacheTagsViewRoutes = exports.setFilterHasAuthMenu = exports.hasAuth = exports.setCacheTagsViewRoutes = exports.formatTwoStageRoutes = exports.formatFlatteningRoutes = void 0;
var vue_router_1 = require("vue-router");
var nprogress_1 = require("nprogress");
require("nprogress/nprogress.css");
var index_ts_1 = require("/@/store/index.ts");
var storage_1 = require("/@/utils/storage");
var loading_1 = require("/@/utils/loading");
var route_1 = require("/@/router/route");
var backEnd_1 = require("/@/router/backEnd");
/**
 * 创建一个可以被 Vue 应用程序使用的路由实例
 * @method createRouter(options: RouterOptions): Router
 * @link 参考：https://next.router.vuejs.org/zh/api/#createrouter
 */
var router = vue_router_1.createRouter({
    history: vue_router_1.createWebHashHistory(),
    routes: route_1.staticRoutes
});
/**
 * 定义404界面
 * @link 参考：https://next.router.vuejs.org/zh/guide/essentials/history-mode.html#netlify
 */
var pathMatch = {
    path: '/:path(.*)*',
    redirect: '/404'
};
/**
 * 路由多级嵌套数组处理成一维数组
 * @param arr 传入路由菜单数据数组
 * @returns 返回处理后的一维路由菜单数组
 */
function formatFlatteningRoutes(arr) {
    if (arr.length <= 0)
        return false;
    for (var i = 0; i < arr.length; i++) {
        if (arr[i].children) {
            arr = arr.slice(0, i + 1).concat(arr[i].children, arr.slice(i + 1));
        }
    }
    return arr;
}
exports.formatFlatteningRoutes = formatFlatteningRoutes;
/**
 * 一维数组处理成多级嵌套数组（只保留二级：也就是二级以上全部处理成只有二级，keep-alive 支持二级缓存）
 * @description isKeepAlive 处理 `name` 值，进行缓存。顶级关闭，全部不缓存
 * @link 参考：https://v3.cn.vuejs.org/api/built-in-components.html#keep-alive
 * @param arr 处理后的一维路由菜单数组
 * @returns 返回将一维数组重新处理成 `定义动态路由（dynamicRoutes）` 的格式
 */
function formatTwoStageRoutes(arr) {
    if (arr.length <= 0)
        return false;
    var newArr = [];
    var cacheList = [];
    arr.forEach(function (v) {
        if (v.path === '/') {
            newArr.push({ component: v.component, name: v.name, path: v.path, redirect: v.redirect, meta: v.meta, children: [] });
        }
        else {
            // 判断是否是动态路由（xx/:id/:name），用于 tagsView 等中使用
            // 修复：https://gitee.com/lyt-top/vue-next-admin/issues/I3YX6G
            if (v.path.indexOf('/:') > -1) {
                v.meta['isDynamic'] = true;
                v.meta['isDynamicPath'] = v.path;
            }
            newArr[0].children.push(__assign({}, v));
            // 存 name 值，keep-alive 中 include 使用，实现路由的缓存
            // 路径：/@/layout/routerView/parent.vue
            if (newArr[0].meta.isKeepAlive && v.meta.isKeepAlive) {
                cacheList.push(v.name);
                index_ts_1.store.dispatch('keepAliveNames/setCacheKeepAlive', cacheList);
            }
        }
    });
    return newArr;
}
exports.formatTwoStageRoutes = formatTwoStageRoutes;
/**
 * 缓存多级嵌套数组处理后的一维数组
 * @description 用于 tagsView、菜单搜索中：未过滤隐藏的(isHide)
 */
// export function setCacheTagsViewRoutes() {
//   // 获取有权限的路由，否则 tagsView、菜单搜索中无权限的路由也将显示
//   let authsRoutes = dynamicRoutes[0].children;
//   // 添加到 vuex setTagsViewRoutes 中
//   store.dispatch('tagsViewRoutes/setTagsViewRoutes', dynamicRoutes[0].children);
// }
function setCacheTagsViewRoutes() {
    // 获取有权限的路由，否则 tagsView、菜单搜索中无权限的路由也将显示
    var authsRoutes = setFilterHasAuthMenu(route_1.dynamicRoutes, index_ts_1.store.state.userInfos.userInfos.authPageList);
    // 添加到 vuex setTagsViewRoutes 中
    index_ts_1.store.dispatch('tagsViewRoutes/setTagsViewRoutes', formatTwoStageRoutes(formatFlatteningRoutes(authsRoutes))[0].children);
}
exports.setCacheTagsViewRoutes = setCacheTagsViewRoutes;
/**
 * 判断路由 `meta.auth` 中是否包含当前登录用户权限字段
 * @param auths 用户权限标识，在 userInfos（用户信息）的 authPageList（登录页登录时缓存到浏览器）数组
 * @param route 当前循环时的路由项
 * @returns 返回对比后有权限的路由项
 */
function hasAuth(auths, route) {
    if (route.meta && route.meta.auth)
        return auths.some(function (auth) { return route.meta.auth.includes(auth); });
    else
        return true;
}
exports.hasAuth = hasAuth;
/**
 * 获取当前用户权限标识去比对路由表，设置递归过滤有权限的路由
 * @param routes 当前路由 children
 * @param auth 用户权限标识，在 userInfos（用户信息）的 authPageList（登录页登录时缓存到浏览器）数组
 * @returns 返回有权限的路由数组 `meta.auth` 中控制
 */
function setFilterHasAuthMenu(routes, auth) {
    var menu = [];
    routes.forEach(function (route) {
        var item = __assign({}, route);
        if (hasAuth(auth, item)) {
            if (item.children)
                item.children = setFilterHasAuthMenu(item.children, auth);
            menu.push(item);
        }
    });
    return menu;
}
exports.setFilterHasAuthMenu = setFilterHasAuthMenu;
/**
 * 设置递归过滤有权限的路由到 vuex routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
 * @description 用于左侧菜单、横向菜单的显示
 * @description 用于 tagsView、菜单搜索中：未过滤隐藏的(isHide)
 */
function setFilterMenuAndCacheTagsViewRoutes() {
    index_ts_1.store.dispatch('routesList/setRoutesList', setFilterHasAuthMenu(route_1.dynamicRoutes[0].children, index_ts_1.store.state.userInfos.userInfos.authPageList));
    setCacheTagsViewRoutes();
}
exports.setFilterMenuAndCacheTagsViewRoutes = setFilterMenuAndCacheTagsViewRoutes;
// export function setFilterMenuAndCacheTagsViewRoutes() {
//   console.log('dynamicRoutes[0].children')
//   console.log(dynamicRoutes[0].children)
//   store.dispatch('routesList/setRoutesList', dynamicRoutes[0].children);
//   setCacheTagsViewRoutes();
// }
/**
 * 获取当前用户权限标识去比对路由表（未处理成多级嵌套路由）
 * @description 这里主要用于动态路由的添加，router.addRoute
 * @link 参考：https://next.router.vuejs.org/zh/api/#addroute
 * @param chil dynamicRoutes（/@/router/route）第一个顶级 children 的下路由集合
 * @returns 返回有当前用户权限标识的路由数组
 */
function setFilterRoute(chil) {
    var filterRoute = [];
    chil.forEach(function (route) {
        if (route.meta.auth) {
            route.meta.auth.forEach(function (metaAuth) {
                index_ts_1.store.state.userInfos.userInfos.authPageList.forEach(function (auth) {
                    if (metaAuth === auth)
                        filterRoute.push(__assign({}, route));
                });
            });
        }
    });
    return filterRoute;
}
exports.setFilterRoute = setFilterRoute;
/**
 * 获取有当前用户权限标识的路由数组，进行对原路由的替换
 * @description 替换 dynamicRoutes（/@/router/route）第一个顶级 children 的路由
 * @returns 返回替换后的路由数组
 */
function setFilterRouteEnd() {
    var filterRouteEnd = formatTwoStageRoutes(formatFlatteningRoutes(route_1.dynamicRoutes));
    filterRouteEnd[0].children = __spreadArrays(setFilterRoute(filterRouteEnd[0].children), [__assign({}, pathMatch)]);
    return filterRouteEnd;
}
exports.setFilterRouteEnd = setFilterRouteEnd;
/**
 * 添加动态路由
 * @method router.addRoute
 * @description 此处循环为 dynamicRoutes（/@/router/route）第一个顶级 children 的路由一维数组，非多级嵌套
 * @link 参考：https://next.router.vuejs.org/zh/api/#addroute
 */
function setAddRoute() {
    setFilterRouteEnd().forEach(function (route) {
        var routeName = route.name;
        if (!router.hasRoute(routeName))
            router.addRoute(route);
    });
}
exports.setAddRoute = setAddRoute;
/**
 * 删除/重置路由
 * @method router.removeRoute
 * @description 此处循环为 dynamicRoutes（/@/router/route）第一个顶级 children 的路由一维数组，非多级嵌套
 * @link 参考：https://next.router.vuejs.org/zh/api/#push
 */
function resetRoute() {
    setFilterRouteEnd().forEach(function (route) {
        console.log('route');
        console.log(route, "color:" + 'red');
        var routeName = route.name;
        router.hasRoute(routeName) && router.removeRoute(routeName);
    });
}
exports.resetRoute = resetRoute;
// isRequestRoutes 为 true，则开启后端控制路由，路径：`/src/store/modules/themeConfig.ts`
var isRequestRoutes = index_ts_1.store.state.themeConfig.themeConfig.isRequestRoutes;
// 前端控制路由：初始化方法，防止刷新时路由丢失
// isRequestRoutes=true
// if (!isRequestRoutes) initFrontEndControlRoutes();
// 路由加载前
router.beforeEach(function (to, from, next) { return __awaiter(void 0, void 0, void 0, function () {
    var token;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                nprogress_1["default"].configure({ showSpinner: false });
                if (to.meta.title)
                    nprogress_1["default"].start();
                token = storage_1.Session.get('token');
                if (!(to.path === '/login' && !token)) return [3 /*break*/, 1];
                next();
                nprogress_1["default"].done();
                return [3 /*break*/, 7];
            case 1:
                if (!!token) return [3 /*break*/, 2];
                next("/login?redirect=" + to.path + "&params=" + JSON.stringify(to.query ? to.query : to.params));
                storage_1.Session.clear();
                resetRoute();
                nprogress_1["default"].done();
                return [3 /*break*/, 7];
            case 2:
                if (!(token && to.path === '/login')) return [3 /*break*/, 3];
                next('/home');
                nprogress_1["default"].done();
                return [3 /*break*/, 7];
            case 3:
                if (!(index_ts_1.store.state.routesList.routesList.length === 0)) return [3 /*break*/, 6];
                if (!isRequestRoutes) return [3 /*break*/, 5];
                // 后端控制路由：路由数据初始化，防止刷新时丢失
                return [4 /*yield*/, backEnd_1.initBackEndControlRoutes()];
            case 4:
                // 后端控制路由：路由数据初始化，防止刷新时丢失
                _a.sent();
                // 动态添加路由：防止非首页刷新时跳转回首页的问题
                // 确保 addRoute() 时动态添加的路由已经被完全加载上去
                next(__assign(__assign({}, to), { replace: true }));
                _a.label = 5;
            case 5: return [3 /*break*/, 7];
            case 6:
                next();
                _a.label = 7;
            case 7: return [2 /*return*/];
        }
    });
}); });
// 路由加载后
router.afterEach(function () {
    nprogress_1["default"].done();
    loading_1.NextLoading.done();
});
// 导出路由
exports["default"] = router;
