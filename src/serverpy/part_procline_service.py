import pinyin
import sys
from hmac import new
from fastapi import FastAPI, File, UploadFile
from typing import Optional

import time

from pydantic.main import BaseModel

import connect as conn


# 获取机修件
def getPart_proclinedetail(procline):
    db = conn.getConn()
    cursor = db.cursor()

    procline1 = ""
    if procline != "":
        procline1 = f''' and procline='{procline}'  '''
    else:
        procline1 = f''' and procline='圆镀一线'  '''
    cursor.execute(
        f'''select * from part_procline_detail where 1=1  {procline1} ''')

    res = cursor.fetchall()

    return res

# 获取机修产线使用件汇总


def getPart_proclineSummary():
    db = conn.getConn()
    cursor = db.cursor()
    cursor.execute(
        f'''
         	

						 select a.*,
						IFNULL(b.圆镀一线,''),
						IFNULL(c.圆镀二线,''),
						IFNULL(d.圆镀三线,''),
						IFNULL(e.圆镀四线,''),
						IFNULL(f.圆镀五线,''),
						IFNULL(g.圆镀六线,''),
						IFNULL(h.方镀一线,''),
						IFNULL(i.方镀二线,''),
						IFNULL(j.方镀三线,'')
						from 
          (select area,type, machine_name from part_procline_detail group by area,machine_name,type ) a
          left join 
          (select * from (
          select 
          area,
					type,
          machine_name,
          case procline
          when '圆镀一线' then  machine_spesc end '圆镀一线'
          from part_procline_detail) aa01
          where 圆镀一线 is not  null
          ) b  on a.area=b.area and a.machine_name=b.machine_name and a.type=b.type
          left join 
          (select * from (
          select 
          area,type,
          machine_name,
          case procline
          when '圆镀二线' then  machine_spesc end '圆镀二线'
          from part_procline_detail) aa01
          where 圆镀二线 is not  null
          ) c  on a.area=c.area and a.machine_name=c.machine_name and a.type=c.type
          left join 
          (select * from (
          select 
          area,type,
          machine_name,
          case procline
          when '圆镀三线' then  machine_spesc end '圆镀三线'
          from part_procline_detail) aa01
          where 圆镀三线 is not  null
          ) d  on a.area=d.area and a.machine_name=d.machine_name and a.type=d.type
          left join 
          (select * from (
          select 
          area,type,
          machine_name,
          case procline
          when '圆镀四线' then  machine_spesc end '圆镀四线'
          from part_procline_detail) aa01
          where 圆镀四线 is not  null
          ) e  on a.area=e.area and a.machine_name=e.machine_name and a.type=e.type
          left join 
          (select * from (
          select 
          area,type,
          machine_name,
          case procline
          when '圆镀五线' then  machine_spesc end '圆镀五线'
          from part_procline_detail) aa01
          where 圆镀五线 is not  null
          ) f on a.area=f.area and a.machine_name=f.machine_name and a.type=f.type
          left join 
          (select * from (
          select 
          area,type,
          machine_name,
          case procline
          when '圆镀六线' then  machine_spesc end '圆镀六线'
          from part_procline_detail) aa01
          where 圆镀六线 is not  null
          ) g  on a.area=g.area and a.machine_name=g.machine_name and a.type=g.type
          left join 
          (select * from (
          select 
          area,type,
          machine_name,
          case procline
          when '方镀一线' then  machine_spesc end '方镀一线'
          from part_procline_detail) aa01
          where 方镀一线 is not  null
          ) h  on a.area=h.area and a.machine_name=h.machine_name and a.type=h.type
          left join 
          (select * from (
          select 
          area,type,
          machine_name,
          case procline
          when '方镀二线' then  machine_spesc end '方镀二线'
          from part_procline_detail) aa01
          where 方镀二线 is not  null
          ) i  on a.area=i.area and a.machine_name=i.machine_name and a.type=i.type
          left join 
          (select * from (
          select 
          area,type,
          machine_name,
          case procline
          when '方镀三线' then  machine_spesc end '方镀三线'
          from part_procline_detail) aa01
          where 方镀三线 is not  null
          ) j  on a.area=j.area and a.machine_name=j.machine_name and a.type=j.type
          order by a.area desc,a.machine_name desc
        
        ''')

    res = cursor.fetchall()

    return res


def getPart_contrast(machineType: Optional[str] = ""):
    db = conn.getConn()
    cursor = db.cursor()
    sql = ""
    if machineType != "":
        sql = f'''where type= '{machineType}'  '''

    cursor.execute(f''' 
            
				select * from (

       select IFNULL(e.mdtype,e.type) as type,IFNULL(e.part_spec,e.machine_spesc) as spec,IFNULL(e.kucun,''),IFNULL(e.cx,'') from 
          (
          select * from 
          ( select md.type as mdtype ,md.part_spec,sum(md.balance) as  kucun from part_detail  md  group  by md.part_spec,md.type) a
          left join
          (select mpd.type,mpd.machine_spesc,count(mpd.machine_spesc) as cx from part_procline_detail   mpd group  by mpd.machine_spesc,mpd.type)b
          on a.part_spec=b.machine_spesc  and a.mdtype=b.type
          UNION
          select * from 
          ( select md.type as mdtype,md.part_spec,sum(md.balance) from part_detail  md  group  by md.part_spec,md.type) c
          right join
          (select mpd.type,mpd.machine_spesc,count(mpd.machine_spesc)  from part_procline_detail   mpd group  by mpd.machine_spesc,mpd.type)d
          on c.part_spec=d.machine_spesc  and c.mdtype=d.type
          ) e 
						)aa 
          {sql}
                  
                   ''')
    res = cursor.fetchall()
    print('temp', sql)
    print('res', res)
    return res


