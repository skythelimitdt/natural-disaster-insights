from Menu import Menu
from SearchYear import SearchYear
from CountEvents import CountEvents
from Splash import Splash


class AppController:
    def __init__(self, master):
        self.master = master
        self.current_app = None

    def start(self):
        self.switch_to_splash()
    

    def switch_to_splash(self):
        self.destroy()
        ###switch to the splash screen.
        self.master.geometry("1900x1500")  #ensure proper splash screen size
        self.current_app = Splash(self.master, self)

    def switch_to_menu(self):
        ###switch to the main menu."""
        self.master.geometry("1024x768")  #set size for the menu        
        self.destroy()
        self.current_app = Menu(self.master, self)

    def switch_to_search(self):
        ###switch to the search by year screen.
        self.master.geometry("1024x768")  #set size for the search screen
        self.destroy()
        self.current_app = SearchYear(self.master, self)

    def switch_to_count(self):
        ###switch to the disaster count by type screen.
        self.master.geometry("1024x768")  #set size for the count events screen
        self.destroy()
        self.current_app = CountEvents(self.master, self)

    def destroy(self):
        if self.current_app:
            self.current_app.main_frame.destroy()
            self.current_app = None