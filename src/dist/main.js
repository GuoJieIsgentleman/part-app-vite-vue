"use strict";
exports.__esModule = true;
var vue_1 = require("vue");
var App_vue_1 = require("./App.vue");
var router_1 = require("./router");
var store_1 = require("./store");
var directive_1 = require("/@/utils/directive");
var index_1 = require("/@/i18n/index");
var componentSize_1 = require("/@/utils/componentSize");
require("default-passive-events");
var element_plus_1 = require("element-plus");
require("element-plus/lib/theme-chalk/index.css");
require("/@/theme/index.scss");
var mitt_1 = require("mitt");
var vue_web_screen_shot_1 = require("vue-web-screen-shot");
var vue_grid_layout_1 = require("vue-grid-layout");
var app = vue_1.createApp(App_vue_1["default"]);
app
    .use(router_1["default"])
    .use(store_1.store, store_1.key)
    .use(element_plus_1["default"], { i18n: index_1.i18n.global.t, size: componentSize_1.globalComponentSize })
    .use(index_1.i18n)
    .use(vue_web_screen_shot_1["default"], { enableWebRtc: false })
    .use(vue_grid_layout_1["default"])
    .mount('#app');
app.config.globalProperties.mittBus = mitt_1["default"]();
directive_1.directive(app);
