

import pymysql


def getConn():

    db = pymysql.connect(host='192.168.3.160',
                         port=3306,
                         user='part',
                         passwd='part',
                         db='part',
                         charset='utf8')

    return db
