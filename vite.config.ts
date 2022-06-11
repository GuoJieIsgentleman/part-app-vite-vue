import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
import type { UserConfig } from 'vite';
import { loadEnv } from './src/utils/viteBuild';

import copy from 'rollup-plugin-copy'
import legacy from '@vitejs/plugin-legacy'
//转换为传统浏览器


import styleImport from 'vite-plugin-style-import'

import vitePluginImp from 'vite-plugin-imp'




const pathResolve = (dir: string): any => {
  return resolve(__dirname, '.', dir);
};




const { VITE_PORT, VITE_OPEN, VITE_PUBLIC_PATH } = loadEnv();

const alias: Record<string, string> = {
  '/@': pathResolve('/src/'),
  'vue-i18n': 'vue-i18n/dist/vue-i18n.cjs.js',
};


// ,
//   legacy({
//     targets: ['> 1%, last 1 version, ie >= 11'],
//     additionalLegacyPolyfills: ['regenerator-runtime/runtime'], // 面向IE11时需要此插件
//   })

const viteConfig: UserConfig = {
  base: './',
  plugins: [vue(),
  copy({
    targets: [
      { src: './public/index.html', dest: './Index' }, //执行拷贝
    ]
  }),
  legacy({
    targets: ['> 1%, last 1 version, ie >= 11'],
    additionalLegacyPolyfills: ['regenerator-runtime/runtime'], // 面向IE11时需要此插件
  })

  ],
  root: process.cwd(),
  resolve: { alias },

  optimizeDeps: {
    include: ['element-plus/lib/locale/lang/zh-cn', 'element-plus/lib/locale/lang/en', 'element-plus/lib/locale/lang/zh-tw'],
  },
  server: {
    host: '0.0.0.0',
    port: 10000,
    // open: VITE_OPEN,
    // base: './',
    proxy: {
      '/api': {
        target: 'http://61.185.74.251:5556',
        ws: true,
        changeOrigin: true,
        rewrite: path => path.replace(/^\//, '')
      },
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: "./static/js",
    minify: 'esbuild',
    sourcemap: false,
    rollupOptions: {
      input: {
        // 入口文件
        main: resolve(__dirname, "index.html")

      },
    },
  },
  define: {
    __VUE_I18N_LEGACY_API__: JSON.stringify(false),
    __VUE_I18N_FULL_INSTALL__: JSON.stringify(false),
    __INTLIFY_PROD_DEVTOOLS__: JSON.stringify(false),
  },

};

export default viteConfig;