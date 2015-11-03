import curses
from loginscreen import LoginScreen
import time
from Animators import Animators

screen = LoginScreen()
screen.welcome()
selection = screen.selector(0)

login_success = False

if selection:
    login_success = screen.create_user()
else :
    login_success = screen.login()

if login_success:
	print 'Woohoo, everything works!'
else:
	print 'oops! something didn\'t work'


