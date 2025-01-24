from MenuUI import Menu
from FilterDataUI import FilterData
from CountDataUI import CountData


class AppController:
    def __init__(self, master):
        self.master = master
        self.current_app = None

    def start(self):
        self.switch_to_menu()

    def switch_to_menu(self):
        self.destroy()
        self.current_app = Menu(self.master, self)

    def switch_to_filter(self):
        self.destroy()
        self.current_app = FilterData(self.master, self)

    def switch_to_count(self):
        self.destroy()
        self.current_app = CountData(self.master, self)

    def destroy(self):
        if self.current_app:
            self.current_app.main_frame.destroy()
            self.current_app = None