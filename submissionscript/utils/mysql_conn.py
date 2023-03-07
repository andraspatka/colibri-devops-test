from mysql.connector import MySQLConnection

import logging
import os

class MysqlConnection(object):
    '''
    MySQL Database connection class
    Can be used with python context mangers:
    with MysqlConnection(host, user, password, port) as conn:
        data = pd.read_sql(sql, conn.connector)
    '''

    def __init__(self, host, user, password, port):
        self.connector = None
        self.host, self.user, self.password, self.port = host, user, password, port

    def __init__(self):
        self.connector = None
        self.host, self.user, self.password, self.database = os.environ['DB_HOST'], os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_NAME']
        if 'PORT' not in os.environ:
            self.port = 3306
        else:
            self.port = os.environ['PORT']

    def __enter__(self):
        logging.debug(f'Creating connection with parameters: host {self.host}, user {self.user}, port {self.port}')
        self.connector = MySQLConnection(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
        )
        
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_tb is None:
            self.connector.commit()
        else:
            self.connector.rollback()
        self.connector.close()