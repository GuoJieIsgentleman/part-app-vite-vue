"use strict";
exports.__esModule = true;
exports.subtimeminutes1 = exports.subtimeminutes = exports.subtimehours = exports.formatDate111 = exports.formatAxis = exports.formatPast = exports.getWeek = exports.formatDate = void 0;
/**
 * 时间日期转换
 * @param date 当前时间，new Date() 格式
 * @param format 需要转换的时间格式字符串
 * @description format 字符串随意，如 `YYYY-mm、YYYY-mm-dd`
 * @description format 季度："YYYY-mm-dd HH:MM:SS QQQQ"
 * @description format 星期："YYYY-mm-dd HH:MM:SS WWW"
 * @description format 几周："YYYY-mm-dd HH:MM:SS ZZZ"
 * @description format 季度 + 星期 + 几周："YYYY-mm-dd HH:MM:SS WWW QQQQ ZZZ"
 * @returns 返回拼接后的时间字符串
 */
function formatDate(date, format) {
    var we = date.getDay(); // 星期
    var z = getWeek(date); // 周
    var qut = Math.floor((date.getMonth() + 3) / 3).toString(); // 季度
    var opt = {
        'Y+': date.getFullYear().toString(),
        'm+': (date.getMonth() + 1).toString(),
        'd+': date.getDate().toString(),
        'H+': date.getHours().toString(),
        'M+': date.getMinutes().toString(),
        'S+': date.getSeconds().toString(),
        'q+': qut
    };
    // 中文数字 (星期)
    var week = {
        '0': '日',
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六'
    };
    // 中文数字（季度）
    var quarter = {
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四'
    };
    if (/(W+)/.test(format))
        format = format.replace(RegExp.$1, RegExp.$1.length > 1 ? (RegExp.$1.length > 2 ? '星期' + week[we] : '周' + week[we]) : week[we]);
    if (/(Q+)/.test(format))
        format = format.replace(RegExp.$1, RegExp.$1.length == 4 ? '第' + quarter[qut] + '季度' : quarter[qut]);
    if (/(Z+)/.test(format))
        format = format.replace(RegExp.$1, RegExp.$1.length == 3 ? '第' + z + '周' : z + '');
    for (var k in opt) {
        var r = new RegExp('(' + k + ')').exec(format);
        // 若输入的长度不为1，则前面补零
        if (r)
            format = format.replace(r[1], RegExp.$1.length == 1 ? opt[k] : opt[k].padStart(RegExp.$1.length, '0'));
    }
    return format;
}
exports.formatDate = formatDate;
/**
 * 获取当前日期是第几周
 * @param dateTime 当前传入的日期值
 * @returns 返回第几周数字值
 */
function getWeek(dateTime) {
    var temptTime = new Date(dateTime.getTime());
    // 周几
    var weekday = temptTime.getDay() || 7;
    // 周1+5天=周六
    temptTime.setDate(temptTime.getDate() - weekday + 1 + 5);
    var firstDay = new Date(temptTime.getFullYear(), 0, 1);
    var dayOfWeek = firstDay.getDay();
    var spendDay = 1;
    if (dayOfWeek != 0)
        spendDay = 7 - dayOfWeek + 1;
    firstDay = new Date(temptTime.getFullYear(), 0, 1 + spendDay);
    var d = Math.ceil((temptTime.valueOf() - firstDay.valueOf()) / 86400000);
    var result = Math.ceil(d / 7);
    return result;
}
exports.getWeek = getWeek;
/**
 * 将时间转换为 `几秒前`、`几分钟前`、`几小时前`、`几天前`
 * @param param 当前时间，new Date() 格式或者字符串时间格式
 * @param format 需要转换的时间格式字符串
 * @description param 10秒：  10 * 1000
 * @description param 1分：   60 * 1000
 * @description param 1小时： 60 * 60 * 1000
 * @description param 24小时：60 * 60 * 24 * 1000
 * @description param 3天：   60 * 60* 24 * 1000 * 3
 * @returns 返回拼接后的时间字符串
 */
