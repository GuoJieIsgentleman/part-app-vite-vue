
import base64
import hmac
import json
import os
import re
import socket
import sys
import threading
import time
from ast import Str
from msilib.schema import tables
from re import S
from tokenize import tabsize
from typing import Optional, Type

import requests

import Machine_parts_service as Machine_parts
import Machine_procline
import machine_service as machine
import part_procline_service as part_procline
import pymysql

import tooling_manager

import uvicorn
from fastapi import Body, FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from flask import jsonify, request
from pydantic import BaseModel
from pydantic.errors import StrError
from starlette.applications import Starlette
from starlette.types import Message


currentPath = os.getcwd()


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


if os.path.isdir(rf"{currentPath}\templates") == False or os.path.isdir(rf"{currentPath}\static") == False:
    input('''请检查templates和static目录 是否存在
    
            ***---按任意键结束---**
    ''')


app = FastAPI()
origins = [
    "http://localhost", "http://localhost:8080", "http://localhost:5555",
    "http://localhost:8888", "http://localhost:10000"
]

print(os.getcwd())

templates = Jinja2Templates(
    directory=rf"{currentPath}\templates")

app.mount(
    "/static", StaticFiles(directory=rf"{currentPath}\static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def getConn():

    db = pymysql.connect(host='192.168.3.160',
                         port=3306,
                         user='part',
                         passwd='part',
                         db='part',
                         charset='utf8')

    return db


@app.get("/")
def read_root():
    return '{"Hello": "World"}'


usertoken = {}


@app.get("/login")
def read_item(username: str, password: str):
    # 验证并且生成token 返回
    db = getConn()
    cursor = db.cursor()
    cursor.execute(
        "select * from user where 1=1 and  username='{0}' and password='{1}'".
        format(username, password))
    data = cursor.fetchall()
    print(len(data))
    if (len(data) == 0):
        # print(usertoken)
        return data
    # 密码验证成功 生成token 插入数据库
    else:
        usertokenpwd = generate_token('username')
        usertoken[username] = usertokenpwd
        # print(usertoken)
        # print(data)

        userdata = {'username': username, 'token': usertoken[username]}
        return json.dumps(userdata)


class Item(BaseModel):
    id: str
    piker_name: str
    part_spec: str
    area: str
    balance: str
    original: str
    new: str
    new_date: str
    manner: str
    pike: str
    piker: str
    piker_date: str
    piker_procline: str
    pike_reason: str
    confirm_person: str
    remark: str
    filltime: str

# return


@app.get('/getuserecord')
def getuserecord(flag: Optional[str] = None,
                 flag1: Optional[str] = '',
                 start: Optional[str] = '',
                 end: Optional[str] = '',
                 prolince: Optional[str] = '',
                 area: Optional[str] = ''):
    db = getConn()
    print('获取领用记录')
    print(flag)
    cursor = db.cursor()
    if flag == 'all' and flag1 == '':
        print('获取所有领用记录')
        cursor.execute("select * from use_detail")
        data = cursor.fetchall()
        return data
    elif flag != 'all' and flag1 == '':
        print('获取未确认领用记录')
        cursor.execute("select * from use_detail where useconfirm ='' ")
        data = cursor.fetchall()
        return data

    if flag1 == '筛选查询':
        sql = 'select * from use_detail where 1=1 '

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

        sql = "select * from use_detail where 1=1 {0} {1} {2} {3} order by use_date".format(
            starttime, endtime, prolince1, area1)
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return data


@app.get('/deletepart')
def deletepart(id: int):
    db = getConn()
    print('删除备件记录')
    cursor = db.cursor()

    cursor.execute('''delete from
                   part_detail where id='{}'
                   '''.format(id))

    db.commit()
    print('删除完成')
    return '删除成功'


class updateuserecord(BaseModel):
    id: int
    useconfirm: str
    use_count: str
    use_area: str
    use_date: str
    use_part_name: str
    type: str
    spec: str
    user: str
    user_reason: str


@app.get('/getuserecordcount')
def getuserecordcount():
    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                  select count(id)  from use_detail
                   ''')

    data = cursor.fetchall()
    return data


@app.get('/getpartcount')
def getpartcount():
    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                  select count(id)  from part_detail
                   ''')

    data = cursor.fetchall()
    return data


@app.get('/getmaintenancecount')
def getmaintenancecount():
    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                  select count(id)  from maintenance_detail
                   ''')

    data = cursor.fetchall()
    return data


@app.get('/getscrapcount')
def getscrapcount():
    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                  select count(id)  from scrap_detail
                   ''')
    data = cursor.fetchall()
    return data


