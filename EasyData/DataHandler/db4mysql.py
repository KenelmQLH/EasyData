# coding: utf-8
# create by jialunzhai on 2021/3/30
from contextlib import contextmanager
import pymysql
import time

class MySQLDB:
    """
    MySQL操作类，对MySQL数据库进行增删改查
    """
    def __init__(self, config):
        """
        连接到数据库（保存连接信息，并连接）
        """
        self._config = config
        self.conn = pymysql.connect(**self._config)
        self.print_id()

    def __del__(self):
        """
        关闭数据库连接
        """
        self.conn.close()

    @contextmanager
    def ensureConn(self):
        """
        检查数据库是否需要重连，并在需要时重连
        """
        try:
            self.conn.ping(reconnect=True)
        except BaseException:
            self.conn = pymysql.connect(**self._config)
        yield

    def print_id(self):
        """
        打印mysql连接id
        """
        with self.ensureConn():
            cursor = self.conn.cursor()
            cursor.execute("select connection_id();")
            res = cursor.fetchone()
        print("MySQLDB - mysql id: {}".format(res))
        return res
 
    def excute_sql(self, sql, show_result=False):
        start = time.time()
        self.print_id()
        print("[excute_sql] start : {}".format(sql))
        with self.ensureConn():
            cursor = self.conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            fields = cursor.description

        result = self.format_sql_results(fields, data) 
        column_list = []
        for i in fields:
            column_list.append(i[0])
        if show_result:
            print('Show columns: ',' '.join(column_list))
            print('Show top 100 records: \n',data[:100])

        all_time = time.time() - start
        print("[excute_sql] finish - Use time : {}s".format(all_time))
        return result

    def format_sql_results(self, fields, result):
        # 字段数组 ['id', 'name', 'password']
        field = []
        for i in fields:
            field.append(i[0])
        # 返回的数组集合 形式[{'id': 1, 'name': 'admin', 'password': '123456'}]
        res = []
        for iter in result:
            line_data = dict()
            for index in range(0, len(field)):
                line_data[field[index]] = iter[index]
            res.append(line_data)
        return res
