import mysql.connector
import time
from configparser import ConfigParser


class Database:

    table_name = 'onlineData'
    config_file = 'config.ini'
    connection = None

    def __init__(self, config_file):
        self.config_file = config_file
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.read_config())
        except mysql.connector.Error as e:
            print('DB Error:', e)

        self.check_connection()

    def check_connection(self):
        if self.connection and self.connection.is_connected():
            print('Connected to MySQL database')
            return
        else:
            print('Retrying connection to mysql server in 5 seconds...')
            time.sleep(5)
            self.connect()

    def read_config(self):
        # create parser and read ini configuration file
        parser = ConfigParser()
        parser.read(self.config_file)

        # get section, default to mysql
        db = {}
        section = 'mysql'
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the config.ini file'.format(section))

        return db

    def query(self, sql, data=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
        except mysql.connector.Error:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
        self.connection.commit()
        return cursor
