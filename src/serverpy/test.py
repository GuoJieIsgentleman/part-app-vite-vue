<<<<<<< HEAD
=======
import pinyin
>>>>>>> e5b1217 (gongzhuang)
import hmac
import base64
import time
import pymysql

# def checkconn():
#     db = pymysql.connect(host='192.168.3.160', port=3306,
#                          user='part', passwd='part', db='part', charset='utf8')
#     cursor = db.cursor()
#     cursor.execute("select * from user")
#     data = cursor.fetchone()
#     print(data)

# def generate_token(key):
#     """
#     @Args:
#         key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
#         expire: int(最大有效时间，单位为s)
#     @Return:
#         state: str
#     :param key:
#     :param expire:
#     :return:
#     """
#     ts_str = str(time.time())
#     ts_byte = ts_str.encode("utf-8")
#     sha1_tshex_str = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
#     token = ts_str+':'+sha1_tshex_str
#     b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))

#     return b64_token.decode("utf-8")

<<<<<<< HEAD
#测试获取路由列表
=======
# 测试获取路由列表
>>>>>>> e5b1217 (gongzhuang)
# @app.get('/getroutes')
import os
import json


def getroutes():

    routes = ''
    routes = open(
        r'C:\Users\Administrator\Desktop\Demo\vue-next-admin\src\serverpy\static\adminMenu.json'
    )
    a = json.load(routes)
    print(a)


<<<<<<< HEAD
getroutes()
=======
def getConn():

    db = pymysql.connect(host='192.168.3.160',
                         port=3306,
                         user='part',
                         passwd='part',
                         db='part',
                         charset='utf8')

    return db


def test(machine_part_name, new_area):
    db = getConn()
    cursor = db.cursor()
    sql = f''' select count(id) from machine_parts_detail where machine_part_name='{machine_part_name}' and area='{new_area}' '''

    cursor.execute(sql)
    rs = cursor.fetchone()
    print(rs[0])
# test('A1008', '值班室备件库一楼')


def tools():

    a = '成套保养_A1000_123'
    x = a.split('_')
    print(x)
    print(x[1])


def getcode():
    return pinyin.get_initial('aaa', delimiter="_")


print(getcode())
>>>>>>> e5b1217 (gongzhuang)
