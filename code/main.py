import curses
from loginscreen import LoginScreen
import time
from Animators import Animators
from menu import Menu
from myApp import MyApp

screen = LoginScreen()
screen.welcome()
selection = screen.selector(0)
username = ""
password = ""
login_success = False
while not login_success:
    if selection:
        login_success = screen.create_user()
        username = screen.username
        password = screen.password
    else:
        login_success = screen.login()
        username = screen.username
        password = screen.password

userpass = {'user':username, 'pass':password}
if login_success:
	curses.wrapper(MyApp, userpass)
else:
	print 'oops! something didn\'t work'


