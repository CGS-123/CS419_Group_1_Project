import curses

class LoginScreen:       
    def __init__(self):
        self.username = '' #username we will store from the user input
        self.password = ''
        self.screen = curses.initscr()
         
    def getCharsUntilReturnKey(self):
        while 1:
            char = self.screen.getch()
            if char == ord('\n'):
                return char  
                
    def login(self):
        print('start screen started')
    #This should return a tuple such as (y, x)
        dimensions = self.screen.getmaxyx() 
        screenXOffset = 10
        screenYOffset = 2
        self.screen.addstr(dimensions[0]/2 - screenYOffset, dimensions[1]/2 - screenXOffset, 'Please enter your username:', curses.A_BOLD)
        self.screen.refresh()
        self.username = self.getCharsUntilReturnKey()
        self.screen.clear()
        self.screen.addstr(dimensions[0]/2 - screenYOffset, dimensions[1]/2 - screenXOffset, 'Please enter your password:', curses.A_BOLD)
        self.screen.refresh()
        self.password = self.getCharsUntilReturnKey()
        #query the database and check if name and password are correct
        #if password && username is correct
            #return True
        #else
            #return False
        curses.endwin()
        return True
