import curses                                                                                                                 
from exports import impexp
from curses import panel
from databaseManager import DatabaseManager                                                     
from menu import Menu

class MyApp(object):                                                         

    def __init__(self, stdscreen):                                           
        self.screen = stdscreen
        #I ran into an error here when trying to set cursur to invisible
        #this if/try makes sure that both the version of curses and the 
        #terminal support this functionality  
        if hasattr(curses, 'curs_set'):
            try:                                            
                curses.curs_set(0)                                                   
            except:
                pass
        importer = impexp(self.screen)
        db_manager = DatabaseManager(self.screen)

        data_items = [                                                    
                ('Import', importer.list_sql_files),                                       
                ('Export', importer.export)                                      
                ]                                                            
        data = Menu(data_items, self.screen)                           

        browse_database_items = [
                ('List Databases', db_manager.display_all_databases),                                      
                ('Create', db_manager.create_new_database),
                ('Copy', db_manager.display_all_copy_database),
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
            

