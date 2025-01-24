import tkinter as tk
from AppController import AppController
from pathlib import Path
import sys


sys.path.append("C:/Users/Ian O'Connor/Github/natural-disaster-insights/data")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("App")
    app_controller = AppController(root)
    app_controller.start()
    root.mainloop()