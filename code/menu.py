import curses
import time
from datetime import date
from curses import panel
class Menu(object):                                                          

    def __init__(self, items, stdscreen, header_opts = None):                                    
        self.window = stdscreen.subwin(0,0)                                  
        self.window.keypad(1)                                                
        self.panel = panel.new_panel(self.window)                            
        self.panel.hide()                                                    
        panel.update_panels()                                                
        self.position = 0                                                    
        self.items = items                                                   
        self.items.append(('exit','exit'))
        if header_opts:
            self.header = self.parseheaderopts(header_opts)
        else:
            self.header = ""                                  
        self.header += "|" + str(date.today()) + "|"

    def parseheaderopts(self, header_opts):
        header = ""
        if 'user' in header_opts:
            header += "| " + header_opts['user'] + " |"
        if 'db' in header_opts:
            header += "Current Databease: " + header_opts['db'] + "|"
        if 'title' in header_opts:
            header += "("  + header_opts['title'] + ")"
        return header

    def navigate(self, n):                                                   
        self.position += n                                                   
        if self.position < 0:                                                
            self.position = 0                                                
        elif self.position >= len(self.items):                               
            self.position = len(self.items)-1                                

    def display(self):                                                       
        self.panel.top()                                                     
        self.panel.show()                                                    
        self.window.clear()                                                  
        dimensions = self.window.getmaxyx()
        while True:    
            self.window.refresh()                                            
            curses.doupdate()  
            self.window.addstr(0, dimensions[1]/2 - len(self.header)/2, self.header, curses.A_BOLD)                                              
            for index, item in enumerate(self.items):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   

                msg = '%d. %s' % (index, item[0])                            
                self.window.addstr(1+index, 1, msg, mode)                    

            key = self.window.getch()                                        

            if key in [curses.KEY_ENTER, ord('\n')]:                         
                if self.position == len(self.items)-1:                       
                    break                                                    
                else:
                    if len(self.items[self.position]) > 2:
                        arg = self.items[self.position][2]
                        self.items[self.position][1](arg)  
                    else:
                        self.items[self.position][1]()                           

            elif key == curses.KEY_UP:                                       
                self.navigate(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigate(1)                                             

        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()
