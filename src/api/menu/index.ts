import { ElMessage } from 'element-plus';
import request from '/@/utils/request';

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
export function getMenuAdmin(params?: any) {
  try {

    return request({
      url: '/getroutes',
      // url: '/api/getroutes',
      method: 'get',
      params,
    });
  } catch (error) {
      
  }
 

}

/**
 * 获取后端动态路由菜单(test)
 * @link 参考：https://gitee.com/lyt-top/vue-next-admin-images/tree/master/menu
 * @param params 要传的参数值，非必传
 * @returns 返回接口数据
 */
export function getMenuOther(params?: any) {

  return request({
    url: '/getroutes',
    method: 'get',
    params,
  });

}