@app.get('/getrepaircount')
def getrepaircount():
    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                  select count(id)  from repair_detail
                   ''')

    data = cursor.fetchall()
    return data


@app.get('/updateuserecord')
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
    db = getConn()
    print('获取领用记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print('id')
    print(id)
    print('useconfirm')
    print(useconfirm)
    print('use_count')
    print(use_count)
    print('use_area')
    print(use_area)
    print('use_date')
    print(use_date)
    print('use_part_name')
    print(use_part_name)
    print('type')
    print(type)
    print('spec')
    print(spec)
    print('user')
    print(user)
    print('user_reason')
    print(user_reason)
    print('confirm_date')
    print(confirm_date)
    print('flag')
    print(flag)
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
                     UPDATE `part`.`use_detail`
                      SET
                       `useconfirm` = '{0}',
                       `confirm_date` = '{1}',
                       `handle`='{2}'
                      WHERE
                      	(`id` = '{3}');

                     '''.format(useconfirm, confirm_date, handle, id))

        db.commit()
        print('确认班长信息更新成功')

    # 保养记录
    if handle == '保养' and flag == 'confirm':
        print('--------保养--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   INSERT INTO `part`.`maintenance_detail`
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

    if handle == '外修' and flag == 'confirm':
        print('--------外修--------')
        cursor.execute('''
                   INSERT INTO `part`.`repair_detail`
                   ( `user`, `use_area`, `type`, `spec`,
                   `use_part_name`, `use_count`, `user_reason`,
                   `use_date`,`use_procline`)
                   VALUES ('{0}', '{1}', '{2}', '{3}',
                   '{4}', '{5}', '{6}', '{7}','{8}');
          '''.format(user, use_area,
                     type, spec,
                     use_part_name, use_count,
                     '', use_date, use_procline))

        db.commit()
        print('--------外修记录添加完成--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if handle == '报废' and flag == 'confirm':
        print('--------报废--------')
        cursor.execute('''
                   INSERT INTO `part`.`scrap_detail`
                   ( `user`, `use_area`, `type`, `spec`,
                   `use_part_name`, `use_count`, `user_reason`,
                   `use_date`,`use_procline`)
                   VALUES ('{0}', '{1}', '{2}', '{3}',
                   '{4}', '{5}', '{6}', '{7}','{8}');
          '''.format(user, use_area,
                     type, spec,
                     use_part_name, use_count,
                     '', use_date,
                     use_procline))

        db.commit()
        print('--------报废记录添加完成--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if handle == '设备整改' and flag == 'confirm':
        print('--------设备整改--------')
        cursor.execute(f'''
                 INSERT INTO `part`.`part_equipment_rectification` 
( `user`, `use_area`, `type`, `spec`, `use_part_name`, `use_count`, 
`user_reason`, `use_date`, `use_procline`, `remark`, `handle`)
 VALUES ( '{user}', '{use_area}', '{type}', '{spec}', '{use_part_name}', '{use_count}', '设备整改', '{use_date}', '{use_procline}','', '{handle}');
          ''')

        db.commit()
        print('--------设备整改记录添加完成--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return '保存成功！'


# 获取保养记录
@app.get('/getmaintenance')
def getmaintenance(flag: Optional[str] = '',
                   flag1: Optional[str] = '',
                   start: Optional[str] = '',
                   end: Optional[str] = '',
                   prolince: Optional[str] = '',
                   area: Optional[str] = ''):
    db = getConn()

    cursor = db.cursor()

    if flag == 'all' and flag1 == '':
        print('获取所有保养记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute("select * from maintenance_detail")
        data = cursor.fetchall()
        return data
    elif flag != 'all' and flag1 == '':
        print('获取未确认保养记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute(
            "select * from maintenance_detail where useconfirm ='' or maintenanceman=''  ")
        data = cursor.fetchall()
        return data

    if flag1 == '筛选查询':
        sql = 'select * from maintenance_detail where 1=1 '
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
        sql = "select * from maintenance_detail where 1=1 {0}{1}{2}{3}{4} order by use_date".format(
            starttime, endtime, prolince1, area1, msg1)
        print('sql')
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return data


# 获取area

@app.get('/getarea')
def getarea():
    db = getConn()
    print('获取area')
    cursor = db.cursor()
    cursor.execute('''select area from part_detail
                    group by area
                    ''')
    data = cursor.fetchall()
    return data


# 获取外修记录
@app.get('/getrepair')
def getrepair(flag: Optional[str] = None,
              flag1: Optional[str] = '',
              start: Optional[str] = '',
              end: Optional[str] = '',
              prolince: Optional[str] = '',
              area: Optional[str] = ''):
    db = getConn()

    cursor = db.cursor()
    try:
        if flag == 'all' and flag1 == '':
            print('获取所有外修记录')
            cursor.execute("select * from repair_detail")
            data = cursor.fetchall()
            return data
        elif flag != 'all' and flag1 == '':
            print('获取未确认外修记录')
            cursor.execute(
                "select * from repair_detail where useconfirm = '' or applicant='' or tryout='' or receipt='' ")
            data = cursor.fetchall()
            return data

        if flag1 == '筛选查询':
            sql = 'select * from repair_detail where 1=1 '

            starttime = ''
            endtime = ''
            prolince1 = ''
            area1 = ''
            msg1 = ''

            if flag == '是':
                msg1 = " and remark='{}'".format("无库存备件外修")
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
            sql = "select * from repair_detail where 1=1 {0}{1}{2}{3} {4}order by use_date".format(
                starttime, endtime, prolince1, area1, msg1)
            print(sql)
            cursor.execute(sql)
            data = cursor.fetchall()

            return data
    except SystemError:
        print('查询异常')

# 获取报废记录


@app.get('/getscrap')
def getscrap(flag: Optional[str] = None,
             flag1: Optional[str] = '',
             start: Optional[str] = '',
             end: Optional[str] = '',
             prolince: Optional[str] = '',
             area: Optional[str] = ''):
    db = getConn()

    cursor = db.cursor()
    if flag == 'all' and flag1 == '':
        print('获取全部报废记录')
        cursor.execute("select * from scrap_detail")
        data = cursor.fetchall()
        return data
    elif flag != 'all' and flag1 == '':
        print('获取未确认报废记录')
        cursor.execute('''
          SELECT
            *
          FROM
            scrap_detail
          WHERE
            scrapconfirm = ''
          OR applyformconfirm = ''
          OR applicantman = ''
          OR useconfirm = ''

                       ''')
        data = cursor.fetchall()
        return data

    if flag1 == '筛选查询':
        sql = 'select * from repair_detail where 1=1 '
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
        sql = "select * from scrap_detail where 1=1 {0}{1}{2}{3} order by use_date".format(
            starttime, endtime, prolince1, area1)
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return data


# 备件设备整改获取
@app.get('/getpart_equipment_rectification')
def getscrap(flag: Optional[str] = None,
             flag1: Optional[str] = '',
             start: Optional[str] = '',
             end: Optional[str] = '',
             prolince: Optional[str] = '',
             area: Optional[str] = ''):
    db = getConn()

    cursor = db.cursor()
    if flag == 'all' and flag1 == '':
        print('获取全部报废记录')
        cursor.execute("select * from part_equipment_rectification")
        data = cursor.fetchall()
        return data
    elif flag != 'all' and flag1 == '':
        print('获取未确认报废记录')
        cursor.execute('''
          SELECT
            *
          FROM
            part_equipment_rectification
          WHERE
           useconfirm = ''

                       ''')
        data = cursor.fetchall()
        return data

    if flag1 == '筛选查询':
        sql = 'select * from part_equipment_rectification where 1=1 '
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
        sql = "select * from part_equipment_rectification where 1=1 {0}{1}{2}{3} order by use_date".format(
            starttime, endtime, prolince1, area1)
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

        return data


@app.get('/updatemachine_equipment_rectification')
def updatemachine_equipment_rectification(id: Optional[str] = '',
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
                                          flag1: Optional[str] = ''):

    return machine.updatemachine_equipment_rectification(id,
                                                         user,
                                                         use_area,
                                                         type,
                                                         spec,
                                                         use_part_name,
                                                         use_count,
                                                         use_reason,
                                                         use_date,
                                                         useconfirm,
                                                         use_procline,
                                                         new_area,
                                                         useconfirmdate,
                                                         remark,
                                                         flag,
                                                         flag1)


@app.get('/getinspectionrecord')
def getinspectionrecord():
    db = getConn()
    print('获取巡检记录')
    cursor = db.cursor()
    cursor.execute("select * from inspectionrecord")

    data = cursor.fetchall()
    return data


# adduserecord


# 获取报废记录
@app.get('/updatepart')
def updatpart(
        username: Optional[str] = None,
        id: Optional[int] = None,
        part_name: Optional[str] = None,
        part_spec: Optional[str] = None,
        area: Optional[str] = None,
        type: Optional[str] = None,
        new_balance: Optional[int] = None,
        new_original: Optional[int] = None,
        connection: Optional[str] = None,
        flag: Optional[str] = None):
    db = getConn()
    print('更改备件结存')
    cursor = db.cursor()

    if flag == '巡检区域更换':
        updateSql = f''' update  part_detail  set area='{area}'  where id={id} '''
        cursor.execute(updateSql)
        db.commit()
        print('更新区域完成')
        return '更新完成'

    print('username', username)
    print('id', id)
    print('part_name', part_name)
    print('part_spec', part_spec)
    print('area', area)
    print('type', type)
    print('new_balance', new_balance)
    print('connection', connection)

    if id != None:
        print('--更改备件信息--')
        try:
            updateSql = '''
                    UPDATE `part`.`part_detail`
                      SET `balance` = '{0}',
                          `original` = '{1}',
                          `connection` = '{2}',
                          `area`='{3}',
                          `part_spec`='{5}'
                      WHERE
                        (`id` = '{4}')
                   
                    '''.format(new_balance, new_original, connection,
                               area, id, part_spec)

            print(updateSql)
            cursor.execute(updateSql)
            db.commit()
            part_update_log(username, part_spec, part_name,
                            area, new_balance, "update")
            cursor.execute('''
                select * from   part_detail

                where id={}

                           '''.format(id))
            data = cursor.fetchall()

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


@app.post('/adduserecord')
def adduserecord(userecordform: Optional[userecordform] = None):

    print('增加领用记录')

    print(f"当前方法名：{sys._getframe().f_code.co_name}")
    print('增加领用记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    db = getConn()
    cursor = db.cursor()

    # 增加领用记录 并且 减去库存数据

    # 增加领用记录 并且 减去库存数据

    print(userecordform.user)
    print(userecordform.area)
    print(userecordform.type)
    print(userecordform.spec)
    print(userecordform.part_name)
    print(userecordform.use_count)
    print(userecordform.reason)
    print(userecordform.use_date)
    print(userecordform.confirm)
    print(userecordform.use_procline)

    print(userecordform.handle)

    print(userecordform.flag)

    cursor.execute(
        '''select *  from  part_detail where area like '%{0}%'and part_spec='{1}' and type='{2}' and part_name='{3}'
    '''.format(userecordform.area, userecordform.spec, userecordform.type,
               userecordform.part_name))
    data = cursor.fetchall()
    print(data[0])

    print('-------更新件数 ---------' +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(data[0][4])

    count = data[0][4]
    cursor.execute('''update part_detail set balance={0}-{5}
        where part_name='{1}' and part_spec='{2}' and area like '%{3}%' and type='{4}'
    '''.format(count, userecordform.part_name, userecordform.spec,
               userecordform.area, userecordform.type,
               userecordform.use_count))
    data = cursor.fetchall()
    db.commit()

    print('--------添加记录--------' +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 总记录
    cursor.execute('''
                   INSERT INTO `part`.`use_detail`
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

    print('--------{}领用记录添加完成--------'.format(userecordform.handle) +
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print('--------保养--------'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # 保养记录
    if userecordform.handle == '保养' and userecordform.flag == 'confirm':

        cursor.execute('''
                   INSERT INTO `part`.`maintenance_detail`
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

    if userecordform.handle == '外修' and userecordform.flag == 'confirm':
        print('--------外修-------- ' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   INSERT INTO `part`.`repair_detail`
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
        print('--------外修记录添加完成--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if userecordform.handle == '报废' and userecordform.flag == 'confirm':
        print('--------报废--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   INSERT INTO `part`.`scrap_detail`
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
        print('--------报废记录添加完成--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if userecordform.handle == '设备整改' and userecordform.flag == 'confirm':
        print('--------设备整改--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   INSERT INTO `part`.`equipment_rectification`
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
        print('--------设备整改记录添加完毕--------' +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    return '添加成功'


class maintenanc(BaseModel):
    id: int
    spec: str
    type: str
    use_area: str
    use_count: str
    use_date: str
    use_part_name: str
    use_reason: str
    # useconfirm: str
    # user: str


#  use_count: str, use_date: str, use_part_name: str,
#                       user_reason: str, useconfirm: str, user: str
@app.get('/updatemaintenance')
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
                      flag: Optional[str] = '',
                      machine_part_name: Optional[str] = ''
                      ):
    print('更新保养记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    db = getConn()
    cursor = db.cursor()

    print('maintenanceman')
    print(maintenanceman)
    print(maintenance_date)

    # 成套
    if scrap == '成套':
        print('处理成套设备')

        # 先查区域有没有
        cursor.execute(f'''
                   select count(*) from machine_parts_detail where area ='{new_area}' and part_name='{use_part_name}' ''')

        rs = cursor.fetchone()
        if rs[0] > 0:

            # 如果有 就update

            # 确定成套整套件数 比较两个balance 大小  以小的为准去更新

            cursor.execute(f'''
                    UPDATE `part`.`machine_parts_detail`
                  SET 
                  `balance` = balance+{use_count},
                  `original` = '9',
                  
                  WHERE
                      part_spec='{spec}'
                    and part_name='{use_part_name}'
                    and area='{new_area}'
                       ''')
            db.commit()
        else:
            cursor.execute(f'''
                   INSERT INTO `part`.`machine_parts_detail` (`part_name`,`part_spec`,`area`,`balance`,`original`,`remark`,`type`,
	`partimgsrc`,`connection`,`type1`,`machine_part_name`
)
VALUES	(	'{use_part_name}',	'{spec}','{new_area}',	'{use_count}','{use_count}','',	'{type}',	'',	'',	'电器',	'{machine_part_name}'
	);
                       ''')
            db.commit()
        # 没有就add
        # 修正成套
        Machine_parts.dealwithcount(machine_part_name, use_area)
        return '处理成套成功'

    if '无库存' in flag:
        print('flag')
        print(flag)
        print('scrap')
        print(scrap)
        print('无库存备件更新记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                     UPDATE `part`.`maintenance_detail`
                      SET
                       `useconfirm` = '{0}',`useconfirmdate`='{1}',`handle`='{3}',`new_area`='{4}'
                      WHERE  `id` = {2}

                       '''.format(useconfirm, useconfirmdate, id, scrap, new_area))
        db.commit()

        if scrap == '外修':

            cursor.execute('''
                   INSERT INTO `part`.`repair_detail`
                  (`user`, `use_area`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`remark`,`use_procline`)
                  VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}',
                          '{6}', DATE_FORMAT('{7}','%Y-%m-%d %H:%i:%s'),'{8}','{9}');
    '''.format(user, use_area, type, spec, use_part_name, use_count, '', use_date, flag+"转外修", use_procline))
            db.commit()
            return '确认完成 新增外修记录'

        if scrap == '报废':
            cursor.execute('''
                   INSERT INTO `part`.`scrap_detail`
                   ( `user`, `use_area`, `type`, `spec`,
                   `use_part_name`, `use_count`, `remark`,
                   `use_date`,`use_procline`)
                   VALUES ('{0}', '{1}', '{2}', '{3}',
                   '{4}', '{5}', '{6}', '{7}', '{8}');
          '''.format(user, use_area, type, spec, use_part_name, use_count,
                     '无库存备件保养转报废', maintenance_date, use_procline))

            db.commit()
            return '确认完成 新增报废记录'
        return '更新完成'

    # 报废流程

    if scrap == '报废' and new_area == '' and flag == '':
        # 增加报废记录
        print('增加报废记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   INSERT INTO `part`.`scrap_detail`
                   ( `user`, `use_area`, `type`, `spec`,
                   `use_part_name`, `use_count`, `user_reason`,
                   `use_date`, `useconfirm`,`use_procline`)
                   VALUES ('{0}', '{1}', '{2}', '{3}',
                   '{4}', '{5}', '{6}', '{7}', '{8}','{9}');
          '''.format(user, use_area, type, spec, use_part_name, use_count,
                     '保养报废', maintenance_date, useconfirm, use_procline))

        db.commit()
        cursor.execute('''
                     UPDATE `part`.`maintenance_detail`
                      SET
                       `useconfirm` = '{0}',`useconfirmdate`='{1}',`handle`='{3}'
                      WHERE  `id` = {2}

                       '''.format(useconfirm, useconfirmdate, id, scrap))
        db.commit()
        print('更新保养确认班长名成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('增加报废记录成功')
        return '报废成功'

    if useconfirm == '' and maintenanceman != '' and flag != '无库存备件保养':

        print('更新保养人'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        cursor.execute('''

                     UPDATE `part`.`maintenance_detail`
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

        if scrap == "外修":
            print('转换到外修'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            cursor.execute('''
                   INSERT INTO `part`.`repair_detail`
                  (`user`, `use_area`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`use_procline`)
                  VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}',
                          '{6}', DATE_FORMAT('{7}','%Y-%m-%d %H:%i:%s'),'{8}');
    '''.format(user, use_area, type, spec, use_part_name, use_count, '', use_date, use_procline))
            db.commit()

            # return '增加外修成功'
        # 保养件数
        # 如果搁置区域有 就加1 否则就新增一条

        # 增加最新搁置区域
        else:
            cursor.execute('''
              SELECT
                  *
                FROM
                  part_detail
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

                cursor.execute('''update part_detail set balance={0}+{5}
              where part_name='{1}' and part_spec='{2}' and area='{3}' and type='{4}'
        '''.format(count, use_part_name, spec, use_area, type, use_count))

                db.commit()
                print('保养数据更新成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            else:

                print('该区域无设备信息 新增')
                cursor.execute('''
                                INSERT INTO `part`.`part_detail` (
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
                  UPDATE `part`.`maintenance_detail`
                    SET
                    `useconfirm` = '{0}',`new_area`='{1}',`useconfirmdate`='{3}',`handle`='{4}'
                    WHERE  `id` = {2}

                    '''.format(useconfirm, new_area, id, useconfirmdate, scrap))
        db.commit()
        print('更新保养确认班长名成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return '成功！'


# 多余留着
@app.get('/addmaintenance')
def addmaintenance(user: str, area: str, type: str, spec: str, part_name: str,
                   use_count: str, reason: str, use_date: str, confirm: str,
                   flag: Optional[str] = None):

    print('增加保养记录')

    db = getConn()
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
                    INSERT INTO `part`.`maintenance_detail`
                    (`user`, `use_procline`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`remark`)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',
                           '{7}', '{8}');
      '''.format(user, area, type, spec, part_name, use_count, reason, use_date,
                 flag))
        db.commit()
        # 开始增加记录

        return '添加成功'


@app.get('/addrepair')
def addrepair(user: str, area: str, type: str, spec: str, part_name: str,
              use_count: str, reason: str, use_date: str, confirm: str,
              flag: Optional[str] = None):
    print('增加外修记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    db = getConn()
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
    if flag == '无库存备件外修':

        cursor.execute('''
                    INSERT INTO `part`.`repair_detail`
                    (`user`, `use_procline`,`type`, `spec`, `use_part_name`,`use_count`, `user_reason`, `use_date`,`remark`)
                    VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',
                            '{7}', '{8}');
      '''.format(user, area, type, spec, part_name, use_count, reason, use_date,
                 flag))
        db.commit()
        # 开始增加记录

        return '添加成功'


class updaterepair(BaseModel):
    id: int
    useconfirm: Optional[str] = None
    use_count: Optional[str] = None
    use_area: Optional[str] = None
    use_date: Optional[str] = None
    use_part_name: Optional[str] = None
    use_reason: Optional[str] = None
    type: Optional[str] = None
    spec: Optional[str] = None
    new_area: Optional[str] = None
    applicant: Optional[str] = None
    receipt: Optional[str] = None
    tryout: Optional[str] = None


@app.get('/updaterepair')
def updaterepair(id: int,
                 user: Optional[str] = '',
                 scrap: Optional[str] = '',
                 useconfirm: Optional[str] = '',
                 use_count: Optional[str] = '',
                 use_area: Optional[str] = '',
                 use_date: Optional[str] = '',
                 use_part_name: Optional[str] = '',
                 use_reason: Optional[str] = '',
                 type: Optional[str] = '',
                 spec: Optional[str] = '',
                 new_area: Optional[str] = '',
                 applicant: Optional[str] = '',
                 receipt: Optional[str] = '',
                 tryout: Optional[str] = '',
                 applicantdate: Optional[str] = '',
                 receiptdate: Optional[str] = '',
                 tryoutdate: Optional[str] = '',
                 useconfirmdate: Optional[str] = '',
                 temporary_area: Optional[str] = '',
                 remark: Optional[str] = '',
                 use_procline: Optional[str] = '',
                 flag: Optional[str] = '',
                 machine_part_name: Optional[str] = ''):
    # 更新试机人

    print('id')
    print(id)
    print('useconfirm')
    print(useconfirm)
    print('use_count')
    print(use_count)
    print('use_area')
    print(use_area)
    print('use_date')
    print(use_date)
    print('use_part_name')
    print(use_part_name)
    print('use_reason')
    print(use_reason)
    print('type')
    print(type)
    print('spec')
    print(spec)
    print('new_area')
    print(new_area)
    print('applicant')
    print(applicant)
    print('receipt')
    print(receipt)
    print('tryout')
    print(tryout)

    print('scrap')
    print(scrap)
    print('applicantdate')
    print(applicantdate)
    print('receiptdate')
    print(receiptdate)
    print('receiptdate')
    print(receiptdate)
    print('flag')
    print(flag)
    db = getConn()
    cursor = db.cursor()
    print('无库存备件' in flag)
    if '无库存备件' in flag:

        print('更新无库存备件外修记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   UPDATE `part`.`repair_detail`
                    SET
                     `useconfirm` = '{0}',`useconfirmdate`='{2}',`handle`='{3}',`new_area`='{4}',`remark`='{5}'
                    WHERE  `id` = {1}
                     '''.format(useconfirm, id,  useconfirmdate, scrap, new_area, scrap))
        db.commit()
        print('更新无库存备件完成')

        if scrap == '报废':
            print('无库存备件外修增加报废记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            cursor.execute('''
                   INSERT INTO `part`.`scrap_detail`
                   ( `user`, `use_area`, `type`, `spec`,
                   `use_part_name`, `use_count`, `remark`,
                   `use_date`,`use_procline`)
                   VALUES ('{0}', '{1}', '{2}', '{3}',
                   '{4}', '{5}', '{6}', '{7}','{8}');
          '''.format(user, use_area, type, spec, use_part_name, use_count,
                     '无库存备件外修转报废', use_date, use_procline))

            db.commit()
            return '无库存备件外修增加报废记录成功'
        return '更新无库存备件外修记录'

    if scrap == '报废' or scrap == '成套报废':
        # 增加报废记录
        print('外修增加报废记录'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                   INSERT INTO `part`.`scrap_detail`
                   ( `user`, `use_area`, `type`, `spec`,
                   `use_part_name`, `use_count`, `user_reason`,
                   `use_date`,`use_procline`)
                   VALUES ('{0}', '{1}', '{2}', '{3}',
                   '{4}', '{5}', '{6}', '{7}','{8}');
          '''.format(user, use_area, type, spec, use_part_name, use_count,
                     '外修报废', use_date, use_procline))

        db.commit()
        cursor.execute('''
                     UPDATE `part`.`repair_detail`
                      SET
                       `useconfirm` = '{0}',`applicantdate`='{2}',`receiptdate`='{3}',
                       `tryoutdate`='{4}',`useconfirmdate`='{5}',`remark`='{6}',`handle`='{7}'
                      WHERE  `id` = {1}

                       '''.format(useconfirm, id, applicantdate, receiptdate, tryoutdate, useconfirmdate, remark, scrap))
        db.commit()
        print('更新外修确认班长名成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('增加报废记录成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return '报废成功'
    if scrap == '成套不报废':
      # 增加成套 判断是否在这个区域有 如果有 就新增 instert  没有就 update

        cursor = db.cursor()
        sql = f''' select count(id) from machine_parts_detail where machine_part_name='{machine_part_name}' and area='{new_area}' '''

        cursor.execute(sql)
        rs = cursor.fetchone()
        if rs[0] > 0:
            # update
            sql1 = f''' update machine_parts_detail set original=original+{use_count} where machine_part_name='{machine_part_name}' and area='{new_area}' '''

            cursor.execute(sql1)
            db.commit()
            print('更新成套库存完成')
        else:
            sql2 = f''' INSERT INTO `part`.`machine_parts_detail` ( `part_name`, `part_spec`, `area` , `original`, `remark`, `type`, `partimgsrc`, `connection`, `type1`, `machine_part_name`, `machine_part_id`) 
          VALUES ( '{use_part_name}', '{spec}', '{new_area}', '{use_count}', '{remark}', '{type}', '', '', '电器', '{machine_part_name}', '{id}');
 '''
            cursor.execute(sql2)
            db.commit()
            print('新增成套库存完成')

    # 更新 申请人 收货人  试机人

    if applicant != '' and receipt == '':
        print('更新申请人---'+time.strftime("%Y-%m-%d %H:%M:%S",
              time.localtime()) + applicant)
        cursor.execute('''
            UPDATE `part`.`repair_detail`
              SET
              `applicant` = '{0}',
              `applicantdate`='{2}'
              WHERE
                (`id` = '{1}');
                    '''.format(applicant, id, applicantdate))

        db.commit()
        print('更新申请人成功---'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    elif applicant != '' and receipt != '' and tryout == '':
        print('更新收货人---' + receipt)
        cursor.execute('''
            UPDATE `part`.`repair_detail`

              SET
              `receipt` = '{0}',
              `receiptdate`='{2}',
              `temporary_area`='{3}'
              WHERE
                (`id` = '{1}');
                    '''.format(receipt, id, receiptdate, temporary_area))

        db.commit()
        print('更新收货人成功---'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    elif applicant != '' and receipt != '' and tryout != '' and useconfirm == '':
        print('更新试机人---' + tryout)
        cursor.execute('''
            UPDATE `part`.`repair_detail`
              SET
              `tryout` = '{0}',
              `tryoutdate`='{2}'
              WHERE
                (`id` = '{1}');
                    '''.format(tryout, id, tryoutdate))

        db.commit()
        print('更新试机人成功---'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    elif applicant != '' and receipt != '' and tryout != '' and useconfirm != '' and new_area != '' and flag == '':

        # 更新确认人班长名
        # 更新完 进行增加到库存列表中

        # 先查询 有就更新 没有 就新增

        print('更新确认班长以及更新库存-----' + useconfirm)
        cursor.execute('''
           SELECT
              	*
              FROM
              	part_detail
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
            print('外修查询出来的数据'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print(data)

            count = data[0][4]
            print(count)
            cursor.execute('''update part_detail set balance={0}+{5}
            where part_name='{1}' and part_spec='{2}' and area='{3}' and type='{4}'
      '''.format(count, use_part_name, spec, use_area, type, use_count))

            db.commit()
            print('外修----区域数据更新成功' +
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        else:

            print('外修----该区域无设备信息 新增' +
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            cursor.execute('''
                              INSERT INTO `part`.`part_detail` (
                            	`part_name`,
                            	`part_spec`,
                            	`area`,
                            	`balance`,
                            	`original`,
                            	`type`
                            )
                           VALUES
                            	(
                            		'{0}',
                            		'{1}',
                            		'{2}',
                            		'{3}',
                            		'{4}',
                            		'{5}'
                            	);
                           '''.format(use_part_name, spec, new_area, use_count,
                                      use_count, type))
            db.commit()
            print('更新新增区域 以及库存成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # 更新确认人
        print('更新确认人'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                     UPDATE `part`.`repair_detail`
                      SET
                       `useconfirm` = '{0}',`new_area`='{1}',
                       `useconfirmdate`='{3}',`remark`='{4}',`handle`='{5}'
                      WHERE  `id` = {2}

                       '''.format(useconfirm, new_area, id, useconfirmdate, remark, scrap))
        db.commit()
        print('更新确认人成功'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:

        return '错误'

    return '成功！'


class updatescrap(BaseModel):
    id: int
    user: str
    use_area: str
    type: str
    spec: str
    use_part_name: str
    use_count: str
    use_reason: str
    use_date: str
    scrapconfirm: str
    selectOption: str
    selectOptiondate: str
    applyformconfirm: str
    applicantman: str


@app.get('/updatescrapselectOption')
def updatescrapselectOption(id: int, selectOption: Optional[int] = None):

    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
             UPDATE `part`.`scrap_detail`
            SET `selectOption` = '{}'
            WHERE
            	(`id` = '5');
                   ''')


@app.get('/updatescrap')
def updatescrap(id: int,
                add_count: Optional[int] = 0,
                received: Optional[int] = 0,
                new_area: Optional[str] = '',
                user: Optional[str] = '',
                use_area: Optional[str] = '',
                type: Optional[str] = '',
                spec: Optional[str] = '',
                use_part_name: Optional[str] = '',
                use_count: Optional[str] = '',
                use_reason: Optional[str] = '',
                use_date: Optional[str] = '',
                scrapconfirm: Optional[str] = '',
                selectOption: Optional[str] = '',
                selectOptiondate: Optional[str] = '',
                applyformconfirm: Optional[str] = '',
                applyformconfirmdate: Optional[str] = '',
                applicantman: Optional[str] = '',
                useconfirm: Optional[str] = '',
                scrapconfirmdate: Optional[str] = '',
                applicantdate: Optional[str] = '',
                remark: Optional[str] = '',
                useconfirmdate: Optional[str] = '',
                flag: Optional[str] = '',
                flag1: Optional[str] = ''
                ):

    print('id')
    print(id)
    print('user')
    print(user)
    print('type')
    print(type)
    print('spec')
    print(spec)
    print('use_part_name')
    print(use_part_name)
    print('use_count')
    print(use_count)
    print('use_reason')
    print(use_reason)
    print('use_date')
    print(use_date)
    print('scrapconfirm')
    print(scrapconfirm)
    print('selectOption')
    print(selectOption)
    print('selectOptiondate')
    print(selectOptiondate)
    print('applyformconfirm')
    print(applyformconfirm)
    print('applicantman')
    print(applicantman)

    print('received')
    print(received)

    print('new_area')
    print(new_area)

    print('add_count')
    print(add_count)
    print('flag')
    print(flag)
    # 更新备件领用逻辑
    db = getConn()
    cursor = db.cursor()

    if "无库存" in flag1:
        # 只是更新确认人
        print('无库存备件不补只更新班长名字'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(useconfirm)
        print(remark)
        print(useconfirmdate)
        print(id)
        cursor.execute('''
                     UPDATE `part`.`scrap_detail`
                      SET
                       `useconfirm` = '{0}',`user_reason`='{2}',`useconfirmdate`='{3}',`new_area`='{4}'
                      WHERE  `id` = '{1}'
                       '''.format(useconfirm, id, remark, useconfirmdate, new_area))
        db.commit()
        print('不补只更新班长名字完成'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return '更新成功'

    # 条件判断
    if flag == '报废申请人确认信息' and applyformconfirm != '':
        print('更新报废申请确认人'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                       UPDATE `part`.`scrap_detail`
                        SET
                         `applyformconfirm` = '{0}',
                         `applyformconfirmdate`='{2}'


                        WHERE
                        	(`id` = '{1}');
                     '''.format(applyformconfirm, id, applyformconfirmdate))
        db.commit()
        print('更新报废申请确认人完成'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return '更新成功'
    if flag == '报废件确认信息' and scrapconfirm != '':
        print('更新报废班长确认人'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        cursor.execute('''
                       UPDATE `part`.`scrap_detail`
                        SET
                         `scrapconfirm` = '{0}',
                          `scrapconfirmdate`='{2}'
                        WHERE
                        	(`id` = '{1}');

                     '''.format(scrapconfirm, id, scrapconfirmdate))
        db.commit()
        print('更新报废班长确认人完成'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return '更新成功'
    if flag == '补件申请人' and applicantman != '':
        print('更新补件申请确认人')
        cursor.execute('''
                       UPDATE `part`.`scrap_detail`
                        SET
                         `applicantman` = '{0}',
                        `applicantdate`='{2}',
                        `received`='{3}',
                        `selectOption`='{4}'
                        WHERE
                        	(`id` = '{1}');

                     '''.format(applicantman, id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), add_count, selectOption))
        db.commit()
        print('更新补件申请确认人及补件件数完成'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return '更新成功'
    if flag == '到件确认人' and useconfirm != '':
        print('更新班长确认人'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        # 先增加库存
        # 然后更新确认班长
        if received != '' and selectOption == '补':
            print('更新确认班长以及更新库存-----'+time.strftime("%Y-%m-%d %H:%M:%S",
                  time.localtime()) + useconfirm)

            cursor.execute('''
                 SELECT
                    	*
                    FROM
                    	part_detail
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
                print('补件区域查询出来的数据' +
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                print(data)
                count = data[0][4]

                cursor.execute('''update part_detail set balance={0}+{5}
                  where part_name='{1}' and part_spec='{2}' and area='{3}' and type='{4}'
            '''.format(count, use_part_name, spec, use_area, type, received))

                db.commit()

                print('报废补件----区域数据更新成功' +
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            else:

                print('报废补件----该区域无设备信息 新增' +
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                cursor.execute('''
                                    INSERT INTO `part`.`part_detail` (
                                  	`part_name`,
                                  	`part_spec`,
                                  	`area`,
                                  	`balance`,
                                  	`original`,
                                  	`type`
                                  )
                                 VALUES
                                  	(
                                  		'{0}',
                                  		'{1}',
                                  		'{2}',
                                  		'{3}',
                                  		'{4}',
                                  		'{5}'
                                  	);
                                 '''.format(use_part_name, spec, new_area,
                                            received, received, type))
                db.commit()
                print('更新新增区域 以及库存成功' +
                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # 更新确认人
            print('更新确认人')
            cursor.execute('''
                           UPDATE `part`.`scrap_detail`
                            SET
                             `useconfirm` = '{0}',`new_area`='{1}',`remark`='{3}',`useconfirmdate`='{4}'
                            WHERE  `id` = {2}

                             '''.format(useconfirm, new_area, id, remark, useconfirmdate))
            db.commit()
        else:
            print('不补只更新班长名字'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print(useconfirmdate)
            cursor.execute('''
                           UPDATE `part`.`scrap_detail`
                            SET
                             `useconfirm` = '{0}',`remark`='{2}',`useconfirmdate`='{3}'
                            WHERE  `id` = {1}

                             '''.format(useconfirm, id, remark, useconfirmdate))
            db.commit()

            print('不补只更新班长名字完成'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    return '成功！'


@app.get('/update')
def update(ruleForm: str):
    print(ruleForm)
    ruleForm1 = json.loads(ruleForm)

    print(ruleForm1['new_date'])

    # 更新备件领用逻辑

    # db = getConn()
    # cursor = db.cursor()
    # cursor.execute("".format(username,  password))
    # data = cursor.fetchall()
    # getConn()
    return '收到'


@app.get('/addparts')
def addparts(
        username: Optional[str] = None,
        part_name: Optional[str] = None,
        part_spec: Optional[str] = None,
        area: Optional[str] = None,
        balance: Optional[int] = 0,
        remark: Optional[str] = None,
        type: Optional[str] = None):

   # 增加备件

   # 如果增加的区域有相关的备件 就直接合并到这个区域

    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                INSERT INTO `part`.`part_detail` (

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
    part_update_log(username, part_spec, part_name, area, balance, "add")
    cursor.execute('''
                   select id from  part_detail where part_name='{0}'
                   and part_spec='{1}' and area='{2}' and type='{3}'
                   '''.format(part_name, part_spec, area, type))

    data = cursor.fetchall()
    res = {'msg': '添加成功', 'id': data[0][0]}

    return res

# 获取电器机修件


@app.get('/getPart_proclinedetail')
def getPart_proclinedetail(procline: Optional[str] = ""):
    return part_procline.getPart_proclinedetail(procline)


@app.get('/getProclinePartTypes')
def getProclinePartTypes():
    return part_procline.getProclinePartTypes()


@app.get('/getPart_proclineSummary')
def getPart_proclineSummary():
    return part_procline.getPart_proclineSummary()


@app.get('/getPart_contrast')
def getPart_contrast(machineType: Optional[str] = ""):
    print('machineType', machineType)
    return part_procline.getPart_contrast(machineType)


@app.post('/Part_procline_detail_uploadfile')
async def Part_procline_detail_uploadfile(flag: Optional[str] = None, imgid: Optional[str] = None, time1:  Optional[str] = None, file: UploadFile = File(...)):

    return await part_procline.create_upload_file(flag, imgid, time1, file)

# 添加产线使用件


@app.get('/addPart_procline_detail')
def addPart_procline_detail(procline: Optional[str] = None, part_name: Optional[str] = None, part_spec: Optional[str] = None, area: Optional[str] = None, type: Optional[str] = None, username: Optional[str] = None):
    return part_procline.addPart_procline_detail(procline, part_name, part_spec, area, type, username)


@app.get('/deletePart_procline_detail')
def deletePart_procline_detail(id: Optional[str] = None, username: Optional[str] = None):
    print("进入删除方法")
    return part_procline.deletePart_procline_detail(id, username)


@app.get('/updatePart_procline_detail')
def updatePart_procline_detail(id: Optional[str] = None, procline: Optional[str] = None, part_name: Optional[str] = None, part_spec: Optional[str] = None, area: Optional[str] = None, type: Optional[str] = None, username: Optional[str] = None):
    return part_procline.updatepart_procline_detail(id, procline, part_name, part_spec, area, type, username)


@app.get('/getrolelist')
def getrolelist():

    # 增加备件
    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                    select * from user_role
                  ''')
    data = cursor.fetchall()

    return data


@app.get('/adduser')
def adduser(
    username: str,
    password: str,
    role: str,
):

    print(username)
    print(password)
    print(role)

    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                    select * from user
                    where 1=1
                    and username='{0}'

                  '''.format(username))
    data = cursor.fetchall()
    if len(data) != 0:
        return '用户名已存在'
    else:

        cursor.execute('''
                     INSERT INTO `part`.`user` (

                        	`username`,
                        	`password`,
                        	`role`
                        )
                        VALUES
                        	(

                        		'{0}',
                        		'{1}',
                        		'{2}'
                        	);
                     '''.format(username, password, role))
        data = cursor.fetchall()
        db.commit()
        return '添加成功'


# 获取区域
@app.get('/getusearea')
def getusearea():
    # 获取领用区域
    print('获取区域'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db = getConn()
    cursor = db.cursor()
    cursor.execute('''
                   select case when left (area, 2)='方镀' then left (area, 6)  
when left (area, 2)='南污' then left (area, 5)  
when left (area, 2)='值班' then left (area, 5)  
when left (area, 2)='圆镀' then left (area, 6)  
else  '其他'
end areas
from part_detail
group by areas

''')

    data = cursor.fetchall()
    print(data)
    return data


# 获取类型
@app.get('/gettype')
def gettype(area: Optional[str] = None):
    # 获取获取类型
    db = getConn()
    cursor = db.cursor()

    if area == None:
        sql = "select type from part_detail    group by type"
        cursor.execute(sql
                       )
        data = cursor.fetchall()
        print(data)
        return data
    else:
        sql = "select type from part_detail where area like'{0}%'group by type".format(
            area)
        cursor.execute(sql
                       )
        data = cursor.fetchall()
        print(data)
        return data


# 获取name
@app.get('/getpartname')
def getpartname(type: Optional[str] = None, area: Optional[str] = None):
    # 获取获取类型
    db = getConn()
    cursor = db.cursor()

    print(type)

    if area == None:
        cursor.execute(
            "select * from part_detail where type='{0}'"
            .format(type))
        data = cursor.fetchall()
        print('备件管理查询'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(data)
        return data
    else:
        cursor.execute(
            "select * from part_detail where type = '{0}' and area like '%{1}%'"
            .format(type, area))
        data = cursor.fetchall()
        print('添加领用查询'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(data)
        return data


@app.get('/getbalance')
def getbalance(type: Optional[str] = None,
               area: Optional[str] = None,
               spec: Optional[str] = None,
               part_name: Optional[str] = None):
    # 获取获取类型
    db = getConn()
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
        "select * from part_detail where area like '%{0}%' and type='{1}' and part_spec='{2}' and part_name='{3}' "
        .format(area, type, spec, part_name))
    data = cursor.fetchall()

    print('getbalance'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print(data)
    return data


# 获取型号e
@app.get('/getspesc')
def getspesc(type: Optional[str] = None,  use_part_name: Optional[str] = None, area: Optional[str] = None):
    # 获取获取类型
    db = getConn()
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
            "select * from part_detail where 1=1 and type='{0}' and part_name='{1}' and area like '%{2}%'  ".format(
                type, use_part_name, area))
        data = cursor.fetchall()
        print(data)
        return data


# 获取备件列表
@app.get('/getparts')
def getmenus(currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0):

    # 每页多少条数据 默认10
    print(currentpagecount)
    # 传过来取多少页的数据
    print(pagesize)
    db = getConn()
    print('获取备件列表'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()

    # 查询多少条
    cursor.execute("select count(id) from part_detail")
    data = cursor.fetchall()

    pages = 0
    # 查询分多少页
    if currentpagecount != 0:
        total = data[0][0]
        tem = total % currentpagecount
        tem1 = total // currentpagecount

        # 算出总页数
        pages = tem if tem == 0 else tem1+1

    start = currentpagecount*(pagesize-1)
    end = currentpagecount
    print('start')
    print(start)
    print('end')
    print(end)
    print(pages)
    print(data[0][0])

    cursor.execute(
        "select * from part_detail order by id  limit {0},{1}".format(start, end))
    data1 = cursor.fetchall()

    res = {
        'total': data[0][0],
        'data1': data1,
        'pages': pages
    }

    return res


# 查询

@app.get('/selectpart')
def selectpart(
    part_spec: Optional[str] = "",
    part_name: Optional[str] = "",
    area: Optional[str] = "",
    type: Optional[str] = "",

):
    db = getConn()
    print('查询备件'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()
    part_spec1 = ''
    part_name1 = ''
    area1 = ''
    type1 = ''
    if part_spec != "":
        part_spec1 = f''' and part_spec like '%{part_spec}%'  '''
    if part_name != "":
        part_name1 = f''' and part_name  like '%{part_name}%'  '''
    if area != "":
        area1 = f''' and area like '%{area}%'  '''
    if type != "":
        type1 = f''' and type like '%{type}%'  '''

    tempsql = f'''{part_spec1}{part_name1}{area1}{type1}'''

    sql = f''' select  * from part_detail  
    where 1=1 {tempsql} order by id
     '''

    print("执行查询sql  ", sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


@app.get('/getroles')
def getroles(currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0):
    print(currentpagecount)
    # 传过来取多少页的数据
    print(pagesize)

    db = getConn()
    print('获取角色列表'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()
    sql = f''' select * from user_role '''
    cursor.execute(sql)

    res = cursor.fetchall()

    cursor.execute("select count(id) from user_role ")
    data = cursor.fetchall()
    pages = 0
    # 查询分多少页
    if currentpagecount != 0:
        total = data[0][0]
        tem = total % currentpagecount
        tem1 = total // currentpagecount

        # 算出总页数
        pages = tem if tem == 0 else tem1+1

    start = currentpagecount*(pagesize-1)
    end = currentpagecount
    print('start')
    print(start)
    print('end')
    print(end)
    print('pages')
    print(pages)
    print(data[0][0])
    print('获取用户列表'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor.execute(
        "select * from user_role order by id  limit {0},{1}".format(start, end))
    data1 = cursor.fetchall()

    #
    res = {
        'total': data[0][0],
        'data1': data1,
        'pages': pages
    }
    print(res)
    return res


@app.get('/getUserRoles')
def getUserRoles(auth_code:  Optional[str] = None):

    sql = ""
    if auth_code == None:
        sql = " select * from menu_list"
    else:
        sql = f''' 
      select mm.id,mm.menu_name,aa.auth_code,aa.menu_name,mm.name,mm.parentname from menu_list mm left join 
    (
    select ml.id,ul.auth_code,ml.menu_name from user_role_list ul left join menu_list ml
    on ul.`name`=ml.`name` and ul.component = ml.compent
    where ul.auth_code='{auth_code}'
    and ml.menu_name is not null) aa
    on aa.menu_name=mm.menu_name and mm.id=aa.id
		where aa.auth_code  is not null
    order by mm.id
    '''
    db = getConn()

    print('sql', sql)
    cursor = db.cursor()

    cursor.execute(sql)
    data1 = cursor.fetchall()

    return data1

# del Role


@app.get('/deleteRole')
def deleteRole(auth_code: Optional[str] = None, auth_name: Optional[str] = None, id: Optional[str] = None):
    db = getConn()
    cursor = db.cursor()
    delsql = f''' delete from user_role 
    where auth_code='{auth_code}' and auth_name='{auth_name}' and id ='{id}' '''
    cursor.execute(delsql)
    db.commit()
    print('删除角色成功')
    return '删除成功'

# add Role


@app.get('/addRole')
def addRole(auth_code: Optional[str] = None, auth_name: Optional[str] = None):
    db = getConn()
    cursor = db.cursor()
    addsql = f''' INSERT INTO `part`.`user_role` ( `auth_name`, `auth_code`, `btn_auth`)
                VALUES ('{auth_name}', '{auth_code}', '["btn.add","btn.edit"]');
 '''
    cursor.execute(addsql)
    db.commit()
    print('添加角色成功')
    return '添加角色成功'


@app.get('/updateUserRole')
def updateUserRole(auth_list: Optional[str] = None, current_authcode: Optional[str] = None):

    if auth_list == None or current_authcode == None:
        return
    print('传过来的auth_list', auth_list)
    authIds = list(eval(auth_list))
    authIds.append(31)
    authIds = set(authIds)
    authIdStr = auth_list[1:-1]
    print(authIdStr)
    # 删除原来的权限
    db = getConn()
    cursor = db.cursor()
    delsql = f''' delete from user_role_list where  auth_code='{current_authcode}'  '''
    cursor.execute(delsql)
    db.commit()
    print('删除成功')

    compent = ''
    path = ''
    name = ''
    title = ''
    icon = ''
    redirect = ''
    parentname = ''
    number = ''

    # add role
    for i in authIds:
        print(i)
        temp = 0
        if i == 31:
            temp = 1
        else:
            temp = 2
        addsql = f'''
            INSERT INTO user_role_list
( `auth_code`, `component`, `path`, `name`, `title`, `icon`, `redirect`, `parentname`, `number`, `menuId`) 
select ue.auth_code,tt.compent as component ,tt.path,tt.`name`,tt.title,tt.icon,tt.redirect,tt.parentname,{temp} as number,tt.id  as menuId
from menu_list tt , user_role ue  where tt.id={i} and ue.auth_code='{current_authcode}'
        
                '''
        cursor.execute(addsql)
        db.commit()
        print('添加成功')
    return '添加成功'
    # for t in temp:
    #     print('auth_list',t['id'],t['auth_code'],t['menu_name'])
    #     #update

    #     sql=f'''  '''
    #     cursor.execute(sql)


# 获取用户列表
@app.get('/getusers')
def getusers(userName:  Optional[str] = None, currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0):
    db = getConn()
    print('获取用户列表'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor = db.cursor()
    # find  username

    print('userName', userName)
    if userName != None:
        findsql = f''' 
        select * from user rr left join user_role re on re.auth_code=rr.role
        where rr.username  like '%{userName}%'
        order by rr.id   '''
        cursor.execute(findsql)
        res = cursor.fetchall()
        return res

    # 10 6
     # 每页多少条数据 默认10
    print('currentpagecount', currentpagecount)
    # 传过来取多少页的数据
    print('pagesize', pagesize)

    # 查询多少条
    cursor.execute(
        "select count(*) from user rr left join user_role re on re.auth_code=rr.role")
    data = cursor.fetchall()
    pages = 0
    total = 0
    # 查询分多少页
    if currentpagecount != 0:
        total = data[0][0]
        tem = total % currentpagecount
        tem1 = total // currentpagecount

        # 算出总页数
        print('tem', tem)
        print('tem1', tem1)

        pages = tem1 if tem == 0 else tem1+1

    start = currentpagecount*(pagesize-1)
    end = currentpagecount
    print('start', start)

    print('end', end)

    print('pages', pages)

    print('total', total)
    print('获取用户列表'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cursor.execute(
        "select * from user rr left join user_role re on re.auth_code=rr.role order by rr.id   limit {0},{1}".format(start, end))
    data1 = cursor.fetchall()

    #
    res = {
        'total': data[0][0],
        'data1': data1,
        'pages': pages
    }
    print(res)
    # db = getConn()
    # print('获取用户列表'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # cursor = db.cursor()
    # cursor.execute(
    #     "select * from user rr left join user_role re on re.auth_code=rr.role by ")
    # data = cursor.fetchall()

    return res


@app.get('/updateuser')
def getusers(username: Optional[str] = None,
             password: Optional[str] = None,
             role: Optional[str] = None,
             area: Optional[str] = "",
             inspect_area: Optional[str] = "",
             flag: Optional[str] = None):
    db = getConn()

    cursor = db.cursor()
    print('area----')
    print(area)
    print('inspect_area----')
    print(inspect_area)
    print(role)

    sql = f''' '''
    area1 = ''
    password1 = ''

    inspect_area1 = ''
    if area != '':
        area1 = f''',`area` ='{area}' '''
    else:
        area1 = f''',`area` =null '''
    if password != '':
        password1 = f''',password='{password}' '''
    else:
        password1 = f''',password=null '''

    if inspect_area != '':
        inspect_area1 = f''',`inspect_area` ='{inspect_area}' '''
    else:
        inspect_area1 = f''',`inspect_area` =null '''

    endsql = f'''
                       UPDATE `part`.`user`
                      SET
                         `role` = '{role}'
                       {password1}
                        {area1}
                        {inspect_area1}
                      WHERE
                      	`username` = '{username}'
                       '''
    print(endsql)
    if flag == '编辑':
        cursor.execute(endsql)
        db.commit()
        print('修改信息成功')
        return '修改成功'
    elif flag == '删除':
        cursor.execute('''
         delete from `user` where `username`='{}'
                       '''.format(username))
        db.commit()
        print('删除成功')
        return '删除成功'


def generate_token(key):
    """
    @Args:
        key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
        expire: int(最大有效时间，单位为s)
    @Return:
        state: str
    :param key:
    :param expire:
    :return:
    """
    ts_str = str(time.time())
    ts_byte = ts_str.encode("utf-8")
    sha1_tshex_str = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshex_str
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))

    return b64_token.decode("utf-8")


# 测试获取路由列表


def arr2tree(source, parent):
    tree = []
    for item in source:
        if item["parent_name"] == parent:

            item["children"] = arr2tree(source, item["name"])
            tree.append(item)
    return tree


@app.get('/getroutes')
def getroutes(auth: str):
    # auth: str
    print('auth', auth)

    db = getConn()

    cursor = db.cursor()

    # 父路由
    cursor.execute(
        f''' select * from user_role_list where auth_code='{auth}' and parentname is null order by number ''')
    data1 = cursor.fetchall()
    print('data1 父路由', data1)
    # 子路由
    cursor.execute(
        f''' select * from user_role_list where auth_code='{auth}' and parentname is not null  order by number ''')
    data2 = cursor.fetchall()
    print('data2 子路由', data2)

    # cursor.execute(
    #     f''' select * from user_role_list where auth_code='{auth}'  order by number ''')
    # data3 = cursor.fetchall()
    # print('data3',data3)
    # 获取后端路由表  通过传进来的角色
    # 处理路由

    # routes = open(
    #     r'C:\Users\Administrator\Desktop\Demo\vue-next-admin\src\serverpy\static\adminMenu.json'
    # )
    # a = json.load(routes)
    # print(a)

    # 获取橘色路由

    # 通过角色定义data 权限列表
    roledata = []
    if data1 != None:
        for i in data1:

            temp = {
                "path": ''.join(i[3]),
                "name": ''.join(i[4]),
                "component": ''.join(i[2]),
                "meta": {
                        "title": ''.join(i[5]),
                        "isLink": "",
                        "isHide": False,
                        "isKeepAlive": False,
                        "isAffix": False,
                        "isIframe": False,
                        # 处理权限
                        "auth": [''.join(i[1])],
                        "icon": "iconfont {}".format(i[6])
                },

            }
            if i[7] != None:
                temp['redirect'] = i[7]
                temp['children'] = []

            for j in data2:

                if ''.join(i[4])+''.join(i[1]) == ''.join(j[8])+''.join(j[1]):

                    temp['children'].append({
                        "path": ''.join(j[3]),
                        "name": ''.join(j[4]),
                        "component": ''.join(j[2]),
                        "meta": {
                            "title": ''.join(j[5]),
                            "isLink": "",
                            "isHide": False,
                            "isKeepAlive": True,
                            "isAffix": False,
                            "isIframe": False,
                            # 处理权限
                            "auth": [''.join(j[1])],
                            "icon": "iconfont {}".format(j[6])
                        }
                    })
                print(temp)
            roledata.append(temp)
            # path ,name, component,title,auth,icon
            print('roledata'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        resdata = {"code": 0, "type": "adminMenu", "data": roledata}

        # print(f''' {auth} 权限  {resdata}''')
        return resdata
    else:
        return '没有权限'


# 用户信息模型

class user(BaseModel):
    userName: str
    password: str


@app.post('/Verify')
def Verify(user: user):
    # auth: str
    print(user)
    print(user.userName)
    print(user.password)
    db = getConn()
    print('yanzheng')
    cursor = db.cursor()
    sql = f'''  select * from user u  where  u.username='{user.userName}' and u.password = '{user.password}' '''
    cursor.execute(sql)
    data = cursor.fetchone()
    print(data)
    if data is None:
        return '用户名密码错误或者权限错误'
    else:

        cursor.execute(
            f'''
        INSERT INTO `part`.`operationlog` (
          `name`,
          `type`,
          `create_date`
          )
          VALUES
            (
              '{user.userName}',
              '登录',
              '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}'
            );

        ''')
        db.commit()
        cursor.execute(
            '''
        select area,btn_auth from user rr left join user_role re on re.auth_code=rr.role
        where rr.username='{0}'
        '''.format(user.userName))
        areainfo = cursor.fetchone()
        print('areainfo')
        print(areainfo)
        if areainfo[0] is None:
            pass
        if areainfo[1] is None:
            pass

        data1 = {'flag': 'success', 'userName': user.userName,
                 'auth': data[3], 'areainfo': areainfo[0], 'btn_auth': areainfo[1]}

        print(data1)
        return data1


@app.get('/savefile')
def savefile(objectUrl: str, filename: str, type: str):
    # auth: str
    pass

    # 查询保养记录


@app.get('/getinspection')
def getinspection(cardid:  Optional[str] = None, flag: Optional[str] = '', username:  Optional[str] = None):
    # auth: str
    db = getConn()
    print('获取巡检区域')
    print(type(cardid))
    cursor = db.cursor()
    if cardid == '-1':
        cursor.execute(
            f''' select inspect_area from `user` where  username = '{username}' ''')

        data1 = cursor.fetchall()
        print("获取到电器全部的区域")
        print(len(data1))
        print(data1)
        if data1[0][0] == '':
            return -1
        if data1[0][0] == None:
            return -1
        temp = str(data1[0][0])
        temp1 = temp[1:len(temp)-1]

        sql = f''' select * from machine_inspection where cardname in({temp1})  '''
        cursor.execute(sql)

        result = cursor.fetchall()
        print('result')
        print(result)
        return result

    new_cardid = cardid[1:len(cardid)-1]
    # new_cardid = cardid
    print('new_cardid:', new_cardid)

    cursor.execute(
        '''select * from inspection where cardid='{0}'
        '''.format(new_cardid))
    data = cursor.fetchone()
    print('巡检区域为')
    print(data)

    # 获取区域
    if flag == '1':
        cursor.execute(
            '''select cardname from inspection where cardid='{0}'
        '''.format(new_cardid))
        data = cursor.fetchone()
        print(data)
        tem = data[0]
        cursor.execute(
            f'''select area from part_detail where area like '{tem}%' group by area''')
        rs = cursor.fetchall()
        return rs

    # 查询保养、外修和备件管理 的确认
    if data == None:
        return '未查询到对应区域'

    if data[2] == None:
        return '未查询到对应区域'
    else:
        # 查询该区域未保养记录

        resdata = {

        }
        resdata['area'] = data[2]
        resdata['cardid'] = data[1]

        cursor.execute('''



            select * from (
            select * from maintenance_detail where use_area like '%{}%'
            ) aa
            where useconfirm ="" or maintenanceman =''
                      '''.format(data[2]))

        maintenance_data = cursor.fetchall()
        print(maintenance_data)
        if maintenance_data == None:
            print('保养未找到未确认')
        else:

            resdata['maintenance_data'] = maintenance_data

        # 查询外修未确认数据

        cursor.execute('''

                    SELECT
            *
          FROM
            (
              SELECT
                *
              FROM
                repair_detail
              WHERE
                use_area like  '%{}%'
            ) aa
          WHERE
            aa.useconfirm = ''
          OR aa.applicant = ''
          OR aa.tryout = ''
          OR aa.receipt = ''
                      '''.format(data[2]))

        repair_data = cursor.fetchall()

        if repair_data == None:
            print('外修未找到未确认')
        else:
            resdata['repair_data'] = repair_data

        # 查询当前区域的备件管理明细

        cursor.execute('''

              SELECT
                *
              FROM
                part_detail
              WHERE
                area like '%{}%'
                      '''.format(data[2]))

        part_data = cursor.fetchall()

        if part_data == None:
            print('备件未找到')
        else:
            resdata['part_data'] = part_data
    return resdata


@app.get('/saveinspectlog')
def saveinspectlog(inspectdate:  Optional[str] = None,
                   inspecter:  Optional[str] = None,
                   remark:  Optional[str] = None,
                   inspect_area: Optional[str] = None,
                   cardid: Optional[str] = None):
    db = getConn()
    cursor = db.cursor()

    print('inspectdate')
    print(inspectdate)
    print('inspecter')
    print(inspecter)
    print('remark')
    print(remark)
    print('inspect_area')
    print(inspect_area)
    print('cardid')
    print(cardid)

    if cardid == '' or inspect_area == '' or remark == '':
        return '信息保存异常'

    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cursor.execute('''
              INSERT INTO `part`.`inspectionrecord` (
                    `start_inspect_date`,
                    `inspecter`,
                    `inspect_area`,
                    `cardid`,
                    `remark`,
                    `end_inspect_date`
                  )
                  VALUES
                    (
                     '{0}',
                     '{1}',
                      '{2}',
                      '{3}',
                      '{4}',
                      '{5}'
                    );
                   '''.format(inspectdate, inspecter, inspect_area, cardid, remark, time1))
    db.commit()
    print('巡检记录添加完成'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    res = {
        'msg': '巡检记录添加完成',
        'endtime': time1
    }
    return res


def part_update_log(
        username: Optional[str] = None,
        area: Optional[str] = None,
        spec: Optional[str] = None,
        item_name: Optional[str] = None,
        count: Optional[int] = 0,
        flag: Optional[str] = None):

    # 更新记录表
    db = getConn()
    cursor = db.cursor()
    if flag == 'add':
        cursor.execute(f''' INSERT INTO `part`.`log` (`username`, `area`, `spec`, `item_name`, `count`, `create_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'add','电器备件管理');
    ''')
        print("增加记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if flag == 'update':
        cursor.execute(f''' INSERT INTO `part`.`log` ( `username`, `area`, `spec`, `item_name`, `count`, `update_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'update','电器备件管理');
    ''')
        print("更新记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db.commit()


@app.get('/getareapartinspection')
def getareapartinspection(cardid:  Optional[str] = None):
    pass


# file 参数类型是 UploadFile
@app.post("/uploadfile")
async def create_upload_file(imgid: str, time1:  Optional[str] = None, file: UploadFile = File(...)):

    print(file.filename)
    print(file.content_type)
    print(file.filename)
    print(time1)
    print(imgid)
    contents = await file.read()
    imgsrc = imgid+"_" + \
        time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".jpg"
    print(imgsrc)
    file = open(
        f"{currentPath}\static\img\{imgsrc}", "wb")
    file.write(contents)

    # 传到静态地址

    db = getConn()
    cursor = db.cursor()

    cursor.execute('''
        UPDATE `part`.`part_detail`
        SET
        `partimgsrc` = '{0}'
        WHERE
          (`id` = '{1}')
                   '''.format('http://61.185.74.251:5556/static/img/'+imgsrc, imgid))

    db.commit()
    return '上传成功'
    # picture=await file.read()
    # result = {
    #     "filename": file.filename,
    #     "content-type": file.content_type,
    #     "read": ''
    # }
    # return result


# 获取机修备件明细

@app.get('/getmachine_detail')
def getmachine_detail(currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0):

    return machine.getparts(currentpagecount, pagesize)


# 备件设备整改获取
@app.get('/getmachine_equipment_rectification')
def getmachine_equipment_rectification(flag: Optional[str] = None,
                                       flag1: Optional[str] = '',
                                       start: Optional[str] = '',
                                       end: Optional[str] = '',
                                       prolince: Optional[str] = '',
                                       area: Optional[str] = ''):
    return machine.getmachine_equipment_rectification(flag, flag1, start, end, prolince, area)

# 信息


@app.get('/getmachine_usearea')
def getmachine_usearea():
    return machine.getusearea()

# 类型


@app.get('/getmachine_type')
def getmachine_type(area: Optional[str] = None):
    return machine.gettype(area)

# 名称


@app.get('/getmachine_name')
def getmachine_name(type: Optional[str] = None, area: Optional[str] = None, flag: Optional[str] = None):
    return machine.getpartname(type, area, flag)


# balance


@app.get('/getmachine_balance')
def getmachine_balance(type: Optional[str] = None,
                       area: Optional[str] = None,
                       spec: Optional[str] = None,
                       part_name: Optional[str] = None):
    return machine.getbalance(type, area, spec, part_name)
# 获取机修型号


@app.get('/getmachine_spesc')
def getmahcine_spesc(type: Optional[str] = None,  use_part_name: Optional[str] = None, area: Optional[str] = None):

    return machine.getspesc(type, use_part_name, area)


# 获取机修领用明细
@app.get('/getmachine_userecord')
def getmachine_userecord(flag: Optional[str] = '',
                         flag1: Optional[str] = '',
                         start: Optional[str] = '',
                         end: Optional[str] = '',
                         prolince: Optional[str] = '',
                         area: Optional[str] = ''):

    return machine.getuserecord(flag,
                                flag1,
                                start,
                                end,
                                prolince,
                                area)


@app.get('/getMachine_repair')
def getMachine_repair(flag: Optional[str] = None,
                      flag1: Optional[str] = '',
                      start: Optional[str] = '',
                      end: Optional[str] = '',
                      prolince: Optional[str] = '',
                      area: Optional[str] = ''):

    return machine.getMachine_repair(flag,
                                     flag1,
                                     start,
                                     end,
                                     prolince,
                                     area)

# 机修保养记录


@app.get('/getmachine_maintenance')
def getmachine_maintenance(flag: Optional[str] = '',
                           flag1: Optional[str] = '',
                           start: Optional[str] = '',
                           end: Optional[str] = '',
                           prolince: Optional[str] = '',
                           area: Optional[str] = ''):

    return machine.getmaintenance(flag,
                                  flag1,
                                  start,
                                  end,
                                  prolince,
                                  area)


@app.get('/addmachine_maintenance')
def addmachine_maintenance(user: str, area: str, type: str, spec: str, part_name: str,
                           use_count: str, reason: str, use_date: str, confirm: str,
                           flag: Optional[str] = None):
    return machine.addmaintenance(user, area, type, spec, part_name,
                                  use_count, reason, use_date, confirm,
                                  flag)


@app.get('/updatemachine_maintenance')
def updatemachine_maintenance(id: int,
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
                              flag: Optional[str] = ''):
    return machine.updatemaintenance(id,
                                     user,
                                     new_area,
                                     type,
                                     spec,
                                     use_part_name,
                                     use_date,
                                     use_area,
                                     use_count,
                                     useconfirm,
                                     maintenanceman,
                                     maintenance_date,
                                     scrap,
                                     useconfirmdate,
                                     use_procline,
                                     flag)


class Machine_repair(BaseModel):
    username: Optional[str] = ''
    id: Optional[str] = ''
    use_count: Optional[str] = '0'
    use_area: Optional[str] = ''
    use_date: Optional[str] = ''
    use_part_name: Optional[str] = ''
    use_reason: Optional[str] = ''
    type: Optional[str] = ''
    spec: Optional[str] = ''
    new_area: Optional[str] = ''
    applicant: Optional[str] = ''
    receipt: Optional[str] = ''
    applicantdate: Optional[str] = ''
    receiptdate: Optional[str] = ''


@app.post('/updateMachine_repair')
def updateMachine_repair(machine_repair: Machine_repair):

    print('Machine_repair', machine_repair)
    return machine.updateMachine_repair(machine_repair)


@app.get('/getmachine_scrap')
def getmachine_scrap(flag: Optional[str] = '',
                     flag1: Optional[str] = '',
                     start: Optional[str] = '',
                     end: Optional[str] = '',
                     prolince: Optional[str] = '',
                     area: Optional[str] = ''):

    print('获取机修报废记录')
    return machine.getscrap(flag,
                            flag1,
                            start,
                            end,
                            prolince,
                            area)


@app.get('/updatemachine_scrap')
def updatemachine_scrap(id: int,
                        add_count: Optional[int] = 0,
                        received: Optional[int] = 0,
                        new_area: Optional[str] = '',
                        user: Optional[str] = '',
                        use_area: Optional[str] = '',
                        type: Optional[str] = '',
                        spec: Optional[str] = '',
                        use_part_name: Optional[str] = '',
                        use_count: Optional[str] = '',
                        use_reason: Optional[str] = '',
                        use_date: Optional[str] = '',
                        scrapconfirm: Optional[str] = '',
                        selectOption: Optional[str] = '',
                        selectOptiondate: Optional[str] = '',
                        applyformconfirm: Optional[str] = '',
                        applyformconfirmdate: Optional[str] = '',
                        applicantman: Optional[str] = '',
                        useconfirm: Optional[str] = '',
                        scrapconfirmdate: Optional[str] = '',
                        applicantdate: Optional[str] = '',
                        remark: Optional[str] = '',
                        useconfirmdate: Optional[str] = '',
                        flag: Optional[str] = '',
                        flag1: Optional[str] = ''):

    return machine.updatescrap(id,
                               add_count,
                               received,
                               new_area,
                               user,
                               use_area,
                               type,
                               spec,
                               use_part_name,
                               use_count,
                               use_reason,
                               use_date,
                               scrapconfirm,
                               selectOption,
                               selectOptiondate,
                               applyformconfirm,
                               applyformconfirmdate,
                               applicantman,
                               useconfirm,
                               scrapconfirmdate,
                               applicantdate,
                               remark,
                               useconfirmdate,
                               flag,
                               flag1)


@app.get('/updatemachine_userecord')
def updatemachine_userecord(id: int,
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
    return machine.updateuserecord(id,
                                   useconfirm,
                                   use_count,
                                   use_area,
                                   use_date,
                                   use_part_name,
                                   type,
                                   spec,
                                   user,
                                   user_reason,
                                   confirm_date,
                                   flag,
                                   username,
                                   password,
                                   handle,
                                   use_procline)


# 添加
@app.get('/addmachine_detail')
def addmachine_detail(
        username: Optional[str] = None,
        part_name: Optional[str] = None,
        part_spec: Optional[str] = None,
        area: Optional[str] = None,
        balance: Optional[int] = 0,
        remark: Optional[str] = None,
        type: Optional[str] = None):
    return machine.addmachine_detail(username, part_name, part_spec, area, balance, remark, type)


# 增加机修领用
@app.post('/addmachine_userecord')
def addmachine_userecord(userecordform: Optional[userecordform] = None):

    print('进入到机修领用流程')
    return machine.adduserecord(userecordform)


# 删除


@app.get('/deletemachine')
def deletemachine(id: int):
    return machine.deletepart(id)

# 更新


@app.get('/updatemachine_part')
def updatemachine_part(username: Optional[str] = None,
                       id: Optional[int] = None,
                       part_name: Optional[str] = None,
                       part_spec: Optional[str] = None,
                       area: Optional[str] = None,
                       type: Optional[str] = None,
                       new_balance: Optional[int] = None,
                       new_original: Optional[int] = None,
                       connection: Optional[str] = None,
                       flag: Optional[str] = None):
    return machine.updatemachine_part(username, id,
                                      part_name,
                                      part_spec,
                                      area,
                                      type,
                                      new_balance,
                                      new_original,
                                      connection)


# 筛选查询
@app.get('/selectmachine')
def selectmachine_part(part_spec: Optional[str] = None,
                       part_name: Optional[str] = None,
                       area: Optional[str] = None,
                       type: Optional[str] = None,):
    return machine.selectpart(part_spec, part_name, area, type)


# @app.get('/deletemachine_part')
# def deletemachine_part(id: int):
#     return machine.deletepart(id)


# 获取机修巡检信息


@app.get('/getmachine_inspection')
def getmachine_inspection(cardid:  Optional[str] = None, username: Optional[str] = None):
    return machine.getinspection(cardid, username)


@app.get('/getmachine_inspectionrecord')
def getmachine_inspectionrecord():
    return machine.getinspectionrecord()


@app.get('/savemachine_inspectlog')
def savemachine_inspectlog(inspectdate:  Optional[str] = None,
                           inspecter:  Optional[str] = None,
                           remark:  Optional[str] = None,
                           inspect_area: Optional[str] = None,
                           cardid: Optional[str] = None):
    return machine.saveinspectlog(inspectdate,
                                  inspecter,
                                  remark,
                                  inspect_area,
                                  cardid)


# @app.get('/updateequipment_rectification')
# def updateequipment_rectification(id: Optional[str] = '',
#                                   user: Optional[str] = '',
#                                   use_area: Optional[str] = '',
#                                   type: Optional[str] = '',
#                                   spec: Optional[str] = '',
#                                   use_part_name: Optional[str] = '',
#                                   use_count: Optional[str] = '',
#                                   use_reason: Optional[str] = '',
#                                   use_date: Optional[str] = '',
#                                   useconfirm: Optional[str] = '',
#                                   use_procline: Optional[str] = '',
#                                   new_area: Optional[str] = '',
#                                   useconfirmdate: Optional[str] = '',
#                                   remark: Optional[str] = '',
#                                   flag: Optional[str] = '',
#                                   flag1: Optional[str] = ''):

#     return machine.updatemachine_equipment_rectification()
#     # 机修上传


@app.post('/machine_uploadfile')
async def machine_uploadfile(imgid: Optional[str] = None, time1:  Optional[str] = None, file: UploadFile = File(...)):

    return await machine.create_upload_file(imgid, time1, file)


# 成套

# 获取成套备件明细
@app.get('/getmachine_parts_detail')
def getmachine_parts_detail(currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0):

    return Machine_parts.getparts(currentpagecount, pagesize)


# 获取成套领用明细
@app.get('/getmachine_parts_userecord')
def getmachine_parts_userecord(flag: Optional[str] = '',
                               flag1: Optional[str] = '',
                               start: Optional[str] = '',
                               end: Optional[str] = '',
                               prolince: Optional[str] = '',
                               area: Optional[str] = ''):
    print('获取成套领用明细')
    return Machine_parts.getuserecord(flag,
                                      flag1,
                                      start,
                                      end,
                                      prolince,
                                      area)


# 增加成套领用记录
@app.get('/addmachine_part_userecord')
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
                              machine_part_name: Optional[str] = ''
                              ):

    return Machine_parts.addmachine_part_userecord(part_name, part_spec,
                                                   reason, use_count,
                                                   type1, handle,
                                                   use_area, user, use_date, type, use_procline, machine_part_name)


# 获取成套单体备件库存信息


@app.get('/get_part_balanceinfo')
def get_part_balanceinfo(part_name: str):
    return Machine_parts.get_part_balanceinfo(part_name)


# 增加成套单体 减少备件库存

@app.get('/addmachine_part_count')
def addmachine_part_count(part_name: str, area: str, addcount: str, machine_part_area: str):
    return Machine_parts.addmachine_part_count(part_name, area, addcount, machine_part_area)


# 获取成套名称

@app.get('/getmachine_part_names')
def getmachine_part_names(area: str):
    print('area', area)
    return Machine_parts.getmachine_part_names(area)


# 增加成套
@app.get('/addmachine_part')
def addmachine_part(
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

        connection: Optional[str] = None):
    return Machine_parts.addparts(
        username,
        part_name,
        part_spec,
        area,
        balance,
        original,
        remark,
        machine_part_name,
        type, type1, connection)

# 更新成套


@app.get('/update_machine_part')
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

    return Machine_parts.update_machine_part(username, id, part_name, part_spec, area, type, new_balance, new_original, connection, machine_part_name)
    # 获取区域


@app.get('/getmachine_part_usearea')
def getmachine_part_usearea():
    return Machine_parts.getusearea()


@app.get('/getmachine_part_equipment_rectification')
def getmachine_part_equipment_rectification(flag: Optional[str] = None,
                                            flag1: Optional[str] = '',
                                            start: Optional[str] = '',
                                            end: Optional[str] = '',
                                            prolince: Optional[str] = '',
                                            area: Optional[str] = ''):
    return Machine_parts.getmachine_part_equipment_rectification(flag, flag1, start, end, prolince, area)


@app.get('/updateMachine_part_equipment_rectification')
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
                                               flag1: Optional[str] = ''):
    return Machine_parts.updateMachine_part_equipment_rectification(id,
                                                                    user,
                                                                    use_area,
                                                                    type,
                                                                    spec,
                                                                    use_part_name,
                                                                    use_count,
                                                                    use_reason,
                                                                    use_date,
                                                                    useconfirm,
                                                                    use_procline,
                                                                    new_area,
                                                                    useconfirmdate,
                                                                    remark,
                                                                    flag,
                                                                    flag1)


@app.get('/selectmachine_part')
def selectmachine_part(part_spec: Optional[str] = None,
                       part_name: Optional[str] = None,
                       area: Optional[str] = None,
                       type: Optional[str] = None,):
    return Machine_parts.selectpart(part_spec, part_name, area, type)


@app.get('/deletemachine_part')
def deletemachine_part(single_part_name: str, flag: str, part_id: str):
    return Machine_parts.deletepart(single_part_name, flag, part_id)


@app.get('/getmachine_part_type')
def getmachine_part_type(area: Optional[str] = None):
    return Machine_parts.gettype(area)


@app.get('/getmachine_part_spesc')
def getmachine_part_spesc(type: Optional[str] = None,  use_part_name: Optional[str] = None, area: Optional[str] = None):
    return Machine_parts.getspesc(type, use_part_name, area)


@app.get('/getmachine_parts_singlepart')
def getmachine_parts_singlepart(machine_part_name: Optional[str] = None):
    return Machine_parts.getmachine_parts_singlepart(machine_part_name)


# 成套上传图片

@app.post('/machine_part_uploadfile')
async def machine_part_uploadfile(machine_part_name: Optional[str] = None, imgid: Optional[str] = None, time1:  Optional[str] = None, file: UploadFile = File(...)):

    return await Machine_parts.create_upload_file(machine_part_name, imgid, time1, file)


# 获取工装明细


@app.get('/gettooling_detail')
def gettooling_detail(currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0):

    return tooling_manager.gettooling_detail(currentpagecount, pagesize)


# 筛选查询工装明细
@app.get('/selecttooling')
def selecttooling(part_spec: Optional[str] = None,
                  part_name: Optional[str] = None,
                  area: Optional[str] = None,
                  type: Optional[str] = None,):
    return tooling_manager.selecttooling(part_spec, part_name, area, type)


# 获取区域
@app.get('/gettooling_usearea')
def gettooling_usearea():
    return tooling_manager.getusearea()


# 获取类型
@app.get('/gettooling_type')
def gettooling_type(area: Optional[str] = None):
    return tooling_manager.gettype(area)


# 名称


@app.get('/gettooling_name')
def gettooling_name(type: Optional[str] = None, area: Optional[str] = None):
    return tooling_manager.getpartname(type, area)


@app.get('/gettooling_spesc')
def gettooling_spesc(type: Optional[str] = None,  use_part_name: Optional[str] = None, area: Optional[str] = None):

    return tooling_manager.getspesc(type, use_part_name, area)


# 添加
@app.get('/addtooling_detail')
def addtooling_detail(
        username: Optional[str] = None,
        part_name: Optional[str] = None,
        part_spec: Optional[str] = None,
        area: Optional[str] = None,
        balance: Optional[int] = 0,
        remark: Optional[str] = None,
        type: Optional[str] = None):
    return tooling_manager.addtooling_detail(username, part_name, part_spec, area, balance, remark, type)

# 删除


@app.get('/deletetooling')
def deletetooling(id: int):
    print("id", id)
    return tooling_manager.deletepart(id)


# 更新工装
@app.get('/updatetooling')
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
    return tooling_manager.updatetooling(
        username, id,
        part_name,
        part_spec,
        area,
        type,
        new_balance,
        new_original,
        connection)

# 上传图片


@app.post('/tooling_uploadfile')
async def tooling_uploadfile(imgid: Optional[str] = None, time1:  Optional[str] = None, file: UploadFile = File(...)):

    return await tooling_manager.create_upload_file(imgid, time1, file)


@app.get('/getAdoption')
def getAdoption(flag: Optional[str] = '',
                flag1: Optional[str] = '',
                start: Optional[str] = '',
                end: Optional[str] = '',
                prolince: Optional[str] = '',
                area: Optional[str] = ''):

    return tooling_manager.getuserecord(flag,
                                        flag1,
                                        start,
                                        end,
                                        prolince,
                                        area)


# get tooling balance
@app.get('/gettooling_balance')
def gettooling_balance(type: Optional[str] = None,
                       area: Optional[str] = None,
                       spec: Optional[str] = None,
                       part_name: Optional[str] = None):
    return tooling_manager.getbalance(type, area, spec, part_name)


# add tooling  Adoption
@app.post('/addtooling_Adoption')
def addtooling_Adoption(userecordform: Optional[userecordform] = None):

    print('进入到工装领用流程')
    return tooling_manager.adduserecord(userecordform)


# confirm tooling  Adoption
@app.get('/updatetooling_Adoption')
def updatetooling_Adoption(id: int,
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
    return tooling_manager.updateuserecord(id,
                                           useconfirm,
                                           use_count,
                                           use_area,
                                           use_date,
                                           use_part_name,
                                           type,
                                           spec,
                                           user,
                                           user_reason,
                                           confirm_date,
                                           flag,
                                           username,
                                           password,
                                           handle,
                                           use_procline)


# get tooling  maintenance
@app.get('/gettooling_maintenance')
def gettooling_maintenance(flag: Optional[str] = '',
                           flag1: Optional[str] = '',
                           start: Optional[str] = '',
                           end: Optional[str] = '',
                           prolince: Optional[str] = '',
                           area: Optional[str] = ''):

    return tooling_manager.getmaintenance(flag,
                                          flag1,
                                          start,
                                          end,
                                          prolince,
                                          area)


@app.get('/addtooling_maintenance')
def addtooling_maintenance(user: str, area: str, type: str, spec: str, part_name: str,
                           use_count: str, reason: str, use_date: str, confirm: str,
                           flag: Optional[str] = None):
    return tooling_manager.addmaintenance(user, area, type, spec, part_name,
                                          use_count, reason, use_date, confirm,
                                          flag)


@app.get('/updatetooling_maintenance')
def updatetooling_maintenance(id: int,
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
                              flag: Optional[str] = ''):
    return tooling_manager.updatemaintenance(id,
                                             user,
                                             new_area,
                                             type,
                                             spec,
                                             use_part_name,
                                             use_date,
                                             use_area,
                                             use_count,
                                             useconfirm,
                                             maintenanceman,
                                             maintenance_date,
                                             scrap,
                                             useconfirmdate,
                                             use_procline,
                                             flag)


@app.get('/get_log')
def get_log(currentpagecount:  Optional[int] = 0, pagesize: Optional[int] = 0, remark: Optional[str] = None,
            part_name: Optional[str] = None,
            part_spec: Optional[str] = None,
            area: Optional[str] = None,
            flag: Optional[str] = None):
    db = getConn()
    cursor = db.cursor()

    print('currentpagecount', currentpagecount)

    print('pagesize', pagesize)

    print('remark', remark)

    print('part_name', part_name)

    print('part_spec', part_spec)

    print('area', area)

    print('flag', flag)

    if remark != None and part_name == None:
        sql = "select * from log where remark='" + remark + "'"
        cursor.execute(sql)
        rs = cursor.fetchall()
        print('初始化查询')
        return rs

    if part_name != None or area != None or part_spec != None:
        # 筛选查询
        print('筛选查询')
        part_name1 = ''
        area1 = ''
        part_spec1 = ''
        flag1 = ''
        if area != None:
            area1 = " and area like'%{}%'  ".format(area)

        if part_name != None:
            part_name1 = " and item_name like '%{}%'".format(part_name)
        if part_spec != None:
            part_spec1 = " and spec like'%{}%'".format(part_spec)

        if flag != None:
            flag1 = " and flag like'%{}%'".format(flag)

        sql = f"select * from log where 1=1 {area1} {part_name1} {part_spec1} {flag1}"
        print(sql)
        cursor.execute(sql)
        rs = cursor.fetchall()
        return rs
    cursor.execute(
        f'''select * from log where remark='{remark}' order by id ''')
    rs = cursor.fetchall()
    return rs


# 更新 2022-07-05 增加机修产线


@app.get('/getMachine_proclinedetail')
def getMachine_proclinedetail(procline: Optional[str] = '',):
    return Machine_procline.getMachine_proclinedetail(procline)


@app.get('/getProclineMachineTypes')
def getProclineMachineTypes():
    return Machine_procline.getProclineMachineTypes()


@app.get('/getMachine_proclineSummary')
def getMachine_proclineSummary():
    return Machine_procline.getMachine_proclineSummary()


@app.get('/getmachine_contrast')
def getmachine_contrast(machineType: Optional[str] = ""):
    print('machineType', machineType)
    return Machine_procline.getmachine_contrast(machineType)


@app.post('/machine_procline_detail_uploadfile')
async def machine_procline_detail_uploadfile(flag: Optional[str] = None, imgid: Optional[str] = None, time1:  Optional[str] = None, file: UploadFile = File(...)):

    return await Machine_procline.create_upload_file(flag, imgid, time1, file)

# 添加产线使用件


@app.get('/addmachine_procline_detail')
def addmachine_procline_detail(procline: Optional[str] = None, part_name: Optional[str] = None, part_spec: Optional[str] = None, area: Optional[str] = None, type: Optional[str] = None, username: Optional[str] = None):
    return Machine_procline.addmachine_procline_detail(procline, part_name, part_spec, area, type, username)


@app.get('/deletemachine_procline_detail')
def deletemachine_procline_detail(id: Optional[str] = None, username: Optional[str] = None):
    print("进入删除方法")
    return Machine_procline.deletemachine_procline_detail(id, username)


@app.get('/updatemachine_procline_detail')
def updatemachine_procline_detail(id: Optional[str] = None, procline: Optional[str] = None, part_name: Optional[str] = None, part_spec: Optional[str] = None, area: Optional[str] = None, type: Optional[str] = None, username: Optional[str] = None):
    return Machine_procline.updatemachine_procline_detail(id, procline, part_name, part_spec, area, type, username)


class Crane(BaseModel):
    starttime: Optional[str] = '',
    endtime: Optional[str] = '',
    new_date: Optional[str] = '',
    models: Optional[str] = '',
    location: Optional[str] = '',
    description: Optional[str] = '',
    clength: Optional[str] = '',
    operator: Optional[str] = '',
    confirmer: Optional[str] = '',
    remark: Optional[str] = '',
    shift: Optional[str] = '',
    procline: Optional[str] = '',
    crane_name: Optional[str] = '',
    craneType: Optional[str] = ''


# 增加天车钢丝绳更换记录
@app.post('/add_crane_log')
def add_crane_log(crane: Crane):

    return machine.add_crane_log(crane)


class Pages(BaseModel):

    pagesize: Optional[int] = 0,
    currentPage: Optional[int] = 0

  # 查询天车记录


@app.post('/get_crane_log')
def get_crane_log(crane: Optional[Crane] = None, pages: Optional[Pages] = None):

    return machine.get_crane_log(crane, pages)


@app.get('/getVersion')
def getVersion():
    # auth: str

    return {
        'app_download': 'http://61.185.74.251:5556/'+'static/app_list/part3.32.apk',
        'app_info': '3.32'
    }


@app.get('/partPages')
def gopartPages(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})


# 请求体为数据模型
class aa(BaseModel):
    e: str


@app.get("/add_park_log")
def add_park_log(item: aa):
    print(item.e)

    db = getConn()
    cursor = db.cursor()

    cursor.execute(
        f'''INSERT INTO `play`.`park_log` ( `content`, `create_time`) 
        VALUES ('{item.e}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
        ''')
    db.commit()
    print("插入停车数据成功")
    return '插入停车数据成功'


#    ssl_keyfile="/ssl/server.key",
#                 ssl_certfile="/ssl/server.crt",
    #  ssl_keyfile="./www_ssxyf_cn.key",
    #             ssl_certfile="./www_ssxyf_cn.crt",


def get_external_ip():
    # proxies={'http': '***.***.***.***:****'}
    # site = requests.get("http://checkip.dyndns.org/",proxies=proxies)
    site = requests.get("http://checkip.dyndns.org/")
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site.text)
    address = grab[0]
    return address


if __name__ == '__main__':
    port = input("\033[1;34;40m请输入需要运行的端口号\033[0m \n")
    isnetworkip = input("\033[1;34;40m请选择 1.内网 2.外网 运行 \033[0m \n ")
    print('isnetworkip:', isnetworkip)
    ip = ""
    # print('外网', get_external_ip())
    if int(isnetworkip) == 1:
        print('仅限内网访问网页,app无法访问')
        ip = get_host_ip()
    if int(isnetworkip) == 2:
        print('外网ip')
        ip = '61.185.74.251'
    print('ip:', ip)

    print(
        f"\033[5;37;44m请按住ctrl点击链接 进入备件品备件管理系统登陆页面 http://{ip}:{port}/partPages   \033[0m")

    uvicorn.run(app,
                host='0.0.0.0',
                port=int(port))
