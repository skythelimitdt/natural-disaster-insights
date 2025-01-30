# Import necessary modules
from Menu import Menu
from SearchYear import SearchYear
from CountEvent import CountEvent
from DeadlyEvent import DeadlyEvent
from DestructiveEvent import DestructiveEvent
from LengthEvent import LengthEvent
from SearchLocation import SearchLocation
from Splash import Splash

class AppController:
    def __init__(self, master):
        # Initialize the controller
        self.master = master
        self.current_app = None

    # Start the application
    def start(self):
        self.switch_to_splash()

    # Switch to the splash screen view
    def switch_to_splash(self):
        self.destroy()
        self.current_app = Splash(self.master, self)

    # Switch to the main menu view
    def switch_to_menu(self):
        self.destroy()
        self.current_app = Menu(self.master, self)

    # Switch to the search-by-year view
    def switch_to_search_year(self):
        self.destroy()
        self.current_app = SearchYear(self.master, self)

    # Switch to the event count view
    def switch_to_count(self):
        self.destroy()
        self.current_app = CountEvent(self.master, self)

    # Switch to the most deadly event view
    def switch_to_deadly(self):
        self.destroy()
        self.current_app = DeadlyEvent(self.master, self)

    # Switch to the most destructive event view
    def switch_to_destructive(self):
        self.destroy()
        self.current_app = DestructiveEvent(self.master, self)

    # Switch to the event duration analysis view
    def switch_to_length(self):
        self.destroy()
        self.current_app = LengthEvent(self.master, self)

    # Switch to the search-by-location view
    def switch_to_search_location(self):
        self.destroy()
        self.current_app = SearchLocation(self.master, self)

    # Destroy the current app
    def destroy(self):
        if self.current_app:
            self.current_app.main_frame.destroy()
            self.current_app = None