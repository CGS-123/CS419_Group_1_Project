import curses
import psycopg2
import time
import pprint
from Animators import Animators
from query import query

class LoginScreen:       
    def __init__(self):
        self.username = '' #username we will store from the user input
        self.password = ''
        self.screen = curses.initscr()

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
            self.screen.addstr(dimensions[0]/2, 2 * dimensions[1]/3 - len(message)/2, message, curses.A_STANDOUT)  
            self.screen.refresh()
        else:
            message = "Select Using ->, <-, and Enter:"
            self.screen.addstr(dimensions[0]/3, dimensions[1]/2 - len(message)/2, message)
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
        LoginScreen.display_mid(self, 'Please enter your desired username: ')
        self.username = self.screen.getstr()
        LoginScreen.display_mid(self, 'Please enter your desired password: ')
        self.password = self.screen.getstr()
        curses.endwin()

        to_query = "SELECT * FROM users WHERE un LIKE \'%s\'" % self.username
        rows = query.select(to_query, 'users')
        
        if rows:
            LoginScreen.display_mid(self, 'Username already in use.')
            time.sleep(3)
            return LoginScreen.create_user(self)
        else:
            to_query = "INSERT INTO users (un, pw) VALUES (\'%s\', \'%s\')" % (self.username, self.password)
            query.insert(to_query, 'users');
            return True

    def login(self):
       
        LoginScreen.display_mid(self, 'Please enter your username: ')
        self.username = self.screen.getstr()
        LoginScreen.display_mid(self, 'Please enter your password: ')
        self.password = self.screen.getstr()
        curses.endwin()


        #query the database and check if name and password are correct
        to_query = "SELECT * FROM users WHERE un LIKE \'%s\' AND pw LIKE \'%s\'" % (self.username, self.password)
        rows = query.select(to_query, 'users')
        
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