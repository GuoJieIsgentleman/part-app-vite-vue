import { createI18n } from 'vue-i18n';
import zhcnLocale from 'element-plus/lib/locale/lang/zh-cn';
import enLocale from 'element-plus/lib/locale/lang/en';
import zhtwLocale from 'element-plus/lib/locale/lang/zh-tw';
import { store } from '../../src/store/index';

import nextZhcn from './lang/zh-cn';
import nextEn from './lang/en';
import nextZhtw from './lang/zh-tw';

import pagesHomeZhcn from './pages/home/zh-cn';
import pagesHomeEn from './pages/home/en';
import pagesHomeZhtw from './pages/home/zh-tw';
import pagesLoginZhcn from './pages/login/zh-cn';
import pagesLoginEn from './pages/login/en';
import pagesLoginZhtw from './pages/login/zh-tw';
import pagesFormI18nZhcn from './pages/formI18n/zh-cn';
import pagesFormI18nEn from './pages/formI18n/en';
import pagesFormI18nZhtw from './pages/formI18n/zh-tw';

// 定义语言国际化内容
/**
 * 说明：
 * /src/i18n/lang 下的 ts 为框架的国际化内容
 * /src/i18n/pages 下的 ts 为各界面的国际化内容
 */
const messages = {
  [zhcnLocale.name]: {
    el: zhcnLocale.el,
    message: {
      ...nextZhcn,
      ...pagesHomeZhcn,
      ...pagesLoginZhcn,
      ...pagesFormI18nZhcn,
    },
  },
  [enLocale.name]: {
    el: enLocale.el,
    message: {
      ...nextEn,
      ...pagesHomeEn,
      ...pagesLoginEn,
      ...pagesFormI18nEn,
    },
  },
  [zhtwLocale.name]: {
    el: zhtwLocale.el,
    message: {
      ...nextZhtw,
      ...pagesHomeZhtw,
      ...pagesLoginZhtw,
      ...pagesFormI18nZhtw,
    },
  },
};

// 导出语言国际化
export const i18n = createI18n({
  locale: store.state.themeConfig.themeConfig.globalI18n,
  fallbackLocale: zhcnLocale.name,
  messages,
});
