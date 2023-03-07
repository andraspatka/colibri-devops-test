from .mysql_conn import MysqlConnection

import glob
import logging

import time

DB_CONNECTION_TIMEOUT = 90

def wait_for_db_ready(host, user, password, port):
    """
    Waits until the database becomes available or until DB_CONNECTION_TIMEOUT is reached
    :return: True if the database connection was successful. Raises an exception otherwise
    """
    for s in range(0, DB_CONNECTION_TIMEOUT):
        logging.info("Trying to connect to Mysql DB")
        try:
            with MysqlConnection(host=host, user=user, password=password, port=port) as conn:
                cur = conn.connector.cursor()
                cur.execute("SELECT VERSION()")
                results = cur.fetchone()
                
                # Check if anything at all is returned
                if results:
                    logging.info("Mysql database UP!")
                    return True
        except Exception as e:
            logging.debug("Mysql database NOT up. Sleeping then trying again...")
            logging.debug(e)
        time.sleep(1)
    error_msg = "MySQL Database is not up!"
    logging.error(error_msg)
    raise Exception(error_msg)


def migrate(host, port, user, password, db_name, db_scripts):
    wait_for_db_ready(host=host, user=user, password=password, port=port)

    migration_scripts = glob.glob(f"{db_scripts}/*.sql")
    migration_scripts.sort()

    logging.debug(migration_scripts)