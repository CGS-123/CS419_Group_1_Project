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
        headeropts = {'db':dbname,'title':"Select Table to Display"}
        table_menu = Menu(parsed_table_menu,self.screen, headeropts)
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

    def drop_table(self, options):
        table = options['table']
        db = options['db'] 
        self.screen_manager.display_mid("Are you sure you want to delete "+ table + "? (y/n)")
        confirmation = self.screen_manager.screen.getstr()
        if confirmation == 'y' or confirmation == "Y":
            tbl_delete_query = "DROP TABLE " + table + " CASCADE"
            if query.query(tbl_delete_query, db, self.screen, 0) == -1:
                self.screen_manager.display_mid("ERROR deleting table")
                self.screen.getch()
                self.screen.clear()
            else:
                self.screen_manager.display_mid("Table " + table + " deleted.")
                self.screen.getch()
                self.screen.clear()
        else:
            self.screen_manager.display_mid("Table " + table + " will not be deleted.")
            self.screen.getch()
            self.screen.clear()
        self.screen.clear()


    def list_drop_tables(self, dbname):
        table_query = "SELECT table_name FROM information_schema.tables where table_schema = 'public'"
        rows = query.query(table_query, dbname, self.screen)
        parsed_table_menu = []
        for datas in rows[1]:
            opts = {'db':dbname,'table':str(datas[0])}
            lst = (str(datas[0]),self.drop_table, opts)
            parsed_table_menu.append(tuple(lst))
        headeropts = {'db':dbname,'title':"Select Table to Drop"}
        table_menu = Menu(parsed_table_menu,self.screen, headeropts)
        table_menu.display()
