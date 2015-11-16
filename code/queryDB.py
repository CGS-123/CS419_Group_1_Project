import curses
import psycopg2
from psycopg2 import extras
from query import query
from error import error

# NOTE: saved/historical queries that would go off the screen are not 
# displayed and are not selectable. They are displayed in a stack 
# style with the most recent saved/run queries displayed in a list.
# However, these queries are still saved/recoreded and can be accessed
# by querying the queries db manually.

class queryDB:

    @staticmethod
    def do(screen):
      ###good spot to put a "users member" variable for current db instead of worlddb
        currentDB = 'worlddb'
        screen.clear()
        queryDB.display_top_left("Please enter a query to execute below:\n", screen)
        curses.echo()
        string = screen.getstr()
        
        queryDB.run(string, currentDB, screen)


    @staticmethod
    def save(screen):
      ###good spot to put a "users member" variable for current db instead of worlddb
        currentDB = 'worlddb'
        screen.clear()
        queryDB.display_top_left("Please enter a query save below:\n", screen)
        curses.echo()
        string = screen.getstr()
        q = "INSERT INTO queries_saved (query) VALUES (%s)"
        query.query(q, 'queries', None, None, string)
        screen.clear()
        

    @staticmethod
    def get_history(screen):
      ###good spot to put a "users member" variable for current db instead of worlddb
        currentDB = 'worlddb'
        history = query.query('SELECT query FROM queries_history ORDER BY id DESC LIMIT 100', 'queries')
        queryDB.display(screen, history, currentDB)
        

    @staticmethod
    def get_saved(screen):
      ###good spot to put a "users member" variable for current db instead of worlddb
        currentDB = 'worlddb'
        saved = query.query('SELECT query FROM queries_saved ORDER BY id DESC LIMIT 100', 'queries')
        queryDB.display(screen, saved, currentDB)
                

    @staticmethod
    def run(string, currentDB, screen):
        result = query.query(string, currentDB, screen)
        if result == -1:
            error.throw(screen, "The query did not succeed.")
            screen.clear()
        elif result == 0:
            error.throw(screen, "The query was succesful.")
            screen.clear()
            q = "INSERT INTO queries_history (query) VALUES (%s)"
            query.query(q, 'queries', None, None, string)
        else:
            screen.clear()
            queryDB.display_top_left(str(result), screen)
            screen.getch()
            screen.clear()
            q = "INSERT INTO queries_history (query) VALUES (%s)"
            query.query(q, 'queries', None, None, string)

    @staticmethod
    def display(screen, data, currentDB):
        dim = screen.getmaxyx()
        screen.clear()
        screen.keypad(1)
        k = 0
        selector = 0
        while selector != ord('\n'):
            j = 0
            for i in range(len(data)):
                if i + j + len(data[i][0])//dim[1] + 1 > dim[0]:
                    i = i - 1
                    break
                if k == i:
                    screen.addstr(i + j, 0, data[i][0], curses.A_STANDOUT)
                else:
                    screen.addstr(i + j, 0, data[i][0], curses.A_DIM)
                if dim[1] < len(data[i][0]):
                    j += len(data[i][0])//dim[1]
            screen.refresh()
            selector = screen.getch()
            screen.clear()
            if selector == curses.KEY_UP:
                if k > 0:
                    k = k - 1
            if selector == curses.KEY_DOWN:
                if k < i:
                    k = k + 1
        queryDB.run(data[k][0], currentDB, screen)


    @staticmethod
    def display_top_left(message, screen):
        screen.addstr(0, 0, message, curses.A_BOLD)
        screen.refresh()

