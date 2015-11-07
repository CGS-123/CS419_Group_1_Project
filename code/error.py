import curses

#NOTE this method is also useful for debugging if you just want to throw a 
#variable up on the screen real quick =)
class error:
    @staticmethod
    def throw(screen, message):
    	screen.clear()
        dimensions = screen.getmaxyx() 
        screen.addstr(dimensions[0]/2, dimensions[1]/2 - len(message)/2, message, curses.A_BOLD)
        screen.addstr(dimensions[0]/2+1, dimensions[1]/2 - len("Press any key to continue.")/2, "Press any key to continue.")
        screen.refresh()
        screen.getch()