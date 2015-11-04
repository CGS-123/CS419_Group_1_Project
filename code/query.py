import curses
import psycopg2
import pprint

class query:
    @staticmethod
    def select(query, db):
        #exceptions for debugging purposes
        try:
            string = "dbname=\'" + db + "\' user='vagrant' password='vagrant'"
            conn = psycopg2.connect(string)
        except:
            print "error to connecting to users database"
            return

        try:
            cur = conn.cursor()
        except:
            print "error creating cursor"
            return

        try:
            cur.execute(query)
        except:
            print "error executing query"
            return

        try:
            rows = cur.fetchall()
        except:
            print "error executing fetch"
            return

        cur.close()
        conn.close()
        return rows

    @staticmethod
    def insert(query, db):
    	#exceptions for debugging purposes
        try:
            string = "dbname=\'" + db + "\' user='vagrant' password='vagrant'"
            conn = psycopg2.connect(string)
        except:
            print "error to connecting to users database"
            return

        try:
            cur = conn.cursor()
        except:
            print "error creating cursor"
            return

        try:
            cur.execute(query)
        except:
            print "error executing query"
            return

        conn.commit()
        cur.close()
        conn.close()