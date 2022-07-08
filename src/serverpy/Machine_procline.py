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
          
          select a.*,b.圆镀一线,c.圆镀二线,d.圆镀三线,e.圆镀四线,f.圆镀五线,g.圆镀六线,h.方镀一线,i.方镀二线,j.方镀三线 from 

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
