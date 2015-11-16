import curses                                                                                                                 
from exports import impexp
from curses import panel
from databaseManager import DatabaseManager                                                     
from menu import Menu
from queryDB import queryDB

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
                ('Import', importer.list_sql_files),                                       
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
                ('Enter A Query', self.enter_query),
                ('Save A Query', self.save_query),                                       
                ('View Past Queries', self.view_history),
                ('View Saved Queries', self.view_saved)                                      
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

    def view_history(self):
        queryDB.get_history(self.screen)

    def view_saved(self):
        queryDB.get_saved(self.screen)

    def enter_query(self):
        queryDB.do(self.screen)

    def save_query(self):
        queryDB.save(self.screen)
        
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
            

