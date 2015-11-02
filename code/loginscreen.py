import curses
import psycopg2
import time
import pprint
from Animators import Animators


class LoginScreen:       
    def __init__(self):
        self.username = '' #username we will store from the user input
        self.password = ''
        self.screen = curses.initscr()


    #this function only return the integer value of 10 (i.e. integer value for newline character?)
    ###FUNCTION CURRENTLY NOT IN USE###  using getstr() instead
    def getCharsUntilReturnKey(self):
        while 1:
            char = self.screen.getch()
            if char == ord('\n'):
                return char

    #recursive function used to select either create account or login
    def selector(self, location):
        self.screen.keypad(1)
        dimensions = self.screen.getmaxyx()
        self.screen.clear()
        if(location):
            message = "Select Using ->, <-, and Enter:"
            self.screen.addstr(dimensions[0]/3, dimensions[1]/2 - len(message)/2, message)
            message = 'Login'
            self.screen.addstr(dimensions[0]/2, dimensions[1]/3 - len(message)/2, message, curses.A_DIM)
            message = 'Create User'
            self.screen.addstr(dimensions[0]/2, 2 * dimensions[1]/3 - len(message)/2, message, curses.A_BOLD)  
            self.screen.refresh()
        else:
            message = "Select Using ->, <-, and Enter:"
            self.screen.addstr(dimensions[0]/3, dimensions[1]/2 - len(message)/2, message)
            message = 'Login'
            self.screen.addstr(dimensions[0]/2, dimensions[1]/3 - len(message)/2, message, curses.A_BOLD)
            message = 'Create User'
            self.screen.addstr(dimensions[0]/2, 2 * dimensions[1]/3 - len(message)/2, message, curses.A_DIM)  
            self.screen.refresh()         
    
        choice = self.screen.getch()
        if choice == ord('\n'):
            return location
        elif choice == curses.KEY_LEFT:
            return LoginScreen.selector(self, 0)
        elif choice == curses.KEY_RIGHT:
            return LoginScreen.selector(self, 1)
        else:
            return LoginScreen.selector(self, location)         

    #function used to insert a new user into the databse:
    def create_user(self):
        LoginScreen.display_mid(self, 'Please enter your desired username: ')
        self.username = self.screen.getstr()
        LoginScreen.display_mid(self, 'Please enter your desired password: ')
        self.password = self.screen.getstr()
        curses.endwin()

        query = "SELECT * FROM users WHERE un LIKE \'" + self.username + "\'"
        rows = LoginScreen.user_query(self, query, 1)
        
        if rows:
            LoginScreen.display_mid(self, 'Username already in use.')
            time.sleep(3)
            return LoginScreen.create_user(self)
        else:
            query = "INSERT INTO users (un, pw) VALUES (\'" + self.username + "\', \'" + self.password + "\')"
            LoginScreen.user_query(self, query, 0);
            return True

    def login(self):
        #Should we be printing non-curses output?
        #print('start screen started')

        
        LoginScreen.display_mid(self, 'Please enter your username: ')
        self.username = self.screen.getstr()
        LoginScreen.display_mid(self, 'Please enter your password: ')
        self.password = self.screen.getstr()
        curses.endwin()


        #query the database and check if name and password are correct
        query = "SELECT * FROM users WHERE un LIKE \'" + self.username + "\' AND pw LIKE \'" + self.password + "\'"
        rows = LoginScreen.user_query(self, query, 1)
        
        if rows:
            return True
        else:
            return False

    #function that prints a flowing welcome message
    def welcome(self):
        anim = Animators()
        anim.enter_down(self.screen, "Welcome!")
        time.sleep(1)
        anim.exit_up(self.screen, "Welcome!")
        self.screen.clear()

    #displays message centered on screen
    def display_mid(self, message):
        self.screen.clear()
        dimensions = self.screen.getmaxyx() 
        self.screen.addstr(dimensions[0]/2, dimensions[1]/2 - len(message)/2, message, curses.A_BOLD)
        self.screen.refresh()

    #runs a query on the users table in the users db and returns the results
    #This method is UNSAFE and is vulnerable to injection - psycopg2 has some prepared statement style methods to prevent this, I just haven't implimented them =)
    def user_query(self, query, fetch):
        #exceptions for debugging purposes
        try:
            conn = psycopg2.connect("dbname='users' user='vagrant' password='vagrant'")
        except:
            print "error to connecting to users database"

        try:
            cur = conn.cursor()
        except:
            print "error creating cursor"

        try:
            cur.execute(query)
        except:
            print "error executing query"

        if fetch:
            try:
                rows = cur.fetchall()
            except:
                print "error executing fetch"

            cur.close()
            conn.close()
            return rows

        conn.commit()
        cur.close()
        conn.close()        

