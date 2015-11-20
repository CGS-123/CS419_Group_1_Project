import sys
import os
import fnmatch
import curses
import psycopg2
from query import query
from menu import Menu
from error import error

class impexp(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
    def export(self, dbname):
        query = """
        SELECT table_name
        FROM information_schema.tables
        where table_schema = 'public'
        """

        #make connection between python and postgresql
        conn = psycopg2.connect("dbname='"+dbname+"' user='vagrant' password='vagrant'")
        cur = conn.cursor()

        cur.execute(query)
        rows = cur.fetchall()

        for datas in rows:
            tablequery = "SELECT * from " + datas[0]
            outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(tablequery)
            myFile = datas[0] + ".csv"
            with open(myFile, 'w') as f:
                cur.copy_expert(outputquery, f)
        conn.close()
        message = "Tables Exported!!!!"
        dimensions = self.screen.getmaxyx() 
        self.screen.addstr(dimensions[0]/2, dimensions[1]/2 - len(message)/2, message, curses.A_BOLD)
    
    def list_sql_files(self):
        top = os.getcwd()
        dir = os.listdir(top)
        parsed_file = []
        count = 0
        for f in dir:
            if fnmatch.fnmatch(f, '*.sql'):
                lst = (str(f), self.import_sql, str(f))
                parsed_file.append(tuple(lst))
                count = 1
        if count == 1:
            sqlfiles = Menu(parsed_file, self.screen)
            sqlfiles.display()
        else:
            error.throw(self.screen, "No .sql files")

    def import_sql(self, file):
        conn = psycopg2.connect("dbname='worlddb' user='vagrant' password='vagrant'")
        cur = conn.cursor()
        cur.execute(open(file, "r").read())
        message = "Import of "+ file +" successful!!"
        dimensions = self.screen.getmaxyx() 
        self.screen.addstr(dimensions[0]/2, dimensions[1]/2 - len(message)/2, message, curses.A_BOLD)





