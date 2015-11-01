import curses
from loginscreen import LoginScreen

print("started")
screen = LoginScreen()
loginSuccessful = screen.login()
if loginSuccessful:
    print('Logged in')
else :
    print('Login failed')


