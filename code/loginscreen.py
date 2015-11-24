import curses
import psycopg2
import time
import pprint
from Animators import Animators
from query import query
from error import error
from screenmanager import ScreenManager
from subprocess import call

class LoginScreen:       
    def __init__(self):
        self.username = '' #username we will store from the user input
        self.password = ''
        self.screen = curses.initscr()
        self.screen_manager = ScreenManager(self.screen)
    #recursive function used to select either create account or login
    def selector(self, location):
        self.screen.keypad(1)
        dimensions = self.screen.getmaxyx()
        self.screen.clear()
        message = "Select Using ->, <-, and Enter:"
        self.screen.addstr(dimensions[0]/3, dimensions[1]/2 - len(message)/2, message)
        if(location):
            message = 'Login'
            self.screen.addstr(dimensions[0]/2, dimensions[1]/3 - len(message)/2, message, curses.A_DIM)
            message = 'Create User'
            self.screen.addstr(dimensions[0]/2, 2 * dimensions[1]/3 - len(message)/2, message, curses.A_STANDOUT)  
            self.screen.refresh()
        else:
            message = 'Login'
            self.screen.addstr(dimensions[0]/2, dimensions[1]/3 - len(message)/2, message, curses.A_STANDOUT)
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
        self.screen_manager.display_mid('Please enter your desired Username: ')
        self.username = self.screen.getstr()
        self.screen_manager.display_mid('Please enter your desired Password: ')
        self.password = self.screen.getstr()

        to_query = "SELECT * FROM pg_catalog.pg_roles WHERE rolname LIKE \'%s\'" % self.username
        rows = query.query(to_query, 'postgres', self.screen)
        
        if rows:
            ScreenManager.throw(self.screen, 'Username already in use.')
            return LoginScreen.create_user(self)
        else:
            to_query = "CREATE USER %s WITH CREATEDB PASSWORD \'%s\'" % (self.username, self.password)
            if query.query(to_query, 'postgres', self.screen) == -1:
                ScreenManager.throw(self.screen, "An error prevented user creation.")
                return False
            to_query = "CREATE DATABASE %s_default" % (self.username)
            if query.query(to_query, 'postgres', self.screen, 0) == -1:
                ScreenManager.throw(self.screen, "An error occured during user default database creation.")
                return False
            to_query = "ALTER DATABASE %s_default owner to %s" % (self.username, self.username)
            if query.query(to_query, 'postgres', self.screen) == -1:
                ScreenManager.throw(self.screen, "An error occured while assigning new user to default database.")
                return False

            return True

    def login(self):
        self.screen_manager.display_mid('Please enter your Username: ')
        self.username = self.screen.getstr()
        self.screen_manager.display_mid('Please enter your Password: ')
        self.password = self.screen.getstr()


        #query the database and check if name and password are correct
        to_query = "SELECT * FROM pg_catalog.pg_roles WHERE rolname LIKE \'root\'"
        rows = query.query(to_query, 'postgres', None, None, None, self.username, self.password)
        
        if rows != -1 and rows != -2:
            return True
        elif rows == -1:
            ScreenManager.throw(self.screen, "Couldn't sign in. Please ensure your system is set up correctly.")
            return False
        else:
            ScreenManager.throw(self.screen, "Incorrect Username or Password.")
            return False

    #function that prints a flowing welcome message
    def welcome(self):
        anim = Animators()
        anim.enter_down(self.screen, "Welcome!")
        time.sleep(.25)
        anim.exit_up(self.screen, "Welcome!")
        self.screen.clear()