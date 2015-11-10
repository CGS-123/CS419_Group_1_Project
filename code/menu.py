import curses                                                                                                                 
from exports import impexp
from curses import panel
from databaseManager import DatabaseManager                                                     

class Menu(object):                                                          

    def __init__(self, items, stdscreen):                                    
        self.window = stdscreen.subwin(0,0)                                  
        self.window.keypad(1)                                                
        self.panel = panel.new_panel(self.window)                            
        self.panel.hide()                                                    
        panel.update_panels()                                                
        self.position = 0                                                    
        self.items = items                                                   
        self.items.append(('exit','exit'))                                  

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

        while True:    
            self.window.refresh()                                            
            curses.doupdate()                                                
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
                    self.items[self.position][1]()                           

            elif key == curses.KEY_UP:                                       
                self.navigate(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigate(1)                                             

        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()

class MyApp(object):                                                         

    def __init__(self, stdscreen):                                           
        self.screen = stdscreen
        self.database_manager = DatabaseManager()
        #I ran into an error here when trying to set cursur to invisible
        #this if/try makes sure that both the version of curses and the 
        #terminal support this functionality  
        if hasattr(curses, 'curs_set'):
            try:                                            
                curses.curs_set(0)                                                   
            except:
                pass
        importer = impexp(self.screen)

        data_items = [                                                    
                ('Import', curses.beep),                                       
                ('Export', importer.export)                                      
                ]                                                            
        data = Menu(data_items, self.screen)                           

        browse_database_items = [
                ('List Databases', self.display_all_databases),
                ('Search', curses.beep),                                       
                ('Create', self.create_new_database),
                ('Copy', curses.flash),
                ('Drop', curses.flash)                                      
                ]                                                            
        browse_database = Menu(browse_database_items, self.screen) 

        browse_table_items = [                                                    
                ('Create', curses.beep),                                       
                ('Delete', curses.flash),
                ('Copy', curses.flash),
                ('Alter', curses.flash)                                      
                ]                                                            
        browse_table = Menu(browse_table_items, self.screen) 

        query_items = [                                                    
                ('Enter Query', curses.beep),                                       
                ('View Past Queries', curses.flash),
                ('View Saved Queries', curses.flash)                                      
                ]                                                            
        query = Menu(query_items, self.screen) 

        main_menu_items = [                                                  
                ('Data Management', data.display),                                       
                ('Browse Databases', browse_database.display),                                     
                ('Browse Tables', browse_table.display),
                ('Query',query.display)                                 
                ]                                                            
        main_menu = Menu(main_menu_items, self.screen)                       

        main_menu.display()  
        
    def display_all_databases(self):   
        parsed_dbs = []
        databases = self.database_manager.fetch_all_databases()
        if databases is not None:
            for db in databases:
                lst = list(db)
                lst.append(curses.flash)
                parsed_dbs.append(tuple(lst))
            displayDatabasesMenu = Menu(parsed_dbs, self.screen)
            displayDatabasesMenu.display()
            
    def create_new_database(self):
        self.set_cursor_visible()
        curses.echo()
        self.display_mid("Please enter a name for the new database: ", self.screen)
        database_name = self.screen.getstr()
        self.screen.clear()
        try:
           did_create_database = self.database_manager.create_database(database_name)
        except RuntimeError as rt_error:
           self.display_mid("Error with the database creation query", self.screen)
        else:
            if did_create_database is True:
                self.display_mid("The database " + database_name + " has been created" , self.screen)
                self.screen.getstr()
        self.screen.clear()
        self.set_cursor_invisible()
        
    #displays message centered on screen
    def display_mid(self, message, screen):
        screen.clear()
        dimensions = self.screen.getmaxyx() 
        screen.addstr(dimensions[0]/2, dimensions[1]/2 - len(message)/2, message, curses.A_BOLD)
        screen.refresh()
        
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
            

