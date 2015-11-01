import curses
from basescreen import BaseScreen

kUserNamePrompt = 'Please enter your username:'
kPasswordPrompt = 'Please enter your password:'
kLoginScreenXOffset = 10
kLoginScreenYOffset = 2

class LoginScreen(BaseScreen):           
    def __init__(self):
        BaseScreen.__init__(self)
        self.username = '' #username we will store from the user input
        self.password = ''
                
    def login(self):
        #This should return a tuple such as (y, x)
        self.screen.addstr(self.dimensions[0]/2 - kLoginScreenYOffset, self.dimensions[1]/2 - kLoginScreenXOffset, kUserNamePrompt, curses.A_BOLD)
        self.screen.refresh()
        self.username = self.getCharsUntilReturnKey()
        self.screen.clear()
        self.screen.addstr(self.dimensions[0]/2 - kLoginScreenYOffset, self.dimensions[1]/2 - kLoginScreenXOffset, kPasswordPrompt, curses.A_BOLD)
        self.screen.refresh()
        self.password = self.getCharsUntilReturnKey()
        self.screen.clear()
        #query the database and check if name and password are correct
        #if password && username is correct
            #return True
        #else
            #return False
        curses.endwin()
        return True
