import argparse
import logging

from utils.db_op import migrate

parser = argparse.ArgumentParser(description='Run migration scripts')

parser.add_argument('dbscripts', help='Path to the DB migration scripts.')
parser.add_argument('dbuser', help='DB username.')
parser.add_argument('dbserver', help='DB server url.')
parser.add_argument('dbname', help='Name of the Database.')
parser.add_argument('dbpassword', help='DB Password.')

parser.add_argument('--debug', '-d', action='store_true')

args = parser.parse_args()

if args.debug:
    level=logging.DEBUG
else:
    level=logging.INFO

logging.basicConfig(level=level) 

logging.debug(f'Script called with parameters: dbscripts: {args.dbscripts}, dbuser: {args.dbuser}, dbserver: {args.dbserver}, dbname: {args.dbname}, dbpassword: {args.dbpassword}')

migrate(host=args.dbserver, port=3306, user=args.dbuser, password=args.dbpassword, db_name=args.dbname, db_scripts=args.dbscripts)
