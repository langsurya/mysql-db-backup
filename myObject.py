#!/usr/bin/python
import pymysql
import sys
# for send bot telegram
import TelegramBot as tele

class BCK:
    def __init__(self, host="localhost", user="root", psswd="", database=""):
        self.__localhost     = host
        self.__username      = user
        self.__password      = psswd
        self.__database      = database
        self.createConnection()
    
    # dapatkan data dari table source
    def read(self):
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM "+self.__table_name+"")

            return cursor.fetchall()
        except Exception as e:
            tele.TelegramBot(e)
            return False;

    # Get DDL Information
    def get_ddl_information(self, table):
        self.__table_name = table
        try:
            cursor = self.__db.cursor()
            cursor.execute("SHOW CREATE TABLE "+ self.__table_name)
            myresult = cursor.fetchone()

            self._create_table_sql = myresult[1]
            return self._create_table_sql
        except Exception as e:
            tele.TelegramBot(e)
            sys.exit(1)

    # get sql "INSERT IGNORE INTO table_name (fields, ...) VALUES (%s, ...)" otomatis
    def get_sql_insert(self):
        try:
            cursor = self.__db.cursor()
            # source table for create Query INSERT IGNORE
            cursor.execute("SHOW COLUMNS FROM "+ self.__table_name)
            myresult = cursor.fetchall()

            fields_name = []
            fields_values = []
            for record in myresult:
                fields_name.append("`"+record[0]+"`")
                fields_values.append("%s")

            fields = ', '.join(fields_name)
            values = ', '.join(fields_values)

            # query insert destination
            insert_sql = f"""INSERT IGNORE INTO {self.__table_name} ({fields}) VALUES ({values})"""

            return insert_sql
        except Exception as e:
            tele.TelegramBot(e)
            sys.exit(1)

    # masuk ke DB target yg masu di insert
    def drop_n_create_tbl(self, create_table_sql, dst_table_full_name):
        try:
            cursor = self.__db.cursor()
            dst_table_remove = "DROP TABLE IF EXISTS "+ dst_table_full_name +";"
            # drop table if exist
            cursor.execute(dst_table_remove)
            # create ulang table if exist
            cursor.execute(create_table_sql)
        except Exception as e:
            tele.TelegramBot(e)
            sys.exit(1)

    # insert many
    def insert_many(self, insert_query, records):
        try:
            cursor = self.__db.cursor()
            cursor.executemany(insert_query, records)
            self.__db.commit()
        except Exception as e:
            print("Error insert to database")
            tele.TelegramBot(e)
            sys.exit(1)

    def createConnection(self):
        self._error = ''
        try:
            db = pymysql.connect(
                host=self.__localhost,
                user=self.__username,
                passwd=self.__password,
                database=self.__database
            )

            self.__db = db
        except Exception as e:
            print("Error connecting database")
            tele.TelegramBot(e)
            sys.exit(1)
  