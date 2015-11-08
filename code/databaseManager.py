import curses
import psycopg2
from query import query
from error import error

class DatabaseManager:       
    def __init__(self):
        self.screen = curses.initscr()
        self.allDatabasesQuery = "SELECT datname FROM pg_database WHERE datistemplate = false"
        self.allTablesQuery = "SELECT table_schema,table_name FROM information_schema.tables ORDER BY table_schema,table_name;"
        
    def fetch_all_databases(self):
        databases = query.query(self.allDatabasesQuery, 'postgres', self.screen)
        return databases
