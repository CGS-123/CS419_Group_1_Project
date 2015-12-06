import curses
import psycopg2
from query import query
from error import error
from menu import Menu
from screenmanager import ScreenManager
from databaseManager import DatabaseManager
from query import query

class TableManager(object):
    def __init__(self,stdscreen):
        self.screen = stdscreen
        self.dimensions = self.screen.getmaxyx() 
        self.screen_manager = ScreenManager(self.screen)

    def listTables(self, dbname):
        table_query = "SELECT table_name FROM information_schema.tables where table_schema = 'public'"
        rows = query.query(table_query, dbname, self.screen)
        parsed_table_menu = []
        for datas in rows[1]:
            lst = (str(datas[0]),curses.flash)
            parsed_table_menu.append(tuple(lst))
        table_menu = Menu(parsed_table_menu,self.screen)
        table_menu.display()
        
    def createTable(self, dbname):
        self.screen_manager.set_cursor_visible()
        curses.echo()
        self.screen_manager.display_mid("Please enter a name for the new table: ")
        new_table_name = self.screen_manager.screen.getstr()
        self.screen.clear()
        
        table_creation_query = "CREATE TABLE IF NOT EXISTS " + new_table_name + "(ID INT PRIMARY KEY      NOT NULL);" 
        if query.query(table_creation_query, dbname, self.screen, 0) == -1:
            ScreenManager.throw(self.screen, "An error prevented table creation.")
        else:
            self.screen_manager.display_mid("Table successfully created!")
            self.screen_manager.screen.getstr()
        self.screen.clear()