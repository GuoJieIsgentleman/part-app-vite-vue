

import pinyin
import sys
from hmac import new
from fastapi import FastAPI, File, UploadFile
from typing import Optional

import time

from pydantic.main import BaseModel

import connect as conn


# get tooling_detail
def gettooling_detail(currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0):

    # 每页多少条数据 默认10
    print(currentpagecount)
    # 传过来取多少页的数据
    print(pagesize)
    db = conn.getConn()
    print('获取备件列表'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()

    # 查询多少条
    cursor.execute("select count(id) from tooling_detail")
    data = cursor.fetchall()
    pages = 0
    # 查询分多少页
    if currentpagecount != 0:
        total = data[0][0]
        tem = total % currentpagecount
        tem1 = total // currentpagecount

        # 算出总页数
        pages = tem1 if tem == 0 else tem1+1

    start = currentpagecount*(pagesize-1)
    end = currentpagecount
    print('start')
    print(start)
    print('end')
    print(end)
    print(pages)
    print(data[0][0])

    cursor.execute(
        "select * from tooling_detail order by id  limit {0},{1}".format(start, end))
    data1 = cursor.fetchall()

    #
    res = {
        'total': data[0][0],
        'data1': data1,
        'pages': pages
    }

    return res


# 筛选查询

def selecttooling(
    part_spec: Optional[str] = None,
    part_name: Optional[str] = None,
    area: Optional[str] = None,
    type: Optional[str] = None,
):
    db = conn.getConn()
    print('查询备件'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()
    print('打印输出')
    print(part_spec)
    print(part_name)
    print(area)
    print(type)

    temlist = {
        'part_spec': part_spec,
        'part_name': part_name,
        'area': area,
        'type': type
    }
    strsql = ""
    for k, v in temlist.items():
        if v != "":
            if k == 'area':
                temsql = "and {0} like '{1}%'".format(k, v)
                strsql += temsql
            else:
                temsql1 = "and {0}='{1}'".format(k, v)
                strsql += temsql1
    print('strsql')
    print(strsql)
    sql = "select * from tooling_detail "
    mid = 'where 1=1 '
    if strsql == '':
        cursor.execute(sql)
        print('进到空字符串')
        data = cursor.fetchall()
        return data
    else:
        # testsql = sql + mid + strsql
        # print(testsql)
        cursor.execute(sql + mid + strsql)
        data = cursor.fetchall()
        # print('进到有条件')
        return data


# 获取区域
def getusearea():
    # 获取领用区域
    print('获取区域'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db = conn.getConn()
    cursor = db.cursor()
    cursor.execute('''
                  select LEFT(area,6)
 from tooling_detail   
group by LEFT(area,6)
                   
                   ''')
    data = cursor.fetchall()
    print(data)
    return data


# 获取类型

def gettype(area: Optional[str] = None):
    # 获取获取类型
    db = conn.getConn()
    cursor = db.cursor()

    if area == None:
        sql = "select type from tooling_detail    group by type"
        cursor.execute(sql
                       )
        data = cursor.fetchall()
        print(data)
        return data
    else:
        sql = "select type from tooling_detail where area like'%{0}%'group by type".format(
            area)
        cursor.execute(sql
                       )
        data = cursor.fetchall()
        print(data)
        return data


# 获取name

def getpartname(type: Optional[str] = None, area: Optional[str] = None):
    # 获取获取类型
    db = conn.getConn()
    cursor = db.cursor()

    print(type)

    if area == None:
        cursor.execute(
            "select * from tooling_detail where type='{0}' group by part_name "
            .format(type))
        data = cursor.fetchall()
        print('备件管理查询'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(data)
        return data
    else:
        cursor.execute(
            "select * from tooling_detail where type='{0}' and area like '%{1}%'"
            .format(type, area))
        data = cursor.fetchall()
        print('添加领用查询'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(data)
        return data


# 获取型号e

def getspesc(type: Optional[str] = None,  use_part_name: Optional[str] = None, area: Optional[str] = None):
    # 获取获取类型
    db = conn.getConn()
    cursor = db.cursor()

    if area == None:

        cursor.execute(
            "select * from tooling_detail where 1=1 and type='{0}' and part_name='{1}'  ".format(
                type, use_part_name))
        data = cursor.fetchall()
        print(data)
        return data
    else:
        cursor.execute(
            "select * from tooling_detail where 1=1 and type='{0}' and part_name='{1}' and area like '%{2}%'  ".format(
                type, use_part_name, area))
        data = cursor.fetchall()
        print(data)
        return data


# 操作删除


def deletepart(id: int):
    db = conn.getConn()
    print('删除工装备件记录')
    cursor = db.cursor()

    cursor.execute('''delete from
                   tooling_detail where id='{}'
                   '''.format(id))

    db.commit()
    print('删除完成')
    return '删除成功'


# 更新 tooling_part

def updatetooling(
        username: Optional[str] = None,
        id: Optional[int] = None,
        part_name: Optional[str] = None,
        part_spec: Optional[str] = None,
        area: Optional[str] = None,
        type: Optional[str] = None,
        new_balance: Optional[int] = None,
        new_original: Optional[int] = None,
        connection: Optional[str] = None):
    db = conn.getConn()
    print('更改备件结存')
    cursor = db.cursor()
    print('id')
    print(id)
    print('part_name')
    print(part_name)
    print('part_spec')
    print(part_spec)
    print('area')
    print(area)
    print('type')
    print(type)

    if id != None:
        print('--更改备件信息--')
        try:
            cursor.execute('''
                    UPDATE `part`.`tooling_detail`
                      SET `balance` = '{0}',
                          `original` = '{1}',
                          `connection` = '{2}',
                          `area`='{3}',
                          `part_name` = '{5}',
                          `part_spec` = '{6}',
                          `type` = '{7}'
                      WHERE
                        (`id` = '{4}')
                     
                    '''.format(new_balance, new_original, connection,
                               area, id, part_name, part_spec, type))
            db.commit()

            tooling_update_log(username, area, part_spec,
                               part_name, new_balance, "update")
            print('--更改备件成功--')
            cursor.execute('''
                select * from   tooling_detail

                where id={}

                           '''.format(id))
            data = cursor.fetchall()
            print('查询data')
            print(data)
            res = {
                'msg': '更新数据成功',
                'data': data
            }
            return res
        except ConnectionError:
            print('异常')
            return '更新失败'
    else:
        return '更新失败'


async def create_upload_file(imgid: str, time1:  Optional[str] = None, file: UploadFile = File(...)):

    try:

        print('进入到上传图片方法里面')
        print(file.filename)
        print(file.content_type)
        print(file.filename)
        print(time1)

        contents = await file.read()
        imgsrc = imgid+"_" + \
            time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".jpg"
        print(imgsrc)
        file = open(
            "F:\partapp\part-app-vite-momo\part-app-vite\part-app-vite\src\serverpy\static\\tooling_img\{}".format(imgsrc), "wb")
        file.write(contents)

        file.close()

        # 传到静态地址

        db = conn.getConn()
        cursor = db.cursor()

        cursor.execute('''
          UPDATE `part`.`tooling_detail`
          SET
          `partimgsrc` = '{0}'
          WHERE
            (`id` = '{1}')
                    '''.format('http://61.185.74.251:5556/static/tooling_img/'+imgsrc, imgid))

        db.commit()
        print("存取路径成功")
        return '上传成功'
    except Exception as e:
        print(e)
        print('出错')
        return '上传失败'


# 添加机修备件明细
def addtooling_detail(
        username: Optional[str] = None,
        part_name: Optional[str] = None,
        part_spec: Optional[str] = None,
        area: Optional[str] = None,
        balance: Optional[int] = 0,
        remark: Optional[str] = None,
        type: Optional[str] = None):

   # 增加备件
    db = conn.getConn()
    cursor = db.cursor()
    cursor.execute('''
                INSERT INTO `part`.`tooling_detail` (

          `part_name`,
          `part_spec`,
          `area`,
          `balance`,
          `original`,
          `remark`,
          `type`
        )
        VALUES
          (

            '{0}',
            '{1}',
            '{2}',
            '{3}',
            '{4}',
            '{5}',
            '{6}'
          );
          '''.format(part_name, part_spec, area, balance, balance, remark, type))
    db.commit()

    cursor.execute('''
                   select id from  tooling_detail where part_name='{0}'
                   and part_spec='{1}' and area='{2}' and type='{3}'
                   '''.format(part_name, part_spec, area, type))

    data = cursor.fetchall()
    res = {'msg': '添加成功', 'id': data[0][0]}

    # 增加日志记录
    tooling_update_log(username, area, part_spec,
                       part_name, balance, "add")
    return res


# 获取工装领用
def getuserecord(flag: Optional[str] = None,
                 flag1: Optional[str] = '',
                 start: Optional[str] = '',
                 end: Optional[str] = '',
                 prolince: Optional[str] = '',
                 area: Optional[str] = ''):
    db = conn.getConn()
    print('获取工装领用记录')
    print(flag)
    cursor = db.cursor()
    if flag == 'all' and flag1 == '':
        print('获取工装所有领用记录')
        cursor.execute("select * from adoption")
        data = cursor.fetchall()
        return data
    elif flag != 'all' and flag1 == '':
        print('获取工装未确认领用记录')
        cursor.execute("select * from adoption where useconfirm ='' ")
        data = cursor.fetchall()
        return data

    if flag1 == '筛选查询':
        sql = 'select * from adoption where 1=1 '

        starttime = ''
        area1 = ''
        endtime = ''
        prolince1 = ''

        if area != '':
            area1 = " and use_area like'%{}%'  ".format(area)

        if start != '':
            starttime = " and use_date >'{}'".format(start)
        if end != '':
            endtime = " and use_date<'{}'".format(end)

        if prolince != '':
            prolince1 = "  and use_procline='{}'".format(prolince)

        sql = "select * from adoption where 1=1 {0} {1} {2} {3} order by use_date".format(
            starttime, endtime, prolince1, area1)
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return data


# get tooling balance
def getbalance(type: Optional[str] = None,
               area: Optional[str] = None,
               spec: Optional[str] = None,
               part_name: Optional[str] = None):
    # 获取获取类型
    db = conn.getConn()
    cursor = db.cursor()
    print('type')
    print(type)
    print('area')
    print(area)
    print('spec')
    print(spec)
    print('part_name')
    print(part_name)
    cursor.execute(
        "select * from tooling_detail where area like '%{0}%' and type='{1}' and part_spec='{2}' and part_name='{3}' "
        .format(area, type, spec, part_name))
    data = cursor.fetchall()
    print('getbalance'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print(data)
    return data


class userecordform(BaseModel):
    user: str
    area: str
    type: str
    spec: str
    part_name: str
    use_count: str
    reason: str
    use_date: str
    confirm: str
    use_procline: str
    handle: str
    flag: str


def adduserecord(userecordform: Optional[userecordform] = None):
    print('增加领用记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    db = conn.getConn()
    cursor = db.cursor()

    # 增加领用记录 并且 减去库存数据
    print('userecordform.user')
    print(userecordform.user)
    print('userecordform.area')
    print(userecordform.area)
    print('userecordform.type')
    print(userecordform.type)
    print('userecordform.spec')
    print(userecordform.spec)
    print('userecordform.part_name')
    print(userecordform.part_name)
    print('userecordform.use_count')
    print(userecordform.use_count)
    print('userecordform.reason')
    print(userecordform.reason)
    print('userecordform.use_date')
    print(userecordform.use_date)
    print('userecordform.confirm')
    print(userecordform.confirm)
    print('userecordform.use_procline')
    print(userecordform.use_procline)
    print('userecordform.handle')
    print(userecordform.handle)
    print('userecordform.flag')
    print(userecordform.flag)
    cursor.execute(
        '''select *  from  tooling_detail where area  like '%{0}%'and part_spec='{1}' and type='{2}' and part_name='{3}'
    '''.format(userecordform.area, userecordform.spec, userecordform.type,
               userecordform.part_name))
    data = cursor.fetchall()
    print(data)
    print(data[0])
    print('-------减去件数 ---------' +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(data[0][4])

    count = data[0][4]
    cursor.execute('''update tooling_detail set balance={0}-{5}
        where part_name='{1}' and part_spec='{2}' and area='{3}' and type='{4}'
    '''.format(count, userecordform.part_name, userecordform.spec,
               userecordform.area, userecordform.type,
               userecordform.use_count))
    data = cursor.fetchall()
    db.commit()

    print('--------添加领用记录--------' +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 总记录
    cursor.execute('''
                   INSERT INTO `part`.`adoption`
                  (`user`, `use_area`,`use_procline`,
                  `type`, `spec`, `use_part_name`,
                  `use_count`, `user_reason`,
                  `use_date`, `useconfirm`,`handle`)
                  VALUES ('{0}', '{1}',
                  '{2}', '{3}', '{4}',
                  '{5}', '{6}', '{7}',DATE_FORMAT('{8}',"%Y-%m-%d %H:%i:%s"), '{9}','{10}');
    '''.format(userecordform.user, userecordform.area,
               userecordform.use_procline, userecordform.type,
               userecordform.spec, userecordform.part_name,
               userecordform.use_count, userecordform.reason,
               userecordform.use_date, userecordform.confirm,
               userecordform.handle))
    db.commit()

    print(userecordform.flag)
    print(userecordform.handle)
    # 保养记录
    if userecordform.handle == '保养' and userecordform.flag == 'confirm':
        print('--------保养--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   INSERT INTO `part`.`tooling_maintenance`
                   ( `user`, `use_area`, `type`, `spec`,
                   `use_part_name`, `use_count`, `user_reason`,
                   `use_date`, `useconfirm`,`use_procline`)
                   VALUES ('{0}', '{1}', '{2}', '{3}',
                   '{4}', '{5}', '{6}', '{7}', '{8}','{9}');
          '''.format(userecordform.user, userecordform.area,
                     userecordform.type, userecordform.spec,
                     userecordform.part_name, userecordform.use_count,
                     userecordform.reason, userecordform.use_date,
                     userecordform.confirm, userecordform.use_procline))
        db.commit()
        print('--------保养记录添加完成--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # if userecordform.handle == '外修' and userecordform.flag == 'confirm':
    #     print('--------外修-------- ' +
    #           time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     cursor.execute('''
    #                INSERT INTO `part`.`machine_repair`
    #                ( `user`, `use_area`, `type`, `spec`,
    #                `use_part_name`, `use_count`, `user_reason`,
    #                `use_date`, `useconfirm`,`use_procline`)
    #                VALUES ('{0}', '{1}', '{2}', '{3}',
    #                '{4}', '{5}', '{6}', '{7}', '{8}','{9}');
    #       '''.format(userecordform.user, userecordform.area,
    #                  userecordform.type, userecordform.spec,
    #                  userecordform.part_name, userecordform.use_count,
    #                  userecordform.reason, userecordform.use_date,
    #                  userecordform.confirm, userecordform.use_procline))

    #     db.commit()
    #     print('--------外修记录添加完成--------' +
    #           time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # if userecordform.handle == '报废' and userecordform.flag == 'confirm':
    #     print('--------报废--------' +
    #           time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     cursor.execute('''
    #                INSERT INTO `part`.`machine_scrap`
    #                ( `user`, `use_area`, `type`, `spec`,
    #                `use_part_name`, `use_count`, `user_reason`,
    #                `use_date`, `useconfirm`,`use_procline`)
    #                VALUES ('{0}', '{1}', '{2}', '{3}',
    #                '{4}', '{5}', '{6}', '{7}', '{8}','{9}');
    #       '''.format(userecordform.user, userecordform.area,
    #                  userecordform.type, userecordform.spec,
    #                  userecordform.part_name, userecordform.use_count,
    #                  userecordform.reason, userecordform.use_date,
    #                  userecordform.confirm, userecordform.use_procline))

    #     db.commit()
    #     print('--------报废记录添加完成--------' +
    #           time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    return '添加成功'


# update tooling use record
def updateuserecord(id: int,
                    useconfirm: Optional[str] = None,
                    use_count: Optional[str] = None,
                    use_area: Optional[str] = None,
                    use_date: Optional[str] = None,
                    use_part_name: Optional[str] = None,
                    type: Optional[str] = None,
                    spec: Optional[str] = None,
                    user: Optional[str] = None,
                    user_reason: Optional[str] = None,
                    confirm_date: Optional[str] = None,
                    flag: Optional[str] = None,
                    username: Optional[str] = None,
                    password: Optional[str] = None,
                    handle: Optional[str] = None,
                    use_procline: Optional[str] = None):
    db = conn.getConn()
    print('获取领用记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print('id', id)

    print('useconfirm', useconfirm)

    print('use_count', use_count)

    print('use_area', use_area)

    print('use_date', use_date)

    print('use_part_name', use_part_name)

    print('type', type)

    print('spec', spec)

    print('user', user)

    print('user_reason', user_reason)

    print('confirm_date', confirm_date)

    print('flag', flag)
    print('handle', handle)

    cursor = db.cursor()

    if flag == '删除':
        cursor.execute('''
               delete from `user`  where username='{}'

                     '''.format(username))
        db.commit()
        print('删除成功')
    else:
        print('更新领用表 确认班长'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                     UPDATE `part`.`adoption`
                      SET
                       `useconfirm` = '{0}',
                       `confirm_date` = '{1}',
                       `handle`='{2}'
                      WHERE
                      	(`id` = '{3}');

                     '''.format(useconfirm, confirm_date, handle, id))

        db.commit()
        print('更新成功')

    # 保养记录
    if handle == '保养' and flag == 'confirm':
        print('--------保养--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   INSERT INTO `part`.`tooling_maintenance`
                   ( `user`, `use_area`, `type`, `spec`,
                   `use_part_name`, `use_count`, `user_reason`,
                   `use_date`,`use_procline` )
                   VALUES ('{0}', '{1}', '{2}', '{3}',
                   '{4}', '{5}', '{6}', '{7}','{8}');
          '''.format(user, use_area,
                     type, spec,
                     use_part_name, use_count,
                     '', use_date, use_procline
                     ))
        db.commit()
        print('--------保养记录添加完成--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # if handle == '外修' and flag == 'confirm':
    #     print('--------外修--------')
    #     cursor.execute('''
    #                INSERT INTO `part`.`machine_repair`
    #                ( `user`, `use_area`, `type`, `spec`,
    #                `use_part_name`, `use_count`, `user_reason`,
    #                `use_date`,`use_procline`)
    #                VALUES ('{0}', '{1}', '{2}', '{3}',
    #                '{4}', '{5}', '{6}', '{7}','{8}');
    #       '''.format(user, use_area,
    #                  type, spec,
    #                  use_part_name, use_count,
    #                  '', use_date, use_procline))

    #     db.commit()
    #     print('--------外修记录添加完成--------' +
    #           time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # if handle == '报废' and flag == 'confirm':
    #     print('--------报废--------')
    #     cursor.execute('''
    #                INSERT INTO `part`.`machine_scrap`
    #                ( `user`, `use_area`, `type`, `spec`,
    #                `use_part_name`, `use_count`, `user_reason`,
    #                `use_date`,`use_procline`)
    #                VALUES ('{0}', '{1}', '{2}', '{3}',
    #                '{4}', '{5}', '{6}', '{7}','{8}');
    #       '''.format(user, use_area,
    #                  type, spec,
    #                  use_part_name, use_count,
    #                  '', use_date,
    #                  use_procline))

    #     db.commit()
    #     print('--------报废记录添加完成--------' +
    #           time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # if handle == '设备整改':
    #     print('--------增加设备整改记录--------')
    #     sql = f'''
    #     INSERT INTO `part`.`machine_equipment_rectification` (
    #           `user`,`use_area`,`type`,
    #           `spec`,`use_part_name`,`use_count`,
    #           `user_reason`,`use_date`,`use_procline`,
    #           `remark`
    #         )
    #         VALUES
    #           (
    #             '{user}','{use_area}','{type}',
    #             '{spec}','{use_part_name}','{use_count}',
    #             '{user_reason}','{use_date}',
    #             '{use_procline}',
    #             '{type}_{handle}'
    #           );
    #     '''
    #     cursor.execute(sql)

    #     db.commit()
    #     print('--------设备整改记录添加完成--------')
    return '成功！'


# 获取工装保养记录
def getmaintenance(flag: Optional[str] = '',
                   flag1: Optional[str] = '',
                   start: Optional[str] = '',
                   end: Optional[str] = '',
                   prolince: Optional[str] = '',
                   area: Optional[str] = ''):
    db = conn.getConn()

    cursor = db.cursor()

    if flag == 'all' and flag1 == '':
        print('获取所有保养记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute("select * from d")
        data = cursor.fetchall()
        return data
    elif flag != 'all' and flag1 == '':
        print('获取未确认保养记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(
            "select * from tooling_maintenance where useconfirm ='' or maintenanceman=''  ")
        data = cursor.fetchall()
        return data

    if flag1 == '筛选查询':
        sql = 'select * from tooling_maintenance where 1=1 '
        print('start')
        print(start)
        print('flag')
        print(flag)
        msg1 = ''
        starttime = ''
        endtime = ''
        prolince1 = ''
        area1 = ''
        if flag == '是':

            msg1 = " and  remark ='{}'".format("无库存备件保养")

        if area != '':
            area1 = " and use_area ='{}'".format(area)

        if start != '':
            starttime = " and use_date >'{}'".format(start)
        if end != '':
            endtime = " and use_date<'{}'".format(end)
            print('end')
            print(end)
        if prolince != '':
            prolince1 = "  and use_procline='{}'".format(prolince)
            print('prolince')
            print(prolince)
            print(prolince1)
        sql = "select * from tooling_maintenance where 1=1 {0}{1}{2}{3}{4} order by use_date".format(
            starttime, endtime, prolince1, area1, msg1)
        print('sql')
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return data


# update maintenance
def updatemaintenance(id: int,
                      user: Optional[str] = '',
                      new_area: Optional[str] = '',
                      type: Optional[str] = '',
                      spec: Optional[str] = '',
                      use_part_name: Optional[str] = '',
                      use_date: Optional[str] = '',
                      use_area: Optional[str] = '',
                      use_count: Optional[str] = '',
                      useconfirm: Optional[str] = '',
                      maintenanceman: Optional[str] = '',
                      maintenance_date: Optional[str] = '',
                      scrap: Optional[str] = '',
                      useconfirmdate: Optional[str] = '',
                      use_procline: Optional[str] = '',
                      flag: Optional[str] = ''
                      ):
    print('更新保养记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print('id', id)
    print('user', user)
    print('new_area', new_area)
    print('flag', flag)

    db = conn.getConn()
    cursor = db.cursor()

    print('maintenanceman')
    print(maintenanceman)
    print(maintenance_date)

    # 处理成套
    print('flag')
    print(flag)
    # if flag != '':
    #     temp1 = flag.split('_')
    #     x = temp1[1]
    # if '成套' in flag:
    #     print('进入成套处理环节')
    #     if scrap == '成套报废':

    #         cursor.execute('''
    #                INSERT INTO `part`.`machine_scrap`
    #                ( `user`, `use_area`, `type`, `spec`,
    #                `use_part_name`, `use_count`, `remark`,
    #                `use_date`,`use_procline`)
    #                VALUES ('{0}', '{1}', '{2}', '{3}',
    #                '{4}', '{5}', '{6}', '{7}', '{8}');
    #       '''.format(user, use_area, type, spec, use_part_name, use_count,
    #                  f'成套备件保养转报废_{x}', maintenance_date, use_procline))

    #         db.commit()
    #     else:
    #         # 不报废
    #         # 查询在这个区域有没有
    #         cursor = db.cursor()
    #         sql = f''' select count(id) from machine_parts_detail where machine_part_name='{x}' and area='{new_area}' '''

    #         cursor.execute(sql)
    #         rs = cursor.fetchone()

    #         if rs[0] > 0:
    #             # update
    #             print('更新区域成套')
    #             sql1 = f''' update machine_parts_detail set original=original+{use_count} where machine_part_name='{x}' and area='{new_area}' '''

    #             cursor.execute(sql1)
    #             db.commit()
    #             dealwithcount(x, new_area)  # 修正成套件数
    #             print('更新成套库存完成')

    #         else:
    #             mid = pinyin.get_initial(
    #                 f'{x}_{new_area}', delimiter="")
    #             print('新增区域成套')
    #             cursor.execute(f'''
    #                 INSERT INTO `part`.`machine_parts_detail` (

    #                       `part_name`,
    #                       `part_spec`,
    #                       `area`,
    #                       `balance`,
    #                       `original`,
    #                       `remark`,
    #                       `type`,
    #                       `partimgsrc`,
    #                       `type1`,
    #                       `machine_part_name`,
    #                       `machine_part_id`
    #                     )
    #                     VALUES
    #                       (
    #                         '{use_part_name}',
    #                         '{spec}',
    #                         '{new_area}',
    #                         {use_count},
    #                         {use_count},
    #                         '',
    #                         '{type}',
    #                         '',
    #                         '机械',
    #                         '{x}',
    #                         '{mid}'
    #                       );
    #           ''')
    #             db.commit()
    #             dealwithcount(x, new_area)  # 修正成套件数
    #             print('新增成套库存完成')

    #     print('开始更新保养确认班长'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     cursor.execute('''
    #               UPDATE `part`.`machine_maintenance`
    #                 SET
    #                 `useconfirm` = '{0}',`new_area`='{1}',`useconfirmdate`='{3}',`handle`='{4}'
    #                 WHERE  `id` = {2}

    #                 '''.format(useconfirm, new_area, id, useconfirmdate, scrap))
    #     db.commit()
    #     print('更新保养确认班长名成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     return '成功！'

    if '无库存' in flag:
        print('flag')
        print(flag)
        print('scrap')
        print(scrap)
        print('无库存备件更新记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                     UPDATE `part`.`tooling_maintenance`
                      SET
                       `useconfirm` = '{0}',`useconfirmdate`='{1}',`handle`='{3}',`new_area`='{4}'
                      WHERE  `id` = {2}

                       '''.format(useconfirm, useconfirmdate, id, scrap, new_area))
        db.commit()

    #     if scrap == '外修':

    #         cursor.execute('''
    #                INSERT INTO `part`.`machine_repair`
    #               (`user`, `use_area`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`remark`,`use_procline`)
    #               VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}',
    #                       '{6}', DATE_FORMAT('{7}','%Y-%m-%d %H:%i:%s'),'{8}','{9}');
    # '''.format(user, use_area, type, spec, use_part_name, use_count, '', use_date, flag+"转外修", use_procline))
    #         db.commit()
    #         return '确认完成 新增外修记录'

    #     if scrap == '报废':
        #   cursor.execute('''
        #          INSERT INTO `part`.`machine_scrap`
        #          ( `user`, `use_area`, `type`, `spec`,
        #          `use_part_name`, `use_count`, `remark`,
        #          `use_date`,`use_procline`)
        #          VALUES ('{0}', '{1}', '{2}', '{3}',
        #          '{4}', '{5}', '{6}', '{7}', '{8}');
        # '''.format(user, use_area, type, spec, use_part_name, use_count,
        #            '无库存备件保养转报废', maintenance_date, use_procline))

        #   db.commit()
        #   return '确认完成 新增报废记录'
        return '更新完成'

    # 报废流程

    # if scrap == '报废' and new_area == '' and flag == '':
    #     # 增加报废记录
    #     print('增加报废记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     cursor.execute('''
    #                INSERT INTO `part`.`machine_scrap`
    #                ( `user`, `use_area`, `type`, `spec`,
    #                `use_part_name`, `use_count`, `user_reason`,
    #                `use_date`,`use_procline`)
    #                VALUES ('{0}', '{1}', '{2}', '{3}',
    #                '{4}', '{5}', '{6}', '{7}', '{8}');
    #       '''.format(user, use_area, type, spec, use_part_name, use_count,
    #                  '保养报废', maintenance_date, use_procline))

    #     db.commit()
    #     print('增加报废记录成功  '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     cursor.execute('''
    #                  UPDATE `part`.`machine_maintenance`
    #                   SET
    #                    `useconfirm` = '{0}',`useconfirmdate`='{1}',`handle`='{3}'
    #                   WHERE  `id` = {2}

    #                    '''.format(useconfirm, useconfirmdate, id, scrap))
    #     db.commit()
    #     print('更新保养确认班长名成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     print('增加报废记录成功')
    #     return '报废成功'

    if useconfirm == '' and maintenanceman != '' and flag != '无库存备件保养':

        print('更新保养人'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''

                     UPDATE `part`.`tooling_maintenance`
                     SET `maintenanceman` = '{0}',`maintenance_date` = '{1}'
                     WHERE 	`id` = {2}


      '''.format(maintenanceman, maintenance_date, id))
        db.commit()
        print('更新保养人成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return '保养人更新成功'

    elif useconfirm != '' and maintenanceman != '' and flag != '无库存备件保养':
        # 更新库存

        print(use_count)
        print(type)
        print(spec)
        print(use_part_name)
        print('id')
        print(id)
        print('use_area')
        print(use_area)
        print('new_area')
        print(new_area)
        print('useconfirm')
        print(useconfirm)

    #     if scrap == "外修":
    #         print('转换到外修'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #         cursor.execute('''
    #                INSERT INTO `part`.`machine_repair`
    #               (`user`, `use_area`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`use_procline`)
    #               VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}',
    #                       '{6}', DATE_FORMAT('{7}','%Y-%m-%d %H:%i:%s'),'{8}');
    # '''.format(user, use_area, type, spec, use_part_name, use_count, '', use_date, use_procline))
    #         db.commit()

        # return '增加外修成功'
        # 保养件数
        # 如果搁置区域有 就加1 否则就新增一条

        # 增加最新搁置区域
        # else:
        cursor.execute('''
              SELECT
                  *
                FROM
                  tooling_detail
                WHERE
                1=1
                AND type = '{0}'
                AND part_spec = '{1}'
                AND part_name = '{2}'
                and area='{3}'
      '''.format(type, spec, use_part_name, new_area))

        data = cursor.fetchall()
        # 增加
        if len(data) != 0:
            print('updatemaintenance')
            print(data)
            count = data[0][4]

            cursor.execute('''update tooling_detail set balance={0}+{5}
              where part_name='{1}' and part_spec='{2}' and area='{3}' and type='{4}'
        '''.format(count, use_part_name, spec, use_area, type, use_count))

            db.commit()
            print('保养数据更新成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        else:

            print('该区域无设备信息 新增')
            cursor.execute('''
                                INSERT INTO `part`.`tooling_detail` (
                                `part_name`,
                                `part_spec`,
                                `area`,
                                `balance`,
                                `original`,
                                `remark`,
                                `type`
                              )
                            VALUES
                                (
                                  '{0}',
                                  '{1}',
                                  '{2}',
                                  '{3}',
                                  '{4}',
                                  '',
                                  '{5}'
                                );
                            '''.format(use_part_name, spec, new_area, use_count,
                                       use_count, type))
            db.commit()

        # 更新确认人
        print('开始更新保养确认班长以及搁置产线'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                  UPDATE `part`.`tooling_maintenance`
                    SET
                    `useconfirm` = '{0}',`new_area`='{1}',`useconfirmdate`='{3}',`handle`='{4}'
                    WHERE  `id` = {2}

                    '''.format(useconfirm, new_area, id, useconfirmdate, scrap))
        db.commit()
        print('更新保养确认班长名成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return '成功！'


def addmaintenance(user: str, area: str, type: str, spec: str, part_name: str,
                   use_count: str, reason: str, use_date: str, confirm: str,
                   flag: Optional[str] = None):
    print('增加保养记录')

    db = conn.getConn()
    cursor = db.cursor()

    # 增加领用记录 并且 减去库存数据
    # print(user)
    # print(area)
    # print(type)
    # print(spec)
    # print(part_name)
    # print(use_count)
    # print(reason)
    # print(use_date)
    # print(confirm)

    if flag == '无库存备件保养':

        cursor.execute('''
                    INSERT INTO `part`.`tooling_maintenance`
                    (`user`, `use_procline`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`remark`)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',
                           '{7}', '{8}');
      '''.format(user, area, type, spec, part_name, use_count, reason, use_date,
                 flag))
        db.commit()
        # 开始增加记录

        return '添加成功'


class Item(BaseModel):
    user: Optional[str] = None,
    username: Optional[str] = None,
    area: Optional[str] = None,
    spec: Optional[str] = None,
    item_name: Optional[str] = None,
    count: Optional[int] = 0


# tooling update api

def tooling_update_log(
        username: Optional[str] = None,
        area: Optional[str] = None,
        spec: Optional[str] = None,
        item_name: Optional[str] = None,
        count: Optional[int] = 0,
        flag: Optional[str] = None):

    # 更新记录表
    db = conn.getConn()
    cursor = db.cursor()
    if flag == 'add':
        cursor.execute(f''' INSERT INTO `part`.`log` (`username`, `area`, `spec`, `iten_name`, `count`, `create_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'add','工装管理');
    ''')
        print("增加记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if flag == 'update':
        cursor.execute(f''' INSERT INTO `part`.`log` ( `username`, `area`, `spec`, `iten_name`, `count`, `update_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'update','工装管理');
    ''')
        print("更新记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db.commit()
