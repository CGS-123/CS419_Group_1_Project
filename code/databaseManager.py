import curses
import psycopg2
from query import query
from error import error
from menu import Menu
from screenmanager import ScreenManager

class DatabaseManager(object):       
    def __init__(self, stdscreen):
        self.screen = stdscreen
        self.dimensions = self.screen.getmaxyx() 
        self.screen_manager = ScreenManager(self.screen)
        self.all_databases_query = "SELECT datname FROM pg_database WHERE datistemplate = false"
        self.all_tables_query = "SELECT table_schema,table_name FROM information_schema.tables ORDER BY table_schema,table_name;"
        self.current_database = None
        
    #Database query methods
    def fetch_all_databases(self):
        databases = query.query(self.all_databases_query, 'postgres', self.screen)
        return databases
        
    def create_database(self, name):
        to_query = "SELECT 1 FROM pg_database WHERE datname = \'%s\'" % (name)
        database_exists = query.query(to_query, 'postgres', self.screen)
        if database_exists:
            ScreenManager.throw(self.screen, 'Database already exists.')
            return False
        else:
            db_creation_query = "CREATE DATABASE " + name 
            if query.query(db_creation_query, 'postgres', self.screen, 0) == -1:
                ScreenManager.throw(self.screen, "An error prevented database creation.")
                return False
            return True
    
    #Display methods
    def display_all_databases(self):   
        parsed_dbs = []
        databases = self.fetch_all_databases()
        if databases is not None:
            for db in databases:
                lst = list(db)
                lst.append(curses.flash)
                parsed_dbs.append(tuple(lst))
            displayDatabasesMenu = Menu(parsed_dbs, self.screen)
            displayDatabasesMenu.display()
    
    def display_all_copy_database(self):   
        parsed_dbs = []
        databases = self.fetch_all_databases()
        if databases is not None:
            for db in databases:
                lst = list(db)
                lst.append(self.copy_database(db[0]))
                parsed_dbs.append(tuple(lst))
            displayDatabasesMenu = Menu(parsed_dbs, self.screen)
            displayDatabasesMenu.display()
            
    def copy_database(self, database):
        self.screen_manager.display_mid(database, self.screen)
    
    def create_new_database(self):
        self.screen_manager.set_cursor_visible()
        self.screen_manager.display_mid("Please enter a name for the new database: ", self.screen)
        database_name = self.screen.getstr()
        self.screen.clear()
        try:
           did_create_database = self.create_database(database_name)
        except RuntimeError as rt_error:
           self.screen_manager.display_mid("Error with the database creation query", self.screen)
        else:
            if did_create_database is True:
                self.display_mid("The database " + database_name + " has been created" , self.screen)
                self.screen.getstr()
        self.screen.clear()
        self.screen_manager.set_cursor_invisible()