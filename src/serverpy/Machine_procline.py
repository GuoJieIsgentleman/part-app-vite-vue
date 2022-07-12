import pinyin
import sys
from hmac import new
from fastapi import FastAPI, File, UploadFile
from typing import Optional

import time

from pydantic.main import BaseModel

import connect as conn


# 获取机修件
def getMachine_proclinedetail(procline):
    db = conn.getConn()
    cursor = db.cursor()
    cursor.execute(
        f'''select * from machine_procline_detial where procline='{procline}' ''')

    res = cursor.fetchall()

    return res

# 获取机修产线使用件汇总


def getMachine_proclineSummary():
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
          (select area, machine_name from machine_procline_detial group by area,machine_name) a
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '圆镀一线' then  machine_spesc end '圆镀一线'
          from machine_procline_detial) aa01
          where 圆镀一线 is not  null
          ) b  on a.area=b.area and a.machine_name=b.machine_name
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '圆镀二线' then  machine_spesc end '圆镀二线'
          from machine_procline_detial) aa01
          where 圆镀二线 is not  null
          ) c  on a.area=c.area and a.machine_name=c.machine_name
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '圆镀三线' then  machine_spesc end '圆镀三线'
          from machine_procline_detial) aa01
          where 圆镀三线 is not  null
          ) d  on a.area=d.area and a.machine_name=d.machine_name
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '圆镀四线' then  machine_spesc end '圆镀四线'
          from machine_procline_detial) aa01
          where 圆镀四线 is not  null
          ) e  on a.area=e.area and a.machine_name=e.machine_name
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '圆镀五线' then  machine_spesc end '圆镀五线'
          from machine_procline_detial) aa01
          where 圆镀五线 is not  null
          ) f on a.area=f.area and a.machine_name=f.machine_name
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '圆镀六线' then  machine_spesc end '圆镀六线'
          from machine_procline_detial) aa01
          where 圆镀六线 is not  null
          ) g  on a.area=g.area and a.machine_name=g.machine_name
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '方镀一线' then  machine_spesc end '方镀一线'
          from machine_procline_detial) aa01
          where 方镀一线 is not  null
          ) h  on a.area=h.area and a.machine_name=h.machine_name
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '方镀二线' then  machine_spesc end '方镀二线'
          from machine_procline_detial) aa01
          where 方镀二线 is not  null
          ) i  on a.area=i.area and a.machine_name=i.machine_name
          left join 
          (select * from (
          select 
          area,
          machine_name,
          case procline
          when '方镀三线' then  machine_spesc end '方镀三线'
          from machine_procline_detial) aa01
          where 方镀三线 is not  null
          ) j  on a.area=j.area and a.machine_name=j.machine_name
          order by a.area,a.machine_name
        
        ''')

    res = cursor.fetchall()

    return res


def getmachine_contrast():
    db = conn.getConn()
    cursor = db.cursor()
    cursor.execute(f''' 
          
          select IFNULL(e.part_name,e.machine_name) as name,IFNULL(e.kucun,''),IFNULL(e.cx,'') from 
          (
          select * from 
          ( select md.part_name,count(md.part_spec) as  kucun from machine_detail  md  group  by md.part_name) a
          left join
          (select mpd.machine_name,count(mpd.machine_spesc) as cx from machine_procline_detial   mpd group  by mpd.machine_name)b
          on a.part_name=b.machine_name
          UNION
          select * from 
          ( select md.part_name,count(md.part_spec) from machine_detail  md  group  by md.part_name) c
          right join
          (select mpd.machine_name,count(mpd.machine_spesc)  from machine_procline_detial   mpd group  by mpd.machine_name)d
          on c.part_name=d.machine_name
          ) e
                 
                  
                   ''')
    res = cursor.fetchall()
    return res


async def create_upload_file(flag: Optional[str] = None, imgid: Optional[str] = None, time1:  Optional[str] = None, file: UploadFile = File(...)):

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
            "F:\partapp\part-app-vite-momo\part-app-vite\part-app-vite\src\serverpy\static\machine_procline_imgs\{}".format(imgsrc), "wb")
        file.write(contents)

        # 传到静态地址

        db = conn.getConn()
        cursor = db.cursor()
        cursor.execute('''
          UPDATE `part`.`machine_procline_detial`
          SET
          `{2}` = '{0}'
          WHERE
            (`id` = '{1}')
                    '''.format('http://61.185.74.251:5556/static/machine_procline_imgs/'+imgsrc, imgid, flag))

        db.commit()
        return '上传成功'
    except Exception:
        print(Exception)
        print('出错')


def addmachine_procline_detail(procline, area, part_name, part_spesc, type):

    db = conn.getConn()
    cursor = db.cursor()
    sql = f''' 
      INSERT INTO `machine_procline_detial` 
( `procline`, `area`, `type`, `machine_name`, `machine_spesc`)
 VALUES ( '{procline}', '{area}', '{type}', '{part_name}', '{part_spesc}')
    '''
    cursor.execute(sql)
    print(sql)
    db.commit()
    print('添加成功')

    # select id from machine_procline_detail where name()
    sql1 = f''' select id from machine_procline_detial
    where machine_name='{part_name}'
    and machine_spesc='{part_spesc}' and type='{type}' and procline='{procline}'
    '''
    print(sql1)
    cursor.execute(sql1)

    res = cursor.fetchall()
    print('res:', res)
    return res


def deletemachine_procline_detail(id):

    if id == None:
        return "id为空 出错"

    db = conn.getConn()
    cursor = db.cursor()

    cursor.execute(f''' delete from  machine_procline_detial where id={id} ''')
    db.commit()
    print('删除成功')
    return '删除成功'


def updatemachine_procline_detail(id, procline, part_name, part_spec, area, type):
    if id == None:
        return "id为空 出错"

    db = conn.getConn()
    cursor = db.cursor()

    cursor.execute(f''' update   machine_procline_detial
                   
                   set procline='{procline}',
                       machine_name='{part_name}',
                       machine_spesc='{part_spec}',
                       type='{type}',
                       area='{area}',
                       update_date='{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}'
                   where id={id}  
                 
                   ''')
    db.commit()
    print('更新成功')
    return '更新成功'
