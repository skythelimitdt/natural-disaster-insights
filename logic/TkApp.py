import tkinter as tk
from tkinter import ttk, messagebox
import requests

class TkApp:
    API_URL = "http://127.0.0.1:5000"

    def __init__(self, master):
        master.title("Data Engineering App")
        self.master = master

        # Tabbed interface
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        # Add tabs
        self.create_filter_sales_tab()

    def create_filter_sales_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Filter Sales")

        # Date filter inputs
        ttk.Label(frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        self.start_date = ttk.Entry(frame)
        self.start_date.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
        self.end_date = ttk.Entry(frame)
        self.end_date.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Fetch Sales", command=self.fetch_sales).grid(row=2, column=0, columnspan=2, pady=10)

    def fetch_sales(self):
        start_date = self.start_date.get()
        end_date = self.end_date.get()

        try:
            response = requests.get(f"{self.API_URL}/sales", params={"start_date": start_date, "end_date": end_date})
            response.raise_for_status()
            sales = response.json()

            # Display results
            result_window = tk.Toplevel(self.master)
            result_window.title("Sales Data")
            for i, sale in enumerate(sales):
                ttk.Label(result_window, text=str(sale)).grid(row=i, column=0, padx=10, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch sales: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = TkApp(root)
    root.mainloop()