async def create_upload_file(flag: Optional[str] = None, imgid: Optional[str] = None, time1:  Optional[str] = None, file: UploadFile = File(...)):
    import os
    try:

        print('进入到上传图片方法里面')
        print(file.filename)
        print(file.content_type)
        print(file.filename)
        print(time1)

        contents = await file.read()
        imgsrc = imgid+"_" + flag+"_" + \
            time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".jpg"
        print('imgsrc==='+imgsrc)
        file = open(
            f"{os.getcwd()}\static\part_procline_imgs\{imgsrc}", "wb")
        file.write(contents)

        # 传到静态地址

        db = conn.getConn()
        cursor = db.cursor()
        cursor.execute('''
          UPDATE `part`.`part_procline_detail`
          SET
          `{2}` = '{0}'
          WHERE
            (`id` = '{1}')
                    '''.format('http://61.185.74.251:5556/static/part_procline_imgs/'+imgsrc, imgid, flag))

        db.commit()
        return '上传成功'
    except Exception:
        print(Exception)
        print('出错')


def addPart_procline_detail(procline, area, part_name, part_spesc, type, username):

    db = conn.getConn()
    cursor = db.cursor()
    sql = f''' 
      INSERT INTO `part_procline_detail` 
( `procline`, `area`, `type`, `machine_name`, `machine_spesc`)
 VALUES ( '{procline}', '{area}', '{type}', '{part_name}', '{part_spesc}')
    '''
    cursor.execute(sql)
    print(sql)
    db.commit()
    print('添加成功')

    # select id from machine_procline_detail where name()
    sql1 = f''' select id from part_procline_detail
    where machine_name='{part_name}'
    and machine_spesc='{part_spesc}' and type='{type}' and procline='{procline}'
    '''
    print(sql1)
    cursor.execute(sql1)

    res = cursor.fetchall()
    part_procline_update_log(
        username, procline, part_spesc, part_name, 1, 'add')
    print('res:', res)
    return res


def deletePart_procline_detail(id, username):

    if id == None:
        return "id为空 出错"

    db = conn.getConn()
    cursor = db.cursor()
    cursor.execute(
        f''' select * from  part_procline_detail where id={id} ''')

    res = cursor.fetchall()
    id = res[0][0]
    procline = res[0][1]
    machine_name = res[0][3]
    machine_spesc = res[0][4]
    cursor.execute(f''' delete from  part_procline_detail where id={id} ''')
    db.commit()
    part_procline_update_log(
        username, procline, machine_spesc, machine_name, 1, 'delete')
    print('删除成功')
    return '删除成功'


def updatepart_procline_detail(id, procline, part_name, part_spec, area, type, username):
    if id == None:
        return "id为空 出错"

    db = conn.getConn()
    cursor = db.cursor()

    cursor.execute(f''' update   part_procline_detail
                   
                   set procline='{procline}',
                       machine_name='{part_name}',
                       machine_spesc='{part_spec}',
                       type='{type}',
                       area='{area}',
                       update_date='{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}'
                   where id={id}  
                 
                   ''')
    db.commit()

    part_procline_update_log(
        username, area, part_spec, part_name, 0, 'update')
    print('更新成功')
    return '更新成功'


def part_procline_update_log(
        username: Optional[str] = None,
        area: Optional[str] = None,
        spec: Optional[str] = None,
        item_name: Optional[str] = None,
        count: Optional[int] = 0,
        flag: Optional[str] = None):

    # 更新记录表
    db = conn.getConn()
    cursor = db.cursor()
    print('增加记录')
    if flag == 'add':
        cursor.execute(f''' INSERT INTO `part`.`log` (`username`, `area`, `spec`, `item_name`, `count`, `create_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'add','机修明细');
    ''')
        print("增加记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if flag == 'update':
        cursor.execute(f''' INSERT INTO `part`.`log` ( `username`, `area`, `spec`, `item_name`, `count`, `update_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'update','机修明细');
    ''')
        print("更新记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if flag == 'delete':
        cursor.execute(f''' INSERT INTO `part`.`log` ( `username`, `area`, `spec`, `item_name`, `count`, `update_date`, `flag`,`remark`) 
        VALUES ('{username}', '{area}', '{spec}', '{item_name}', '{count}', '{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}', 'delete','机修明细');
    ''')
        print("更新记录完成 " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db.commit()


def getProclinePartTypes():
    db = conn.getConn()
    cursor = db.cursor()
    sql = f''' 

        select type from(
        select type from part_detail group by  type
        UNION
        select type from part_procline_detail group by  type
        ) aa
        group by aa.type

 '''
    cursor.execute(sql)
    res = cursor.fetchall()
    return res
