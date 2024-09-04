import time
import mysql.connector as mysql_connector
import datetime
from . import dates
import multiprocessing
import sqlite3

def mysql(user='', password='', host='', database=''):
    return SQL_Class(user=user, password=password, host=host, database=database)

def sqlite3(path=''):
    return SQL_Class('sqlite', path = path)


modes = ['mysql', 'sqlite']

class SQL_Class:

    def __init__(self, mode='mysql', **kwargs):
        if mode not in modes:
            raise NotSupportedMode
        self.mode = mode
        self.db = None
        self.cursor = None

        self.tabels = []
        self.database = ''
        self.host = 'localhost'
        self.user = ''
        self.password = ''
        self.path = ''

        if kwargs != {}:
            self.login(**kwargs)

    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
        except Exception:
            pass

    def login(self, **kwargs):
        if self.mode == modes[0]:  
            self.host = kwargs['host'] 
            self.password = kwargs['password']
            self.user = kwargs['user']
            self.database = kwargs['database']
            self.tabels = kwargs['tables']
            self.connect_mysql()

        if self.mode == modes[1]:
            self.path = kwargs['path']
            self.connect_sqlite()

    def connect_mysql(self):
        self.db = mysql_connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.db.cursor()

    def connect_sqlite(self):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

    def ifconnected(self):
        if self.cursor == '':
            return False
        else:
            return True
        
    def table_str(self, tabels=None, return_first=False):
        if tabels is None:
            tabels = [x for x in self.tabels]
        for x in range(len(tabels)):
            if self.mode == 'mysql':
                tabels[x] = f'{tabels[x]}'
            if self.mode == 'sqlite':
                tabels[x] = f'{tabels[x]}'
        if not return_first:
            return ', '.join(tabels)
        else:
            return tabels[0]
        
    def select_str(self, *args):
        if len(args) == 0:
            select = '*'
        else:
            select = ', '.join(args)
        return select

    def where_construct(self, **kwargs):
        elements = list()
        for x in kwargs:
            elements.append(f"{x} = '{kwargs[x]}'")
        elements = ' and '.join(elements)
        return elements

    def reset_auto_increment(self):
        self.Execute_SQL_Command(f'ALTER TABLE `{self.table_str()}`  AUTO_INCREMENT = 1')
        self.db.commit()

    def clear_table(self):
        self.Execute_SQL_Command(f'DELETE FROM `{self.table_str()}`')
        self.db.commit()

    def basic_read(self, tabels=None, *args, **kwargs):
        if not self.ifconnected():
            raise NotConnected
        tabels_str = self.table_str(tabels)
        select = self.select_str(*args)
        elements = self.where_construct(**kwargs)
        if kwargs == {}:
            Abfrage = f'SELECT {select} FROM {tabels_str}'
        else:
            Abfrage = f'SELECT {select} FROM {tabels_str} WHERE {elements}'
        Return = self.Execute_SQL_Command(Abfrage)
        return Return

    def basic_write(self, tabels=None, **kwargs):
        if not self.ifconnected():
            raise NotConnected
        tabels_str = self.table_str(tabels, True)
        colums = []
        for x in kwargs:
            colums.append(x)
        values = []
        for x in kwargs:
            values.append(kwargs[x])
        for x in range(len(values)):
            values[x] = f"'{values[x]}'"
        colums = ', '.join(colums)
        values = ', '.join(values)
        Abfrage = f'INSERT INTO {tabels_str} ({colums}) VALUES ({values})'
        self.Execute_SQL_Command(Abfrage)
        self.db.commit()

    def basic_delete(self, tabels=None, **kwargs):
        if not self.ifconnected():
            raise NotConnected
        tabels_str = self.table_str(tabels, True)
        elements = self.where_construct(**kwargs)
        Abfrage = f'DELETE FROM {tabels_str} WHERE {elements}'
        self.Execute_SQL_Command(Abfrage)
        self.db.commit()

    def Execute_SQL_Command(self, command:str):
        print(command)
        self.cursor.execute(command)
        return self.cursor.fetchall()

class NotConnected(Exception):

    pass

class NotSupportedMode(Exception):

    pass

class auto_delete():

    def __init__(self, tabel:str, colum:str, Buffertime:list, SQL:SQL_Class = None): # Buffertime: [name:(days, months, years, minutes, seconds, hours), time:int]
        self.SQL = SQL
        self.tabel = tabel
        self.colum = colum
        self.Buffertime = Buffertime
        self.Process = None
        self.setup()

    def setup(self):
        self.SQL.tabels = [self.tabel]
        self.Process = multiprocessing.Process(target=self.exe)

    def delete_if_too_old_date(self):
        dates_list = self.SQL.basic_read(None, self.colum)
        dates_list = [dates.format(x[0]) for x in dates_list]
        dates_delete = []
        for x in dates_list:
            if 'months' == self.Buffertime[0]:
                if dates.add(x, months=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'days' == self.Buffertime[0]:
                if dates.add(x, days=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'years' == self.Buffertime[0]:
                if dates.add(x, years=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'minutes' == self.Buffertime[0]:
                if dates.add(x, minutes=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'seconds' == self.Buffertime[0]:
                if dates.add(x, seconds=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'hours' == self.Buffertime[0]:
                if dates.add(x, hours=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
        print(dates_delete)
        for x in dates_delete:
            self.SQL.Execute_SQL_Command(f"DELETE FROM `{self.SQL.database}`.`{self.tabel}` WHERE (`{self.colum}` = '{x}')")
        self.SQL.db.commit()

    def exe(self):
        while True:
            try:
                self.delete_if_too_old_date()
            except Exception:
                print(Exception)

    def run(self):
        multiprocessing.freeze_support()
        self.Process.start()

    def stop(self):
        self.Process.terminate()