import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

class MySQLApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MySQL Operations with Python")
        self.master.geometry("600x400")
        self.conn = None
        self.cursor = None
        self.init_setup()
        
    def init_setup(self):
        self.setup_window = tk.Toplevel(self.master)
        self.setup_window.title("Database Setup")
        self.setup_window.geometry("400x200")
        
        self.db_label = tk.Label(self.setup_window, text="Enter MySQL Credentials")
        self.db_label.pack(pady=10)
        
        self.user_label = tk.Label(self.setup_window, text="Username:")
        self.user_label.pack()
        self.user_entry = tk.Entry(self.setup_window,show='*')
        self.user_entry.pack(pady=5)
        
        self.password_label = tk.Label(self.setup_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.setup_window, show='*')
        self.password_entry.pack(pady=5)
        
        self.create_db_button = tk.Button(self.setup_window, text="Create Database", command=self.create_database)
        self.create_db_button.pack(pady=10)
        
        self.enter_db_button = tk.Button(self.setup_window, text="Enter Existing Database", command=self.enter_database)
        self.enter_db_button.pack(pady=10)
    
    def create_database(self):
        username = self.user_entry.get()
        password = self.password_entry.get()
        
        database = simpledialog.askstring("Database Name", "Enter the name for the new database:", parent=self.setup_window)
        
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            self.conn.database = database
            messagebox.showinfo("Success", f"Database '{database}' created and connected successfully.")
            self.setup_window.destroy()
            self.main_window()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
    
    def enter_database(self):
        username = self.user_entry.get()
        password = self.password_entry.get()
        
        database = simpledialog.askstring("Database Name", "Enter the name of the existing database:", parent=self.setup_window)
        
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user=username,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            messagebox.showinfo("Success", f"Connected to database '{database}' successfully.")
            self.setup_window.destroy()
            self.main_window()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
    
    def main_window(self):
        self.label = tk.Label(self.master, text="Enter your SQL Query:")
        self.label.pack(pady=10)
        
        self.text = tk.Text(self.master, height=10, width=50)
        self.text.pack(pady=10)
        
        self.run_button = tk.Button(self.master, text="Run Query", command=self.run_query)
        self.run_button.pack(pady=10)
        
        self.result_label = tk.Label(self.master, text="Results:")
        self.result_label.pack(pady=10)
        
        self.result_text = tk.Text(self.master, height=10, width=50)
        self.result_text.pack(pady=10)
        
    def run_query(self):
        query = self.text.get("1.0", tk.END).strip()
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            self.result_text.delete("1.0", tk.END)
            for row in rows:
                self.result_text.insert(tk.END, str(row) + '\n')
            self.conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("SQL Error", str(e))
    
    def on_closing(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.master.destroy()


root = tk.Tk()
app = MySQLApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()

