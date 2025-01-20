import tkinter as tk
from tkinter import ttk
from TkApp import TkApp

class MainApp:
    def __init__(self, master):
        tk.Grid.columnconfigure(master, 0, weight=1)
        tk.Grid.rowconfigure(master, 0, weight=1)

        # build ui
        self.__main_notebook = ttk.Notebook(master)
        self.__main_notebook.grid(column='0', row='0', sticky='nsew')
        self.__main_notebook.rowconfigure('0', weight='1')
        self.__main_notebook.columnconfigure('0', weight='1')

        # Main widget
        self.__mainwindow = self.__main_notebook

        main_app = MainApp(self.__mainwindow)
        self.__main_notebook.add(main_app.get_top_frame(), text="Test 1")

        flask_app = TkApp(self.__mainwindow)
        self.__main_notebook.add(flask_app.get_top_frame(), text="Test 2")

    def run(self):
        self.__mainwindow.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    app.run()