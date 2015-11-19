import curses
import psycopg2
from query import query
from error import error
from menu import Menu
from screenmanager import ScreenManager
from databaseManager import DatabaseManager

class TableManager(object):
    def __init__(self,stdscreen):
        self.screen = stdscreen
        self.screen = stdscreen
        self.dimensions = self.screen.getmaxyx() 
        self.screen_manager = ScreenManager(self.screen)
        self.db_mgr = DatabaseManager(self.screen)


    def listTables(self):
        query = """
        SELECT table_name
        FROM information_schema.tables
        where table_schema = 'public'
        """
        #make connection between python and postgresql
        conn = psycopg2.connect("dbname='worlddb' user='vagrant' password='vagrant'")
        cur = conn.cursor()

        cur.execute(query)
        rows = cur.fetchall()
        parsed_table_menu = []
        for datas in rows:
            lst = (str(datas[0]),curses.flash)
            parsed_table_menu.append(tuple(lst))
        table_menu = Menu(parsed_table_menu,self.screen)
        table_menu.display()
