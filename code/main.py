import curses
from loginscreen import LoginScreen
import time
from Animators import Animators
from menu import Menu
from menu import MyApp

screen = LoginScreen()
screen.welcome()
selection = screen.selector(0)

login_success = False
while not login_success:
    if selection:
        login_success = screen.create_user()
    else:
        login_success = screen.login()

if login_success:
	curses.wrapper(MyApp)
else:
	print 'oops! something didn\'t work'


