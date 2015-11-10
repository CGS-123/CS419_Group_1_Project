import curses
import psycopg2
from query import query
from error import error

class DatabaseManager:       
    def __init__(self):
        self.screen = curses.initscr()
        self.all_databases_query = "SELECT datname FROM pg_database WHERE datistemplate = false"
        self.all_tables_query = "SELECT table_schema,table_name FROM information_schema.tables ORDER BY table_schema,table_name;"
        
    def fetch_all_databases(self):
        databases = query.query(self.all_databases_query, 'postgres', self.screen)
        return databases
        
    def create_database(self, name):
        to_query = "SELECT 1 FROM pg_database WHERE datname = \'%s\'" % (name)
        database_exists = query.query(to_query, 'postgres', self.screen)
        if database_exists:
            error.throw(self.screen, 'Database already exists.')
            return False
        else:
            db_creation_query = "CREATE DATABASE " + name 
            if query.query(db_creation_query, 'postgres', self.screen, 0) == -1:
                error.throw(self.screen, "An error prevented database creation.")
                return False
            return True
        