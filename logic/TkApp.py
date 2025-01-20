import tkinter as tk
from tkinter import ttk
import psycopg2

class TkApp:
    def __init__(self, master):
        master.title("Data Engineering App")

        # Tabbed interface
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        # Sales filter tab
        self.sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sales_frame, text="Filter Sales")

        # Date filter inputs
        ttk.Label(self.sales_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        self.start_date = ttk.Entry(self.sales_frame)
        self.start_date.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.sales_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
        self.end_date = ttk.Entry(self.sales_frame)
        self.end_date.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self.sales_frame, text="Fetch Sales", command=self.fetch_sales).grid(row=2, column=0, columnspan=2, pady=10)

    def fetch_sales(self):
        start_date = self.start_date.get()
        end_date = self.end_date.get()

        try:
            conn = psycopg2.connect(
                dbname="my_project_db",
                user="your_username",
                password="your_password",
                host="localhost"
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM sales WHERE sale_date BETWEEN %s AND %s;", (start_date, end_date))
            sales = cur.fetchall()
            cur.close()
            conn.close()

            # Display results
            result_window = tk.Toplevel()
            result_window.title("Sales Data")
            for i, sale in enumerate(sales):
                ttk.Label(result_window, text=str(sale)).grid(row=i, column=0, padx=10, pady=5)

        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to fetch sales: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = TkApp(root)
    root.mainloop()