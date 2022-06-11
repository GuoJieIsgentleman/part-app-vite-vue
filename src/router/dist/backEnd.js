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
exports.__esModule = true;
exports.dynamicImport = exports.backEndComponent = exports.setBackEndControlRefreshRoutes = exports.getBackEndControlRoutes = exports.initBackEndControlRoutes = void 0;
var index_ts_1 = require("/@/store/index.ts");
var storage_1 = require("/@/utils/storage");
var loading_1 = require("/@/utils/loading");
var index_1 = require("/@/router/index");
var route_1 = require("/@/router/route");
var index_2 = require("/@/api/menu/index");
var layouModules = import.meta.glob('../layout/routerView/*.{vue,tsx}');
var viewsModules = import.meta.glob('../views/**/*.{vue,tsx}');
/**
 * 获取目录下的 .vue、.tsx 全部文件
 * @method import.meta.glob
 * @link 参考：https://cn.vitejs.dev/guide/features.html#json
 */
var dynamicViewsModules = Object.assign({}, __assign({}, layouModules), __assign({}, viewsModules));
/**
 * 后端控制路由：初始化方法，防止刷新时路由丢失
 * @method  NextLoading 界面 loading 动画开始执行
 * @method store.dispatch('userInfos/setUserInfos') 触发初始化用户信息
 * @method store.dispatch('requestOldRoutes/setBackEndControlRoutes') 存储接口原始路由（未处理component），根据需求选择使用
 * @method setAddRoute 添加动态路由
 * @method setFilterMenuAndCacheTagsViewRoutes 设置递归过滤有权限的路由到 vuex routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
 */
function initBackEndControlRoutes() {
    return __awaiter(this, void 0, void 0, function () {
        var res, _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    // 界面 loading 动画开始执行
                    if (window.nextLoading === undefined)
                        loading_1.NextLoading.start();
                    // 无 token 停止执行下一步
                    if (!storage_1.Session.get('token'))
                        return [2 /*return*/, false];
                    // 触发初始化用户信息
                    index_ts_1.store.dispatch('userInfos/setUserInfos');
                    return [4 /*yield*/, getBackEndControlRoutes()];
                case 1:
                    res = _b.sent();
                    // 存储接口原始路由（未处理component），根据需求选择使用
                    // store.dispatch('requestOldRoutes/setBackEndControlRoutes', JSON.parse(JSON.stringify(res.data)));
                    index_ts_1.store.dispatch('requestOldRoutes/setBackEndControlRoutes', res.data.data);
                    // 处理路由（component），替换 dynamicRoutes（/@/router/route）第一个顶级 children 的路由
                    _a = route_1.dynamicRoutes[0];
                    return [4 /*yield*/, backEndComponent(res.data.data)];
                case 2:
                    // 处理路由（component），替换 dynamicRoutes（/@/router/route）第一个顶级 children 的路由
                    _a.children = _b.sent();
                    // 添加动态路由
                    return [4 /*yield*/, index_1.setAddRoute()];
                case 3:
                    // 添加动态路由
                    _b.sent();
                    // 设置递归过滤有权限的路由到 vuex routesList 中（已处理成多级嵌套路由）及缓存多级嵌套数组处理后的一维数组
                    index_1.setFilterMenuAndCacheTagsViewRoutes();
                    return [2 /*return*/];
            }
        });
    });
}
exports.initBackEndControlRoutes = initBackEndControlRoutes;
/**
 * 请求后端路由菜单接口
 * @description isRequestRoutes 为 true，则开启后端控制路由
 * @returns 返回后端路由菜单数据
 */
function getBackEndControlRoutes() {
    // 模拟 admin 与 test
    var auth = index_ts_1.store.state.userInfos.userInfos.authPageList[0];
    console.log('获取后端路由传递的参数 权限');
    console.log(auth);
    // 管理员 admin
    if (auth === 'admin')
        return index_2.getMenuAdmin({ auth: auth });
    // 其它用户 test
    else
        return index_2.getMenuOther({ auth: auth });
}
exports.getBackEndControlRoutes = getBackEndControlRoutes;
/**
 * 重新请求后端路由菜单接口
 * @description 用于菜单管理界面刷新菜单（未进行测试）
 * @description 路径：/src/views/system/menu/component/addMenu.vue
 */
function setBackEndControlRefreshRoutes() {
    getBackEndControlRoutes();
}
exports.setBackEndControlRefreshRoutes = setBackEndControlRefreshRoutes;
/**
 * 后端路由 component 转换
 * @param routes 后端返回的路由表数组
 * @returns 返回处理成函数后的 component
 */
function backEndComponent(routes) {
    var routes1 = routes;
    if (!routes1)
        return;
    var returndata = routes1.map(function (item) {
        if (item.component) {
            item.component = dynamicImport(dynamicViewsModules, item.component);
            // if (item.children.length > 0) {
            //   console.log('item.children')
            //   console.log(item.children)
            //   backEndComponent(item.children);
            // }
        }
        //递归组成item 路由的 children
        //递归组成item 路由的 children
        //递归组成item 路由的 children
        //递归组成item 路由的 children
        //递归组成item 路由的 children
        item.children && backEndComponent(item.children);
        return item;
    });
    return returndata;
}
exports.backEndComponent = backEndComponent;
/**
 * 后端路由 component 转换函数
 * @param dynamicViewsModules 获取目录下的 .vue、.tsx 全部文件
 * @param component 当前要处理项 component
 * @returns 返回处理成函数后的 component
 */
function dynamicImport(dynamicViewsModules, component) {
    var keys = Object.keys(dynamicViewsModules);
    var matchKeys = keys.filter(function (key) {
        var k = key.replace(/..\/views|../, '');
        return k.startsWith("" + component) || k.startsWith("/" + component);
    });
    if ((matchKeys === null || matchKeys === void 0 ? void 0 : matchKeys.length) === 1) {
        var matchKey = matchKeys[0];
        return dynamicViewsModules[matchKey];
    }
    if ((matchKeys === null || matchKeys === void 0 ? void 0 : matchKeys.length) > 1) {
        return false;
    }
}
exports.dynamicImport = dynamicImport;
