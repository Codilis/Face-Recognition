import mysql.connector
from mysql.connector import errorcode

class Connection:
    def __init__(self, user, password):
        self.config = {
          'user': user,
          'password': password,
          'host': '127.0.0.1',
          'raise_on_warnings': False,
        }

    def connect(self):
        self.cnx = mysql.connector.connect(**self.config)        
        self.c = self.cnx.cursor()
        try:
            self.c.execute("CREATE DATABASE images")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                pass
        self.c.execute("USE images")

    def create_table(self):
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS names (id integer PRIMARY KEY AUTO_INCREMENT, name varchar(50) UNIQUE)')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists.")
            else:
                print(err.msg)

    def insert_value(self,value):
        idd = self.c.lastrowid
        data = {'id':idd, 'name':value}
        sql = ("INSERT INTO names (id, name) VALUES (%(id)s, %(name)s)")
        x = 0
        try:
            self.c.execute(sql, data)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                print('name already exist')
                x = input('Input 1 to enter more images to dataset ')
        self.cnx.commit()
        return x

    def select_value(self,value):
        sql = ("SELECT * FROM names where name = %(name)s")
        data = {'name':value}
        sel = self.c.execute(sql, data)
        data = self.c.fetchall()
        ids = data[-1][0]
        return ids

    def select_all(self):
        sql = ("SELECT * FROM names")
        sel = self.c.execute(sql)
        data = self.c.fetchall()
        return data

    def close_connection(self):
        self.c.close()
        self.cnx.close()
