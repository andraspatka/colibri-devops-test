from .mysql_conn import MysqlConnection

import glob
import logging

import time
import re

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
    '''
    Runs the query defined in :query: and returns the results
    :return: list of rows returned by the query
    '''
    with MysqlConnection() as conn:
        cur = conn.connector.cursor(dictionary=True)
        cur.execute(query)
        rows = []
        for row in cur:
            print(row)
            rows.append(row)
        return rows


def migrate(db_scripts):
    '''
    Runs the SQL scripts under the folder :db_scripts:
    Runs them in ascending order based on the version which is defined in the script name. Unversioned scripts are not executed.
    Only executes scripts if the script version is lower than the database version defined in the table versionTable.
    '''
    wait_for_db_ready()
    try:
        current_db_version = int(get_data(f'SELECT version FROM versionTable;')[0]['version'])
    except Exception as e:
        logging.error('Unable to determine database version!')
        logging.error(e)
    
    logging.info(f'Current database version is: {current_db_version}')

    migration_scripts = glob.glob(f'{db_scripts}/*.sql')
    migration_scripts.sort()

    logging.debug(f'Migration scripts: {migration_scripts}')

    for script in migration_scripts:
        try:
            # regex to extract script version. Skip leading 0 if exists, capture rest of the numbers
            script_version = int(re.search('0?(\d+)', script).group(1))
        except Exception as e:
            logging.warn(f'No version information in script: {script}. Skipping it...')
            continue

        logging.debug(f'Script {script} has version {script_version}')
        if current_db_version < script_version:
            with open(script, 'r') as f:
                script_content = f.read()
                logging.debug(f'Content of {script} is {script_content}')

                with MysqlConnection() as conn:
                    cur = conn.connector.cursor(dictionary=True)

                    for result in cur.execute(script_content, multi=True):
                        logging.info(result.statement)

                    cur.execute('UPDATE versionTable set version=%s', (script_version,))
                    logging.info(f'Executed script: {script} successfully!')



