from Menu import Menu
from SearchYear import SearchYear
from CountEvent import CountEvent
from DeadlyEvent import DeadlyEvent
from DestructiveEvent import DestructiveEvent
from LengthEvent import LengthEvent
from RandomEvent import RandomEvent
from SearchName import SearchName
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

    def switch_to_search_year(self):
        self.destroy()
        self.current_app = SearchYear(self.master, self)

    def switch_to_count(self):
        self.destroy()
        self.current_app = CountEvent(self.master, self)

    def switch_to_deadly(self):
        self.destroy()
        self.current_app = DeadlyEvent(self.master, self)

    def switch_to_destructive(self):
        self.destroy()
        self.current_app = DestructiveEvent(self.master, self)

    def switch_to_length(self):
        self.destroy()
        self.current_app = LengthEvent(self.master, self)

    def switch_to_random(self):
        self.destroy()
        self.current_app = RandomEvent(self.master, self)

    def switch_to_search_name(self):
        self.destroy()
        self.current_app = SearchName(self.master, self)


    def destroy(self):
        if self.current_app:
            self.current_app.main_frame.destroy()
            self.current_app = None