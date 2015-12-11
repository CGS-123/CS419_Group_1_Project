import curses
import psycopg2
from query import query
from menu import Menu
from screenmanager import ScreenManager

class DatabaseManager(object):       
    def __init__(self, stdscreen, userpass):
        self.username = userpass['user']
        self.password = userpass['pass']
        self.screen = stdscreen
        self.dimensions = self.screen.getmaxyx() 
        self.screen_manager = ScreenManager(self.screen)
        self.all_databases_query = "SELECT datname FROM pg_database WHERE datistemplate = false"
        self.all_tables_query = "SELECT table_schema,table_name FROM information_schema.tables ORDER BY table_schema,table_name;"
        self.current_database = None
        
    #Database query methods
    def fetch_all_databases(self):
        databases = query.query(self.all_databases_query, 'postgres', self.screen, 0, None, self.username, self.password)
        return databases[1]
        
    def create_database(self, name):
        to_query = "SELECT 1 FROM pg_database WHERE datname = \'%s\'" % (name)
        database_exists = query.query(to_query, 'postgres', self.screen, 0, None, self.username, self.password)
        if database_exists[1]:
            ScreenManager.throw(self.screen, 'Database already exists.')
            return False
        else:
            db_creation_query = "CREATE DATABASE " + name 
            if query.query(db_creation_query, 'postgres', self.screen, 0, None, self.username, self.password) == -1:
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
            headeroptions = {'title':"List of Databases",'user':self.username}
            displayDatabasesMenu = Menu(parsed_dbs, self.screen, headeroptions)
            displayDatabasesMenu.display()

    #Display methods
    def display_all_databases_opt(self, action):   
        parsed_dbs = []
        databases = self.fetch_all_databases()
        if databases is not None:
            for db in databases:
                lst = (str(db[0]),action,str(db[0]))
                parsed_dbs.append(tuple(lst))
            headoptions = {'title':"Select Database",'user':self.username}
            displayDatabasesMenu = Menu(parsed_dbs, self.screen, headoptions)
            displayDatabasesMenu.display()
    
    def display_all_copy_database(self):   
        parsed_dbs = []
        databases = self.fetch_all_databases()
        if databases is not None:
            for db in databases:
                lst = list(db)
                lst.append(self.copy_database)
                lst.append(db)
                parsed_dbs.append(tuple(lst))
            headoptions = {'title':"Select Database to Copy",'user':self.username}
            displayDatabasesMenu = Menu(parsed_dbs, self.screen, headoptions)
            displayDatabasesMenu.display()
    
    def display_all_delete_database(self):   
        parsed_dbs = []
        databases = self.fetch_all_databases()
        if databases is not None:
            for db in databases:
                lst = list(db)
                lst.append(self.drop_database)
                lst.append(db)
                parsed_dbs.append(tuple(lst))
            headoptions = {'title':"Select Database to delete",'user':self.username}
            displayDatabasesMenu = Menu(parsed_dbs, self.screen, headoptions)
            displayDatabasesMenu.display()
            
    def copy_database(self, database):
        db_name = database[0]
        
        self.screen_manager.set_cursor_visible()
        curses.echo()
        self.screen_manager.display_mid("Please enter a name for the new database: ")
        new_db_name = self.screen_manager.screen.getstr()
        self.screen.clear()
        
        db_copy_query = "CREATE DATABASE " + new_db_name + " WITH TEMPLATE " + db_name
        if query.query(db_copy_query, 'postgres', self.screen, 0, None, self.username, self.password) == -1:
            ScreenManager.throw(self.screen, "An error prevented database creation.")
        else:
            self.screen_manager.display_mid("The database " + new_db_name + " has been copied from " + db_name)
            self.screen.getstr()
        self.screen.clear()
        self.screen_manager.set_cursor_invisible()
        
    def drop_database(self, database):
        db_name = database[0]
        
        self.screen_manager.set_cursor_visible()
        curses.echo()
        self.screen_manager.display_mid("Are you sure you want to delete " + db_name + "? (Y/N): ")
        confirmation = self.screen_manager.screen.getstr()
        if confirmation == 'Y':
            db_delete_query = "DROP DATABASE " + db_name
            if query.query(db_delete_query, 'postgres', self.screen, 0, None, self.username, self.password) == -1:
                ScreenManager.throw(self.screen, "An error prevented database creation.")
            else:
                self.screen_manager.display_mid("The database " + db_name + " has been deleted")
                self.screen.getstr()
        else:
            self.screen_manager.display_mid(db_name + " will not be deleted")
            self.screen_manager.screen.getstr()
        self.screen.clear()
        self.screen_manager.set_cursor_invisible()            
    
    def create_new_database(self):
        self.screen_manager.set_cursor_visible()
        curses.echo()
        self.screen_manager.display_mid("Please enter a name for the new database: ")
        database_name = self.screen_manager.screen.getstr()
        self.screen.clear()
        try:
           did_create_database = self.create_database(database_name)
        except RuntimeError as rt_error:
           self.screen_manager.display_mid("Error with the database creation query")
        else:
            if did_create_database is True:
                self.screen_manager.display_mid("The database " + database_name + " has been created")
                self.screen.getstr()
        self.screen.clear()
        self.screen_manager.set_cursor_invisible()
