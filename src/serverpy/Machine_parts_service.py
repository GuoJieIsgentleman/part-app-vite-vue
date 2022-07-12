

import pinyin
import sys

# 定义机器维修的主要环节


from fastapi import FastAPI, File, UploadFile
from typing import Optional

import time

import connect as conn

# from serverpy.untils import machine

# 获取成套备件列表


def getparts(currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0):

    # 每页多少条数据 默认10
    print('currentpagecount  ', currentpagecount)
    # 传过来取多少页的数据
    print('pagesize  ', pagesize)
    db = conn.getConn()
    print('获取备件列表'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()

    # 查询多少条
    cursor.execute("select count(id) from machine_parts_detail")
    data = cursor.fetchall()
    pages = 0
    print('data[0] total ', data[0][0])
    # 查询分多少页
    if currentpagecount != 0:
        total = data[0][0]
        tem = total % currentpagecount
        tem1 = total // currentpagecount
        print('tem---', tem)
        print('tem1---', tem1)
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
        "select * from machine_parts_detail order by id  limit {0},{1}".format(start, end))
    data1 = cursor.fetchall()

    #
    res = {
        'total': data[0][0],
        'data1': data1,
        'pages': pages
    }
    print(res)
    return res


def getusearea():
    # 获取领用区域
    print('获取区域'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db = conn.getConn()
    cursor = db.cursor()
    cursor.execute("select area from machine_parts_detail group by area")
    data = cursor.fetchall()
    print(data)
    return data


# 获取成套领用
def getuserecord(flag: Optional[str] = None,
                 flag1: Optional[str] = '',
                 start: Optional[str] = '',
                 end: Optional[str] = '',
                 prolince: Optional[str] = '',
                 area: Optional[str] = ''):
    db = conn.getConn()
    print('获取成套备件领用记录')
    print(flag)
    cursor = db.cursor()
    if flag == 'all' and flag1 == '':
        print('获取成套备件所有领用记录')
        cursor.execute("select * from machine_parts_use")
        data = cursor.fetchall()
        return data
    elif flag != 'all' and flag1 == '':
        print('获取成套未确认领用记录')
        cursor.execute("select * from machine_parts_use where useconfirm ='' ")
        data = cursor.fetchall()
        return data

    if flag1 == '筛选查询':
        sql = 'select * from machine_parts_use where 1=1 '

        starttime = ''
        area1 = ''
        endtime = ''
        prolince1 = ''

        if area != '':
            area1 = " and use_area='{}'  ".format(area)

        if start != '':
            starttime = " and use_date >'{}'".format(start)
        if end != '':
            endtime = " and use_date<'{}'".format(end)

        if prolince != '':
            prolince1 = "  and use_procline='{}'".format(prolince)

        sql = "select * from machine_parts_use where 1=1 {0} {1} {2} {3} order by use_date".format(
            starttime, endtime, prolince1, area1)
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return data


# 获取成套名称

def getmachine_part_names(area: str):
    db = conn.getConn()
    print('获取成套名称'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()

    cursor.execute(f'''
               select  machine_part_name from machine_parts_detail  where area='{area}'  group by machine_part_name

                   ''')

    data = cursor.fetchall()

    return data


# 上传成套图片
async def create_upload_file(machine_part_name: str, imgid: str, time1:  Optional[str] = None, file: UploadFile = File(...)):

    print(file.filename)
    print(file.content_type)
    print(file.filename)
    print(time1)
    contents = await file.read()
    imgsrc = imgid+"_" + \
        time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".jpg"
    print(imgsrc)
    file = open(
        "F:\partapp\part-app-vite-momo\part-app-vite\part-app-vite\src\serverpy\static\machine_parts_img\{}".format(imgsrc), "wb")
    file.write(contents)

    # 传到静态地址

    db = conn.getConn()
    cursor = db.cursor()

    # 先查询这个成套名称明细有几个 如果有2个就更新为一个url

    sql = f''' select count(*) from machine_parts_detail  where machine_part_name='{machine_part_name}' '''
    cursor.execute(sql)
    rs = cursor.fetchone()
    print('rs', rs)
    print(rs[0])
    if rs[0] > 1:
        sql1 = f'''select partimgsrc from machine_parts_detail  where machine_part_name='{machine_part_name}' and partimgsrc !=''  '''
        cursor.execute(sql)
        rs1 = cursor.fetchone()
        sql2 = f''' update machine_parts_detail set partimgsrc ='{rs1[0]}'  where machine_part_name='{machine_part_name}' and partimgsrc ='' '''

    else:
        cursor.execute('''
          UPDATE `part`.`machine_parts_detail`
          SET
          `partimgsrc` = '{0}'
          WHERE
            (`id` = '{1}')
                    '''.format('http://61.185.74.251:5556/static/machine_parts_img/'+imgsrc, imgid))

        db.commit()
        return '上传成功'


def selectpart(
    part_spec: Optional[str] = None,
    part_name: Optional[str] = None,
    area: Optional[str] = None,
    type: Optional[str] = None,
):
    db = conn.getConn()
    print('查询备件'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()

    part_spec1 = ''
    part_name1 = ''
    area1 = ''
    type1 = ''

    if part_spec != '':
        part_spec1 = " and part_spec='{}'".format("part_spec")
    if area != '':
        area1 = " and area='{}'".format(area)
    if part_name != '':
        part_name1 = " and part_name ='{}'".format(part_name)
    if type != '':
        type1 = " and type='{}'".format(type)

    sql = "select * from machine_parts_detail where 1=1 {0}{1}{2}{3} order by machine_part_name,id".format(
        part_spec1, part_name1, type1, area1)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()

    return data


def gettype(area: Optional[str] = None):
    # 获取获取类型
    db = conn.getConn()
    cursor = db.cursor()

    if area == None:
        sql = "select type from machine_parts_detail    group by type"
        cursor.execute(sql
                       )
        data = cursor.fetchall()
        print(data)
        return data
    else:
        sql = "select type from machine_parts_detail where area='{0}'group by type".format(
            area)
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        return data


def getspesc(type: Optional[str] = None,  use_part_name: Optional[str] = None, area: Optional[str] = None):
    # 获取获取类型
    db = conn.getConn()
    cursor = db.cursor()

    if area == None:

        cursor.execute(
            "select * from part_detail where 1=1 and type='{0}' and part_name='{1}'  ".format(
                type, use_part_name))
        data = cursor.fetchall()
        print(data)
        return data
    else:
        cursor.execute(
            "select * from part_detail where 1=1 and type='{0}' and part_name='{1}' and area='{2}'  ".format(
                type, use_part_name, area))
        data = cursor.fetchall()
        print(data)
        return data


def deletepart(single_part_name: str, flag: str, part_id: str):

    print(single_part_name)
    print(flag)
    print(part_id)
    try:

        db = conn.getConn()
        print('删除成套备件记录')
        cursor = db.cursor()
        cursor.execute('''delete from
                  machine_parts_detail where part_name='{0}' and id ='{1}'
                  '''.format(single_part_name, part_id))
        db.commit()
        print('删除完成')
        return '删除成功'
    except Exception as e:
        print(e)
        db.rollback()
        return '删除失败,请刷新重试'


# 添加成套备件 模式需要添加成对的东西


def addparts(
        username: Optional[str] = None,
        part_name: Optional[str] = None,
        part_spec: Optional[str] = None,
        area: Optional[str] = None,
        balance: Optional[int] = 0,
        original: Optional[int] = 0,
        remark: Optional[str] = None,
        machine_part_name: Optional[str] = None,
        type: Optional[str] = None,
        type1: Optional[str] = None,
        machine_part_id: Optional[str] = None,
        connection: Optional[str] = None):

   # 增加备件

   # 如果增加的区域有相关的备件 就直接合并到这个区域
    try:
        mid = pinyin.get_initial(
            f'{machine_part_name}_{area}', delimiter="")
        db = conn.getConn()
        cursor = db.cursor()
        cursor.execute(f'''
                    INSERT INTO `part`.`machine_parts_detail` (

                          `part_name`,
                          `part_spec`,
                          `area`,
                          `balance`,
                          `original`,
                          `remark`,
                          `type`,
                          `partimgsrc`,
                          `connection`,
                          `type1`,
                          `machine_part_name`,
                          `machine_part_id`
                        )
                        VALUES
                          (

                            '{part_name}',
                            '{part_spec}',
                            '{area}',
                            {balance},
                            {original},
                            '{remark}',
                            '{type}',
                            '',
                            '{connection}',
                            '{type1}',
                            '{machine_part_name}',
                            '{mid}'
                          );
              ''')
        db.commit()
        machine_parts_update_log(
            username, area, part_spec, part_name, balance, "add")
        cursor.execute('''
                      select id from  machine_parts_detail where part_name='{0}'
                      and part_spec='{1}' and area='{2}' and type='{3}'
                      '''.format(part_name, part_spec, area, type))

        data = cursor.fetchall()
        res = {'msg': '添加成功', 'id': data[0][0]}

        return res
    except Exception as e:

        print(e)

        db.rollback()
        return '错误'


# 获取成套单体备件信息


def get_part_balanceinfo(part_name):

    db = conn.getConn()
    cursor = db.cursor()
    cursor.execute(
        '''
             select *  from part_detail where part_name='{}'
             '''.format(
            part_name))
    data = cursor.fetchall()
    print(data)
    return data


def addmachine_part_count(part_name, area, addcount, machine_part_area):
    print(part_name)

    print(area)
    print(addcount)
    print(machine_part_area)
    try:
        print('减少备件库存')
        subsql = f"update part_detail set balance=balance-{addcount}  where  part_name='{part_name}' and area='{area}' "
        db = conn.getConn()
        cursor = db.cursor()
        cursor.execute(subsql)

        print('减少备件库存成功')

        print('增加成套单件库存')
        addsql = f"update machine_parts_detail set balance=balance+{addcount}  where  part_name='{part_name}' and area='{machine_part_area}' "
        cursor.execute(subsql)
        print('增加成套单件库存成功')
        print('wait success')
        db.commit()
        print('commit success')

        return '成功'
    except Exception as e:
        print(e)
        # db.rollback()
        return '失败'


def update_machine_part(
        username: Optional[str] = None,
        id: Optional[str] = None,
        part_name: Optional[str] = None,
        part_spec: Optional[str] = None,
        area: Optional[str] = None,
        type: Optional[str] = None,
        new_balance: Optional[str] = None,
        new_original: Optional[str] = None,
        connection: Optional[str] = None,
        machine_part_name: Optional[str] = None):

    print(id)
    print(part_name)
    print(part_spec)
    print(area)
    print(new_balance)
    print(new_original)
    print(connection)
    try:
        print('更新成套单件结存')
        db = conn.getConn()
        cursor = db.cursor()
        sql = f'''
             update machine_parts_detail set original={new_balance} where id='{id}' and part_name='{part_name}'
            '''
        cursor.execute(sql)
        db.commit()
        print('更新成套单件结存成功')
        dealwithcount(machine_part_name, area)
        machine_parts_update_log(
            username, area, part_spec, part_name, new_balance, "update")
        return '修改成功'
    except Exception as e:
        print(e)
        db.rollback()


def getmachine_parts_singlepart(machine_part_name: Optional[str] = None):

    db = conn.getConn()
    cursor = db.cursor()
    sql = f'''
           select * from machine_parts_detail where machine_part_name='{machine_part_name}'
          '''
    cursor.execute(sql)
    rs = cursor.fetchall()
    print(rs)
    print('更新成套单件结存成功')
    return {'msg': 'success', 'data': rs}


# 增加领用记录
def addmachine_part_userecord(part_name: Optional[str] = '',
                              part_spec: Optional[str] = '',
                              reason: Optional[str] = '',
                              use_count: Optional[str] = '',
                              type1: Optional[str] = '',
                              handle: Optional[str] = '',
                              use_area: Optional[str] = '',
                              user: Optional[str] = '',
                              use_date: Optional[str] = '',
                              type: Optional[str] = '',
                              use_procline: Optional[str] = '',
                              machine_part_name: Optional[str] = ''):

    print('添加成套领用记录')
    print('part_name', part_name)
    print('part_spec', part_spec)
    print('handle', handle)
    print('reason', reason)
    print('use_count', use_count)
    print('type1', type1)
    print('use_area', use_area)
    print('machine_part_name', machine_part_name)
    try:
        # 减少成套单件库存 usecount
        db = conn.getConn()

        cursor = db.cursor()
        sql = f'''
        update machine_parts_detail set original=original-{use_count}
        where  part_name='{part_name}'
        and part_spec='{part_spec}'
        and area='{use_area}'
        '''
        cursor.execute(sql)
        db.commit()
        print('更新成套单件库存')
        dealwithcount(machine_part_name, use_area)
        print('更新成套单件库存完成')
        print('增加成套领用记录')

        cursor.execute(f'''
                 		INSERT INTO `part`.`machine_parts_use` (
	`user`,`use_area`,`use_procline`,`type`,`spec`,`use_part_name`,`use_count`,`user_reason`,`use_date`,`handle`)
 VALUES('{user}','{use_area}','{use_procline}','{type}','{part_spec}','{part_name}','{use_count}','{reason}','{use_date}','{handle}');
                       '''
                       )
        db.commit()

        if handle == '设备整改':
            print('', handle)
            sql = f'''
            INSERT INTO `part`.`machine_parts_equipment_rectification` (
	`user`,`use_area`,`type`,`spec`,`use_part_name`,`use_count`,`user_reason`,`use_date`,`use_procline`,`remark`,`machine_part_name`
)
VALUES
	(
	'{user}','{use_area}','{type}','{part_spec}','{part_name}','{use_count}','{reason}','{use_date}','{use_procline}','{reason}','{machine_part_name}'
	);
            '''
            cursor.execute(sql)
            print('开始增加设备整改记录')
            db.commit()

            return f'{type1}-{part_spec}-{part_name}增加设备整改记录成功'
        if type1 == '机械':

            # 走机修保养
            print('机械  :')
            if handle == '保养':

                print('机械      ', handle)
                # 整体操作
                # 增加机修保养记录 machine_use
                print('开始增加机修保养')
                cursor.execute('''
                INSERT INTO `part`.`machine_maintenance`
                ( `user`, `use_area`, `type`, `spec`,
                `use_part_name`, `use_count`, `user_reason`,
                `use_date`, `use_procline`,`remark`)
                VALUES ('{0}', '{1}', '{2}', '{3}',
                '{4}', '{5}', '{6}', '{7}', '{8}','{9}');
                '''.format(user, use_area,
                           type, part_spec,
                           part_name, use_count,
                           reason, use_date,
                           use_procline, f'成套机械保养_{machine_part_name}_{reason}'))
                db.commit()
                return '机械保养成功'

        else:
            # 走电器 保养 外修
            print('电器')

            if handle == '保养':
                print('电器      ', handle)
                # 整体操作
                # 增加电器保养记录 part 保养记录
                print('走电器保养新增')
                cursor.execute('''
                INSERT INTO `part`.`maintenance_detail`
                (`user`,`use_area`, `use_procline`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`remark`)
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',
                      '{7}', '{8}','{9}');
                '''.format(user, use_area, use_procline, type, part_spec, part_name, use_count, reason, use_date,
                           f'成套电器保养_{machine_part_name}_{reason}'))
                db.commit()

                return '成功电器保养'

            else:
                # 整体操作
                # 增加电器保养记录 part 外修记录
                print('电器      ', handle)
                cursor.execute('''
                    INSERT INTO `part`.`repair_detail`
                   (`user`,`use_area`, `use_procline`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`remark`)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',
                            '{7}', '{8}','{9}');
                '''.format(user, use_area, use_procline, type, part_spec, part_name, use_count, reason, use_date, f'成套电器外修_{machine_part_name}_{reason}'))
                db.commit()
                return '成功电器外修'

    except Exception as e:
        print(e)
        db.rollback()


def dealwithcount(machine_part_name, area):
    '''修正成套件数'''
    print(f"当前方法名：{sys._getframe().f_code.co_name}")

    print(machine_part_name, '    ', area)
    db = conn.getConn()
    cursor = db.cursor()
    # find count
    sql = f''' select original from machine_parts_detail where machine_part_name='{machine_part_name}' and area='{area}' '''
    cursor.execute(sql)
    rs = cursor.fetchall()
    print(rs)
    print(len(rs))
    if len(rs) > 1:
        tem1 = rs[0][0]
        tem2 = rs[1][0]
        mincount = min(tem1, tem2)
        try:
            print('开始调整成套件数')
            sql1 = f''' update machine_parts_detail set balance={mincount} where machine_part_name ='{machine_part_name}' and area='{area}'  '''
            cursor.execute(sql1)
            db.commit()
            print('调整完成')
            return
        except Exception as e:
            print(e)
            db.rollback()
    else:
        print('不用调整')
        return


def getmachine_part_equipment_rectification(flag: Optional[str] = None,
                                            flag1: Optional[str] = '',
                                            start: Optional[str] = '',
                                            end: Optional[str] = '',
                                            prolince: Optional[str] = '',
                                            area: Optional[str] = ''):
    db = conn.getConn()
    cursor = db.cursor()
    if flag == 'all' and flag1 == '':
        print('获取全部报废记录')
        cursor.execute("select * from machine_parts_equipment_rectification")
        data = cursor.fetchall()
        return data
    elif flag != 'all' and flag1 == '':
        print('获取未确认报废记录')
        cursor.execute('''
          SELECT
            *
          FROM
            machine_parts_equipment_rectification
          WHERE
           useconfirm = ''
                       ''')
        data = cursor.fetchall()
        return data

    if flag1 == '筛选查询':
        sql = 'select * from machine_parts_equipment_rectification where 1=1 '
        print('start')
        print(start)
        starttime = ''
        endtime = ''
        prolince1 = ''
        area1 = ''
        if area != '':
            area1 = " and use_area='{}'".format(area)
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
        sql = "select * from machine_parts_equipment_rectification where 1=1 {0}{1}{2}{3} order by use_date".format(
            starttime, endtime, prolince1, area1)
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return data


def updateMachine_part_equipment_rectification(id: Optional[str] = '',
                                               user: Optional[str] = '',
                                               use_area: Optional[str] = '',
                                               type: Optional[str] = '',
                                               spec: Optional[str] = '',
                                               use_part_name: Optional[str] = '',
                                               use_count: Optional[str] = '',
                                               use_reason: Optional[str] = '',
                                               use_date: Optional[str] = '',
                                               useconfirm: Optional[str] = '',
                                               use_procline: Optional[str] = '',
                                               new_area: Optional[str] = '',
                                               useconfirmdate: Optional[str] = '',
                                               remark: Optional[str] = '',
                                               flag: Optional[str] = '',
                                               flag1: Optional[str] = '',
                                               machine_part_name: Optional[str] = ''):

    print(f"当前方法名：{sys._getframe().f_code.co_name}")

    print('id', id)
    print('user', user)
    print('use_area', use_area)
    print('type', type)
    print('spec', spec)
    print('use_part_name', use_part_name)
    print('use_count', use_count)
    print('use_reason', use_reason)
    print('use_date', use_date)
    print('useconfirm', useconfirm)
    print('use_procline', use_procline)
    print('new_area', new_area)
    print('useconfirmdate', useconfirmdate)
    print('remark', remark)
    print('flag', flag)
    print('flag1', flag)
    print('machine_part_name', machine_part_name)

    # 同步 整改表和库存
    db = conn.getConn()
    cursor = db.cursor()
    print('更新整改表确认')
    sql = f'''
    UPDATE `part`.`machine_parts_equipment_rectification`
        SET
        `useconfirm` = '{useconfirm}',
        `new_area` = '{new_area}',
        `useconfirmdate` = '{useconfirmdate}',
        `remark` = '{remark}'
        WHERE
          `id` = '{id}'
         '''
    cursor.execute(sql)
    db.commit()
    print('更新整改表确认 --完毕')
    # 增加库存 该区域有了就增加库存 没有就新建
    sql1 = f''' SELECT
                  *
                FROM
                  machine_parts_detail
                WHERE
                1=1
                AND type = '{type}'
                AND part_spec = '{spec}'
                AND part_name = '{use_part_name}'
                and area='{new_area}' '''
    cursor.execute(sql1)
    data = cursor.fetchall()
    # 增加
    if len(data) != 0:
        print('成套设备整改')
        print(data)
        count = data[0]
        sql1 = f'''
        UPDATE `part`.`machine_parts_detail`
            SET 
            `part_name` = '{use_part_name}',
            `part_spec` = '{spec}',
            `area` = '{new_area}',
            `balance` = '{use_count}',
            `original` = '{use_count}',
            `remark` = '{remark}',
            `type` = '{type}',
            `machine_part_name` = '{machine_part_name}'
            WHERE
              (`id` = '{id}');

              '''
        cursor.execute(sql1)

        db.commit()

        print('备件数据更新成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    else:

        print('该区域无设备信息 新增')
        mid = pinyin.get_initial(
            f'{machine_part_name}_{new_area}', delimiter="")
        sql2 = f'''INSERT INTO `part`.`machine_parts_detail` (
          `machine_part_name`,
                      `part_name`,
                      `part_spec`,
                      `area`,
                      `balance`,
                      `original`,
                      `remark`,
                      `type`,
                      `machine_part_id`
                              )
                            VALUES
                                ('{machine_part_name}',
                                  '{use_part_name}',
                                  '{spec}',
                                  '{new_area}',
                                  '{use_count}',
                                  '{use_count}',
                                  '',
                                  '{type}',
                                  '{mid}'
                                ); '''
        cursor.execute(sql2)
        db.commit()
    dealwithcount(machine_part_name, new_area)
    return '更新完成'


def machine_parts_update_log(
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
        cursor.execute(f''' INSERT INTO `part`.`log` (`username`, `area`, `spec`, `item_name`, `count`, `create_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'add','成套备件管理');
    ''')
        print("增加记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if flag == 'update':
        cursor.execute(f''' INSERT INTO `part`.`log` ( `username`, `area`, `spec`, `item_name`, `count`, `update_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'update','成套备件管理');
    ''')
        print("更新记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db.commit()
