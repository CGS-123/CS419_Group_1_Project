import curses
from Animators import Animators
#NOTE this method is also useful for debugging if you just want to throw a 
#variable up on the screen real quick =)

class ScreenManager:
    def __init__(self, stdscreen):
        self.screen = stdscreen

    @staticmethod
    def throw(screen, message):
        screen.clear()
        dimensions = screen.getmaxyx() 
        screen.addstr(dimensions[0]/2, dimensions[1]/2 - len(message)/2, message, curses.A_BOLD)
        screen.addstr(dimensions[0]/2+1, dimensions[1]/2 - len("Press any key to continue.")/2, "Press any key to continue.")
        screen.refresh()
        screen.getch()

    #displays message centered on screen
    def display_mid(self, message):
        self.screen.clear()
        dimensions = self.screen.getmaxyx() 
        self.screen.addstr(dimensions[0]/2, dimensions[1]/2 - len(message)/2, message, curses.A_BOLD)
        self.screen.refresh()


    #function that prints a flowing welcome message
    def welcome(self):
        anim = Animators()
        anim.enter_down(self.screen, "Welcome!")
        time.sleep(1)
        anim.exit_up(self.screen, "Welcome!")
        self.screen.clear()

    def set_cursor_invisible(self):
        if hasattr(curses, 'curs_set'):
            try:
                curses.curs_set(0)
            except:
                pass

    def set_cursor_visible(self):
        if hasattr(curses, 'curs_set'):
            try:
                curses.curs_set(1)
            except:
                pass