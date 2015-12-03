import curses
import psycopg2
from psycopg2 import extras
from query import query
from error import error
from tableDisplay import tableDisplay

# NOTE: saved/historical queries that would go off the self.screen are not 
# displayed and are not selectable. They are displayed in a stack 
# style with the most recent saved/run queries displayed in a list.
# However, these queries are still saved/recoreded and can be accessed
# by querying the queries db manually.

class queryDB:
    def __init__(self, screen):
        self.screen = screen


    def do(self, dbname):
        self.screen.clear()
        queryDB.display_top_left(self, "Please enter a query to execute below:\n")
        curses.echo()
        string = self.screen.getstr()
        
        queryDB.run(self, string, dbname)


    def save(self):
        self.screen.clear()
        queryDB.display_top_left(self, "Please enter a query save below:\n")
        curses.echo()
        string = self.screen.getstr()
        q = "INSERT INTO queries_saved (query) VALUES (%s)"
        query.query(q, 'queries', None, None, string)
        self.screen.clear()
        

    def get_history(self, dbname):
        history = query.query('SELECT query FROM queries_history ORDER BY id DESC LIMIT 100', 'queries')
        queryDB.display(self, history, dbname)
        

    def get_saved(self, dbname):
        saved = query.query('SELECT query FROM queries_saved ORDER BY id DESC LIMIT 100', 'queries')
        queryDB.display(self, saved, dbname)
                

    def run(self, string, currentDB):
        result = query.query(string, currentDB, self.screen)
        if result == -1:
            error.throw(self.screen, "The query did not succeed.")
            self.screen.clear()
        elif result == 0:
            error.throw(self.screen, "The query was succesful.")
            self.screen.clear()
            q = "INSERT INTO queries_history (query) VALUES (%s)"
            query.query(q, 'queries', None, None, string)
        else:
            self.screen.clear()
            tableDisplay.navigate(result, 0, 0, self.screen)
            self.screen.clear()
            q = "INSERT INTO queries_history (query) VALUES (%s)"
            query.query(q, 'queries', None, None, string)


    def display(self, data, currentDB):
        dim = self.screen.getmaxyx()
        self.screen.clear()
        self.screen.keypad(1)
        k = 0
        selector = 0
        while selector != ord('\n'):
            j = 0
            i = 0
            for i in range(len(data[1])):
                if i + j + len(data[1][i][0])//dim[1] + 1 > dim[0]:
                    i = i - 1
                    break
                if k == i:
                    self.screen.addstr(i + j, 0, data[1][i][0], curses.A_STANDOUT)
                else:
                    self.screen.addstr(i + j, 0, data[1][i][0], curses.A_DIM)
                if dim[1] < len(data[1][i][0]):
                    j += len(data[1][i][0])//dim[1]
            if not data[1]:
                error.throw(self.screen, "No queries available.")
                self.screen.clear()
                return
            self.screen.refresh()
            selector = self.screen.getch()
            self.screen.clear()
            if selector == curses.KEY_UP:
                if k > 0:
                    k = k - 1
            if selector == curses.KEY_DOWN:
                if k < i:
                    k = k + 1
        queryDB.run(self, data[1][k][0], currentDB)


    def display_top_left(self, message):
        self.screen.addstr(0, 0, message, curses.A_BOLD)
        self.screen.refresh()

    def display_all_database_save(self):   
        parsed_dbs = []
        databases = self.fetch_all_databases()
        if databases is not None:
            for db in databases:
                lst = list(db)
                lst.append(curses.flash)
                parsed_dbs.append(tuple(lst))
            displayDatabasesMenu = Menu(parsed_dbs, self.screen)
            displayDatabasesMenu.display()

    def fetch_all_databases(self):
        databases = query.query(self.all_databases_query, 'postgres', self.screen)
        return databases[1]

