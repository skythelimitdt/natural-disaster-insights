import tkinter as tk
from tkinter import ttk, messagebox
import requests

class TkApp:
    API_URL = ""

    def __init__(self, master):
        master.title("App")
        self.master = master

        # Tabbed interface
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        # Add tabs
        self.create_filter_data_tab()

    def create_filter_data_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Filter Data")

        # Date filter inputs
        ttk.Label(frame, text="Parameter #1:").grid(row=0, column=0, padx=10, pady=5)
        self.data1 = ttk.Entry(frame)
        self.data1.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Parameter #2:").grid(row=1, column=0, padx=10, pady=5)
        self.data2 = ttk.Entry(frame)
        self.data2.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Fetch Data", command=self.fetch_data).grid(row=2, column=0, columnspan=2, pady=10)

    def fetch_data(self):
        data1 = self.data1.get()
        data2 = self.data2.get()

        try:
            response = requests.get(f"{self.API_URL}", params={"": data1, "": data2})
            response.raise_for_status()
            sales = response.json()

            # Display results
            result_window = tk.Toplevel(self.master)
            result_window.title("Data")
            for i, sale in enumerate(sales):
                ttk.Label(result_window, text=str(sale)).grid(row=i, column=0, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = TkApp(root)
    root.mainloop()