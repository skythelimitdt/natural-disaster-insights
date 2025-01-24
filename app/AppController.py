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
        self.current_app = Splash(self.master, self)

    def switch_to_menu(self):
        self.destroy()
        self.current_app = Menu(self.master, self)

    def switch_to_search(self):
        self.destroy()
        self.current_app = SearchYear(self.master, self)

    def switch_to_count(self):
        self.destroy()
        self.current_app = CountEvents(self.master, self)

    def destroy(self):
        if self.current_app:
            self.current_app.main_frame.destroy()
            self.current_app = None