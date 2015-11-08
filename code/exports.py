import sys
import curses
import psycopg2

class impexp(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
    def export(self):
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