import curses                                                                                                                 
from exports import impexp
from curses import panel
from databaseManager import DatabaseManager   
from screenmanager import ScreenManager   
from tableManager import TableManager                                               
from menu import Menu
from queryDB import queryDB

class MyApp(object):                                                         

    def __init__(self, stdscreen, userpass):                                           
        self.screen = stdscreen
        self.username = userpass['user']
        self.password = userpass['pass']
        self.database_manager = DatabaseManager(self.screen, userpass)
        self.screen_manager = ScreenManager(self.screen)
        self.table_manager = TableManager(self.screen, userpass)
        self.query_manager = queryDB(self.screen, userpass)
        headeroptions = {'user':self.username}

        #I ran into an error here when trying to set cursur to invisible
        #this if/try makes sure that both the version of curses and the 
        #terminal support this functionality  
        if hasattr(curses, 'curs_set'):
            try:                                            
                curses.curs_set(0)                                                   
            except:
                pass
        importer = impexp(self.screen, userpass)
        data_items = [                                                    
                ('Import', self.database_manager.display_all_databases_opt, importer.list_sql_files),                                       
                ('Export', self.database_manager.display_all_databases_opt, importer.export)                                      
                ]                                                            
        data = Menu(data_items, self.screen, headeroptions)                           

        browse_database_items = [
                ('List Databases', self.database_manager.display_all_databases),                                      
                ('Create', self.database_manager.create_new_database),
                ('Copy', self.database_manager.display_all_copy_database),
                ('Drop', self.database_manager.display_all_delete_database)                                      
                ]                                                            
        browse_database = Menu(browse_database_items, self.screen, headeroptions) 

        browse_table_items = [
                ('List Tables', self.database_manager.display_all_databases_opt, self.table_manager.listTables),                                                    
                ('Create', self.database_manager.display_all_databases_opt, self.table_manager.createTable),                                       
                ('Delete', self.database_manager.display_all_databases_opt, self.table_manager.list_drop_tables),
                ('Copy', curses.flash),
                ('Alter', curses.flash)                                      
                ]                                                            
        browse_table = Menu(browse_table_items, self.screen, headeroptions) 

        query_items = [                                                    
                ('Enter A Query', self.database_manager.display_all_databases_opt, self.query_manager.do),
                ('Save A Query', self.query_manager.save),                                       
                ('View Past Queries', self.database_manager.display_all_databases_opt, self.query_manager.get_history),
                ('View Saved Queries', self.database_manager.display_all_databases_opt, self.query_manager.get_saved)                                      
                ]                                                            
        query = Menu(query_items, self.screen, headeroptions) 

        main_menu_items = [                                                  
                ('Data Management', data.display),                                       
                ('Browse Databases', browse_database.display),                                     
                ('Browse Tables', browse_table.display),
                ('Query',query.display)                                 
                ]        
                                               
        main_menu = Menu(main_menu_items, self.screen, headeroptions)                       

        main_menu.display()          
        
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
            

