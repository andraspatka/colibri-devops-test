from .mysql_conn import MysqlConnection

import glob
import logging

import time

DB_CONNECTION_TIMEOUT = 90

def wait_for_db_ready():
    '''
    Waits until the database becomes available or until DB_CONNECTION_TIMEOUT is reached
    :return: True if the database connection was successful. Raises an exception otherwise
    '''
    for s in range(0, DB_CONNECTION_TIMEOUT):
        logging.info('Trying to connect to Mysql DB')
        try:
            with MysqlConnection() as conn:
                cur = conn.connector.cursor()
                cur.execute('SELECT VERSION()')
                results = cur.fetchone()
                
                # Check if anything at all is returned
                if results:
                    logging.info('Mysql database UP!')
                    return True
        except Exception as e:
            logging.debug('Mysql database NOT up. Sleeping then trying again...')
            logging.debug(e)
        time.sleep(1)
    error_msg = 'MySQL Database is not up!'
    logging.error(error_msg)
    raise Exception(error_msg)


def get_data(query):
    with MysqlConnection() as conn:
        cur = conn.connector.cursor(dictionary=True)
        cur.execute(query)
        rows = []
        for row in cur:
            print(row)
            rows.append(row)
        return rows


def migrate(db_scripts):
    wait_for_db_ready()

    migration_scripts = glob.glob(f'{db_scripts}/*.sql')
    migration_scripts.sort()

    logging.debug(f'Migration scripts: migration_scripts')

    try:
        current_db_version = get_data(f"SELECT version FROM versionTable;")[0]['version']
    except Exception as e:
        logging.error("Unable to determine database version!")
        logging.error(e)
    
    logging.info(f'Current database version is: {current_db_version}')
