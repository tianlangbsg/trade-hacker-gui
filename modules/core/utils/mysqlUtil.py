import queue

import pymysql
from modules.core.config import configManager
import modules.core.utils.logUtil as log

# 数据库配置信息
DATABASE_HOST = configManager.get(section='database', option='database_host')
DATABASE_PORT = configManager.get_int(section='database', option='database_port')
DATABASE_USERNAME = configManager.get(section='database', option='database_username')
DATABASE_PASSWORD = configManager.get(section='database', option='database_password')
DATABASE_NAME = configManager.get(section='database', option='database_name')
DATABASE_CHARSET = configManager.get(section='database', option='database_charset')

# 连接池
class ConnectionPool(object):
    def __init__(self, **kwargs):
        self.size = kwargs.get('size', 10)
        self.kwargs = kwargs
        self.conn_queue = queue.Queue(maxsize=self.size)
        for i in range(self.size):
            self.conn_queue.put(self._create_new_conn())

    def _create_new_conn(self):
        return pymysql.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USERNAME, password=DATABASE_PASSWORD,
        database=DATABASE_NAME,
        charset=DATABASE_CHARSET)

    def _put_conn(self, conn):
        self.conn_queue.put(conn)

    def _get_conn(self):
        conn = self.conn_queue.get()
        if conn is None:
            self._create_new_conn()
        return conn

    def exec_sql(self, sql, params):
        conn = self._get_conn()
        try:
            # 获取一个光标
            cursor = conn.cursor()
            result = cursor.execute(sql, params)
            conn.commit()
            cursor.close()
            return result
        except Exception as ex:
            log.error('数据库执行异常:' + ex.__str__())
            raise ex
        finally:
            self._put_conn(conn)

    def query_sql(self, sql):
        conn = self._get_conn()
        try:
            # 获取一个光标
            cursor = conn.cursor()
            # 执行sql语句
            cursor.execute(sql)
            # 取到查询结果
            result = cursor.fetchall()
            conn.commit()
            cursor.close()
            return result
        except Exception as ex:
            log.error('数据库查询异常:' + ex.__str__())
            raise ex
        finally:
            self._put_conn(conn)

    def __del__(self):
        try:
            while True:
                conn = self.conn_queue.get_nowait()
                if conn:
                    conn.close()
        except queue.Empty:
            pass

# 初始化连接池
connectionPool = ConnectionPool()


# 执行SQL
def execute(sql,params):
    return connectionPool.exec_sql(sql,params)


# 查询SQL
def query(sql):
    return connectionPool.query_sql(sql)

