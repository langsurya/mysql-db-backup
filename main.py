#!/usr/bin/python
import sys
import configparser
import datetime
import time
from myObject import *
import TelegramBot as tele
import argparse
from prettytable import PrettyTable
import pathlib


print("MySQL Copy Table Tool - v2.0.0")

class Main:
    def __init__(self, table):
        self._table = table
        self._config()
        self._connect()

    def _config(self):
        try:
            config = configparser.ConfigParser()
            config_file_name = pathlib.Path(__file__).parent.absolute() / "config.ini"
            config.read(config_file_name)

            self._table_name = "`%s`" % (self._table)
            # source data
            self.src_host=config["src"]["host"];        self.src_user=config["src"]["user"];
            self.src_passwd=config["src"]["passwd"];    self.src_dbname=config["src"]["schema"];
            self.src_table_full_name = "`%s`.%s" % (self.src_dbname, self._table_name)

            # destination
            self.dst_host=config["dst"]["host"];        self.dst_user=config["dst"]["user"];
            self.dst_passwd=config["dst"]["passwd"];    self.dst_dbname=config["dst"]["schema"];
            self.dst_table_full_name = "`%s`.%s" % (self.dst_dbname, self._table_name)
            self.main_import_data=config["main"]["import_data"]
        except Exception as e:
            print("Error reading file " + config_file_name)
            sys.exit(1)

    def _connect(self):
        try:
            # connect source DB
            self._source = BCK(self.src_host, self.src_user, self.src_passwd, self.src_dbname)
            # connect destination DB
            self._target = BCK(self.dst_host, self.dst_user, self.dst_passwd, self.dst_dbname)

            conn = "Connected to %s AND %s ..." % (self.src_host, self.dst_host);
        except Exception as e:
            print(e)
            sys.exit(1)
        # print(conn)

    def _get_ddl_sql_result(self):
        operation_msg="Copying"; operation_success_msg="Copy"; import_data_msg="";

        if self.main_import_data == "True":
            import_data_msg = "with data"

        message = "%s %s to %s %s..." % (operation_msg,self.src_table_full_name,self.dst_table_full_name,import_data_msg)

        # DDL Information
        self.create_tbl_sql = self._source.get_ddl_information(self._table_name)
        # GET query for insert
        self.insert_tbl_sql = self._source.get_sql_insert()
        # get data
        self._source_result = self._source.read()

        print(message);
        return message

    def _run(self):
        # drop table destination/_target
        self._target.drop_n_create_tbl(self.create_tbl_sql, self.dst_table_full_name)

        if self.main_import_data == "True":
            # insert many data
            self._target.insert_many(self.insert_tbl_sql, self._source_result)
            rows = len(self._source_result)
            total_rows = str(rows)

            return total_rows;

start = time.time()
tbls = None

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-t", "--Table", help = "Get Tables")
# Read arguments from command line
args = parser.parse_args()

if args.Table:
    tbls = args.Table
    tbls = tbls.split(",")
    print("Displaying Output as: %s" % args.Table)
tbl = []

t = PrettyTable(['Table Name', 'Count', 'Times'])
t.align = "l"
# print(t)
# sys.exit(1)

if tbls is None:
    print("tables is None")
    sys.exit(1)

if tbls is not None:
    for x in tbls:
        # time start
        in_start = time.time()
        # Main backup
        main = Main(x)
        main._get_ddl_sql_result()
        result = main._run()
        # time finish
        fnst = str(datetime.timedelta(seconds=int(time.time() - in_start)))
        # add row tables
        t.add_row([x, result, fnst])

    cons = "\nFinished in [" + str(datetime.timedelta(seconds=int(time.time() - start))) + "]"
    print(str(t))
    sendtbl = f'<pre>{t}</pre>'
    cc=None
    tele.TelegramBot("%s %s" % (sendtbl, cons), cc);