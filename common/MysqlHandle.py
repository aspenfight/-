import pymysql
from common.helper import *


class HandleMysql:
    def __init__(self):
        dbinfo = dict(map(lambda x: (x[0], x[1]), get_config_items(pathUartConfig,'db')))
        self.conn = pymysql.connect(host = dbinfo['host'],
                                   user = dbinfo['user'],
                                   password = dbinfo['password'],
                                   database = dbinfo['database'],
                                   port = int(dbinfo['port']),
                                   charset = dbinfo['charset'],
                                   cursorclass =pymysql.cursors.DictCursor)

        self.cur = self.conn.cursor()

    def query_sql(self,sql,args=None,is_all=False):
        """
        查询sql
        :param sql:
        :param args:
        :param is_all:
        :return:
        """
        self.cur.execute(sql,args)
        self.conn.commit()
        if is_all:
            return self.cur.fetchall()
        else:
            return self.cur.fetchone()

    def execute(self, sqls):
        """
        增删改
        :param sql:
        :return:
        """
        try:
            for i in sqls:
                self.cur.execute(i)
        except Exception as e:
            print("执行增删改有错，错误是{}，需要回滚".format(e))
            self.conn.rollback()
        #     增删改操作有误时回滚操作
        else:
            self.conn.commit()
            print("事务提交成功")