function formatPast(param, format) {
    if (format === void 0) { format = 'YYYY-mm-dd'; }
    // 传入格式处理、存储转换值
    var t, s;
    // 获取js 时间戳
    var time = new Date().getTime();
    // 是否是对象
    typeof param === 'string' || 'object' ? (t = new Date(param).getTime()) : (t = param);
    // 当前时间戳 - 传入时间戳
    time = Number.parseInt("" + (time - t));
    if (time < 10000) {
        // 10秒内
        return '刚刚';
    }
    else if (time < 60000 && time >= 10000) {
        // 超过10秒少于1分钟内
        s = Math.floor(time / 1000);
        return s + "\u79D2\u524D";
    }
    else if (time < 3600000 && time >= 60000) {
        // 超过1分钟少于1小时
        s = Math.floor(time / 60000);
        return s + "\u5206\u949F\u524D";
    }
    else if (time < 86400000 && time >= 3600000) {
        // 超过1小时少于24小时
        s = Math.floor(time / 3600000);
        return s + "\u5C0F\u65F6\u524D";
    }
    else if (time < 259200000 && time >= 86400000) {
        // 超过1天少于3天内
        s = Math.floor(time / 86400000);
        return s + "\u5929\u524D";
    }
    else {
        // 超过3天
        var date = typeof param === 'string' || 'object' ? new Date(param) : param;
        return formatDate(date, format);
    }
}
exports.formatPast = formatPast;
/**
 * 时间问候语
 * @param param 当前时间，new Date() 格式
 * @description param 调用 `formatAxis(new Date())` 输出 `上午好`
 * @returns 返回拼接后的时间字符串
 */
function formatAxis(param) {
    var hour = new Date(param).getHours();
    if (hour < 6)
        return '凌晨好';
    else if (hour < 9)
        return '早上好';
    else if (hour < 12)
        return '上午好';
    else if (hour < 14)
        return '中午好';
    else if (hour < 17)
        return '下午好';
    else if (hour < 19)
        return '傍晚好';
    else if (hour < 22)
        return '晚上好';
    else
        return '夜里好';
}
exports.formatAxis = formatAxis;
exports.formatDate111 = function (date) {
    if (date) {
        var d = new Date(date);
        var y = d.getFullYear(); // 年份
        var m = (d.getMonth() + 1).toString().padStart(2, '0'); // 月份
        var r = d.getDate().toString().padStart(2, '0'); // 日子
        var hh = d.getHours().toString().padStart(2, '0'); // 小时
        var mm = d.getMinutes().toString().padStart(2, '0'); // 分钟
        var ss = d.getSeconds().toString().padStart(2, '0'); // 秒
        return y + "-" + m + "-" + r + " " + hh + ":" + mm + ":" + ss; // es6 字符串模板
    }
    else {
        return '';
    }
};
exports.subtimehours = function (date) {
    if (date) {
        var date1 = (new Date().getTime() - new Date(date.replace(/-/g, '/')).getTime());
        var time = Math.floor(date1 / 1000 / 60 / 60);
        return time; // es6 字符串模板
    }
    else {
        return '';
    }
};
exports.subtimeminutes = function (date) {
    if (date) {
        var date1 = (new Date().getTime() - new Date(date.replace(/-/g, '/')).getTime());
        var time = Math.floor(date1 / 1000 / 60);
        console.log('time');
        console.log(time);
        return time; // es6 字符串模板
    }
    else {
        return '';
    }
};
exports.subtimeminutes1 = function (startdate, enddate) {
    if (startdate && enddate) {
        var date1 = (new Date(enddate.replace(/-/g, '/')).getTime() - new Date(startdate.replace(/-/g, '/')).getTime());
        var time = Math.floor(date1 / 1000 / 60);
        console.log('time');
        console.log(time);
        return time; // es6 字符串模板
    }
    else {
        return '';
    }
};
