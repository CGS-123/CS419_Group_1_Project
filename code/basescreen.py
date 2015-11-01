import curses

#Put all shared functionality between screens in this class

class BaseScreen:
    def __init__(self):
        self.screen = curses.initscr()
        self.dimensions = self.screen.getmaxyx() 

    def getCharsUntilReturnKey(self):
        while 1:
            char = self.screen.getch()
            if char == ord('\n'):
                return char
