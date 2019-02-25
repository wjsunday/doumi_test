#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/23 9:58
# @Author  : HT
# @Site    : 
# @File    : MySqlOperationer.py
# @Software: PyCharm Community Edition
# @Describe: Desc
# @Issues  : Issues


import pymssql
class MySqlOperationer(object):
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def execQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        self.conn.close()
        return resList

    def execNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def execNonQuerys(self,sqls):
        cur = self.__GetConnect()
        for sql in sqls:
            try:
                cur.execute(sql)
                self.conn.commit()
            except Exception as error:
                # print('插入失败的语句\n %s'% (sql))
                print('失败原因 \n %s'%(error))

                # quit(0)
            # except

        self.conn.close()

my_mssql =  MySqlOperationer(host="192.168.6.37", user="da_ht", pwd="ht_123456", db="fengmingdw")