import tkinter as tk
from AppController import AppController

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Natural Disaster App")
    app_controller = AppController(root)
    app_controller.start()
    root.mainloop()