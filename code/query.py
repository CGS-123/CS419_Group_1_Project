import curses
import psycopg2
from error import error


#functions in Class:
#   fetch() - used for psql queries that return information. (i.e. SELECT)
#   execute() - used for psql queires that create/modify information (i.e.
#   CREATE, INSERT, DROP, DELETE)

class query:

    #director function
    @staticmethod
    def query(string, db, screen = None, ISO_level = None, multi_part = None, username = None, password = None):
        select = string.split(" ")
        if select[0].lower() == "select":
            return query.fetch(string, db, screen, ISO_level, multi_part, username, password)
        else:
            return query.execute(string, db, screen, ISO_level, multi_part, username, password)


    #NOTE: overloaded function,  if provided screen, will display error
    #method used to return any values from a database given a string query
    #on succes returns list of elelemts
    #on fail throws error screen and returns -1 !!Needs to be handled!!
    @staticmethod
    def fetch(query, db, screen = None, ISO_level = None, multi_part = None, username = None, password = None):
        if username is None:
            try:
                string = "dbname=\'" + db + "\' user='vagrant' password='vagrant'"
                conn = psycopg2.connect(string)
            except:
                if screen is not None:
                    error.throw(screen, "Error to connecting to \'" + db + "\' database.")
                    return -1
                else:
                    return -1
        else:
            try:
                string = "dbname=\'" + db + "\' user=\'" + username + "\' password=\'" + password + "\'"
                conn = psycopg2.connect(string)
            except:
                if screen is not None:
                    error.throw(screen, "Error to connecting to \'" + db + "\' database.")
                    return -2
                else:
                    return -2

        if ISO_level is not None:
            try:
                conn.set_isolation_level(ISO_level)
            except:
                if screen is not None:
                    error.throw(screen, "Error setting Isolation Level.")
                    return -1
                else:
                    return -1

        try:
            cur = conn.cursor()
        except:
            if screen is not None:
                error.throw(screen, "Error creating cursor.")
                return -1
            else:
                return -1
        
        if ISO_level is not 0 or None:
            try:
                if multi_part is None:
                    cur.execute(query)
                else:
                    cur.execute(query, (multi_part,))
            except:
                if screen is not None:
                    error.throw(screen, "Error executing query.")
                    return -1
                else:
                    return -1

        try:
            cols = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
        except:
            if screen is not None:
                error.throw(screen, "Error executing fetch.")
                return -1
            else:
                return -1

        try:
            cur.close()
        except:
            if screen is not None:
                error.throw(screen, "Error closing cursor.")
                return -1
            else:
                return -1

        try:
            conn.close()
        except:
            if screen is not None:
                error.throw(screen, "Error closing connection.")
                return -1
            else:
                return -1
        
        return (cols, rows)

    #NOTE: overloaded function,  if provided screen, will display error
    #method used to return any values from a database given a string query
    #on succes returns 0
    #on fail throws error screen and returns -1 !!Needs to be handled!!
    @staticmethod
    def execute(query, db, screen = None, ISO_level = None, multi_part = None, username = None, password = None):
    	#exceptions for debugging purposes
        if username is None:
            try:
                string = "dbname=\'" + db + "\' user='vagrant' password='vagrant'"
                conn = psycopg2.connect(string)
            except:
                if screen is not None:
                    error.throw(screen, "Error to connecting to \'" + db + "\' database.")
                    return -1
                else:
                    return -1
        else:
            try:
                string = "dbname=\'" + db + "\' user=\'" + username + "\' password=\'" + password + "\'"
                conn = psycopg2.connect(string)
            except:
                if screen is not None:
                    error.throw(screen, "Error to connecting to \'" + db + "\' database.")
                    return -2
                else:
                    return -2

        if ISO_level is not None:
            try:
                conn.set_isolation_level(ISO_level)
            except:
                if screen is not None:
                    error.throw(screen, "Error setting Isolation Level.")
                    return -1
                else:
                    return -1

        try:
            cur = conn.cursor()
        except:
            if screen is not None:
                print error.throw(screen, "Error creating cursor.")
                return -1
            else:
                return -1

        try:
            if multi_part is None:
                cur.execute(query)
            else:
                cur.execute(query, (multi_part,))
        except:
            if screen is not None:
                error.throw(screen, "Error executing query.")
                
                return -1
            else:
                return -1

        if ISO_level is not 0 or None:
            try:
                conn.commit()
            except:
                if screen is not None:
                    error.throw(screen, "Error commiting query.")
                    return -1
                else:
                    return -1

        try:
            cur.close()
        except:
            if screen is not None:
                error.throw(screen, "Error closing cursor.")
                return -1
            else:
                return -1

        try:
            conn.close()
        except:
            if screen is not None:
                error.throw(screen, "Error closing connection.")
                return -1
            else:
                return -1

        return 0
