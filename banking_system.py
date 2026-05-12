import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime


class BankingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Banking System")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e293b")

        self.conn = sqlite3.connect("banking_system.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.current_user = None

        self.main_screen()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            account_number INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            balance REAL DEFAULT 0
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number INTEGER,
            type TEXT,
            amount REAL,
            date TEXT
        )
        ''')

        self.conn.commit()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def title_label(self, text):
        tk.Label(
            self.root,
            text=text,
            font=("Arial", 24, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(pady=20)

    def main_screen(self):
        self.clear_screen()

        self.title_label("Professional Banking System")

        frame = tk.Frame(self.root, bg="#334155", padx=40, pady=40)
        frame.pack(pady=50)

        tk.Button(
            frame,
            text="Create Account",
            width=25,
            height=2,
            bg="#0ea5e9",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.create_account_screen
        ).pack(pady=15)

        tk.Button(
            frame,
            text="Login",
            width=25,
            height=2,
            bg="#22c55e",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.login_screen
        ).pack(pady=15)

        tk.Button(
            frame,
            text="Exit",
            width=25,
            height=2,
            bg="#ef4444",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.root.quit
        ).pack(pady=15)

    def create_account_screen(self):
        self.clear_screen()
        self.title_label("Create New Account")

        frame = tk.Frame(self.root, bg="#334155", padx=30, pady=30)
        frame.pack(pady=20)

        tk.Label(frame, text="Full Name", bg="#334155", fg="white").grid(row=0, column=0, pady=10)
        name_entry = tk.Entry(frame, width=30)
        name_entry.grid(row=0, column=1)

        tk.Label(frame, text="Password", bg="#334155", fg="white").grid(row=1, column=0, pady=10)
        password_entry = tk.Entry(frame, show="*", width=30)
        password_entry.grid(row=1, column=1)

        tk.Label(frame, text="Initial Deposit", bg="#334155", fg="white").grid(row=2, column=0, pady=10)
        deposit_entry = tk.Entry(frame, width=30)
        deposit_entry.grid(row=2, column=1)

        def create_account():
            name = name_entry.get()
            password = password_entry.get()
            deposit = deposit_entry.get()

            if not name or not password or not deposit:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                deposit = float(deposit)
            except:
                messagebox.showerror("Error", "Deposit must be a number")
                return

            self.cursor.execute('''
            INSERT INTO users(name, password, balance)
            VALUES (?, ?, ?)
            ''', (name, password, deposit))

            self.conn.commit()

            account_number = self.cursor.lastrowid

            self.add_transaction(account_number, "Deposit", deposit)

            messagebox.showinfo(
                "Success",
                f"Account Created Successfully\n\nAccount Number: {account_number}"
            )

            self.main_screen()

        tk.Button(
            frame,
            text="Create Account",
            bg="#0ea5e9",
            fg="white",
            width=20,
            command=create_account
        ).grid(row=3, columnspan=2, pady=20)

        tk.Button(
            self.root,
            text="Back",
            command=self.main_screen
        ).pack()

    def login_screen(self):
        self.clear_screen()
        self.title_label("User Login")

        frame = tk.Frame(self.root, bg="#334155", padx=30, pady=30)
        frame.pack(pady=30)

        tk.Label(frame, text="Account Number", bg="#334155", fg="white").grid(row=0, column=0, pady=10)
        account_entry = tk.Entry(frame, width=30)
        account_entry.grid(row=0, column=1)

        tk.Label(frame, text="Password", bg="#334155", fg="white").grid(row=1, column=0, pady=10)
        password_entry = tk.Entry(frame, show="*", width=30)
        password_entry.grid(row=1, column=1)

        def login():
            account = account_entry.get()
            password = password_entry.get()

            self.cursor.execute('''
            SELECT * FROM users
            WHERE account_number=? AND password=?
            ''', (account, password))

            user = self.cursor.fetchone()

            if user:
                self.current_user = user[0]
                self.dashboard()
            else:
                messagebox.showerror("Error", "Invalid Login")

        tk.Button(
            frame,
            text="Login",
            bg="#22c55e",
            fg="white",
            width=20,
            command=login
        ).grid(row=2, columnspan=2, pady=20)

        tk.Button(
            self.root,
            text="Back",
            command=self.main_screen
        ).pack()

    def dashboard(self):
        self.clear_screen()

        self.title_label("Bank Dashboard")

        frame = tk.Frame(self.root, bg="#334155", padx=20, pady=20)
        frame.pack(pady=20)

        self.cursor.execute(
            "SELECT name, balance FROM users WHERE account_number=?",
            (self.current_user,)
        )

        user = self.cursor.fetchone()

        tk.Label(
            frame,
            text=f"Welcome, {user[0]}",
            font=("Arial", 18, "bold"),
            bg="#334155",
            fg="white"
        ).pack(pady=10)

        tk.Label(
            frame,
            text=f"Balance: ${user[1]:.2f}",
            font=("Arial", 16),
            bg="#334155",
            fg="#38bdf8"
        ).pack(pady=10)

        buttons_frame = tk.Frame(self.root, bg="#1e293b")
        buttons_frame.pack(pady=20)

        tk.Button(buttons_frame, text="Deposit", width=20, bg="#0ea5e9", fg="white", command=self.deposit_screen).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="Withdraw", width=20, bg="#f59e0b", fg="white", command=self.withdraw_screen).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="Transfer", width=20, bg="#8b5cf6", fg="white", command=self.transfer_screen).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="Transactions", width=20, bg="#22c55e", fg="white", command=self.transaction_screen).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="Logout", width=20, bg="#ef4444", fg="white", command=self.main_screen).grid(row=2, columnspan=2, pady=20)

    def deposit_screen(self):
        self.amount_window("Deposit")

    def withdraw_screen(self):
        self.amount_window("Withdraw")

    def amount_window(self, action):
        window = tk.Toplevel(self.root)
        window.title(action)
        window.geometry("350x200")

        tk.Label(window, text=f"{action} Amount", font=("Arial", 14)).pack(pady=20)

        amount_entry = tk.Entry(window, width=25)
        amount_entry.pack(pady=10)

        def submit():
            try:
                amount = float(amount_entry.get())
            except:
                messagebox.showerror("Error", "Invalid amount")
                return

            self.cursor.execute(
                "SELECT balance FROM users WHERE account_number=?",
                (self.current_user,)
            )

            balance = self.cursor.fetchone()[0]

            if action == "Withdraw" and amount > balance:
                messagebox.showerror("Error", "Insufficient Balance")
                return

            if action == "Deposit":
                self.cursor.execute(
                    "UPDATE users SET balance = balance + ? WHERE account_number=?",
                    (amount, self.current_user)
                )
                self.add_transaction(self.current_user, "Deposit", amount)

            else:
                self.cursor.execute(
                    "UPDATE users SET balance = balance - ? WHERE account_number=?",
                    (amount, self.current_user)
                )
                self.add_transaction(self.current_user, "Withdraw", amount)

            self.conn.commit()
            messagebox.showinfo("Success", f"{action} Successful")
            window.destroy()
            self.dashboard()

        tk.Button(window, text=action, command=submit).pack(pady=20)

    def transfer_screen(self):
        window = tk.Toplevel(self.root)
        window.title("Transfer Money")
        window.geometry("400x300")

        tk.Label(window, text="Receiver Account Number").pack(pady=10)
        receiver_entry = tk.Entry(window)
        receiver_entry.pack()

        tk.Label(window, text="Amount").pack(pady=10)
        amount_entry = tk.Entry(window)
        amount_entry.pack()

        def transfer():
            receiver = receiver_entry.get()

            try:
                amount = float(amount_entry.get())
            except:
                messagebox.showerror("Error", "Invalid amount")
                return

            self.cursor.execute(
                "SELECT balance FROM users WHERE account_number=?",
                (self.current_user,)
            )
            balance = self.cursor.fetchone()[0]

            if amount > balance:
                messagebox.showerror("Error", "Insufficient Balance")
                return

            self.cursor.execute(
                "SELECT * FROM users WHERE account_number=?",
                (receiver,)
            )

            if not self.cursor.fetchone():
                messagebox.showerror("Error", "Receiver not found")
                return

            self.cursor.execute(
                "UPDATE users SET balance = balance - ? WHERE account_number=?",
                (amount, self.current_user)
            )

            self.cursor.execute(
                "UPDATE users SET balance = balance + ? WHERE account_number=?",
                (amount, receiver)
            )

            self.conn.commit()

            self.add_transaction(self.current_user, "Transfer Sent", amount)
            self.add_transaction(receiver, "Transfer Received", amount)

            messagebox.showinfo("Success", "Transfer Successful")
            window.destroy()
            self.dashboard()

        tk.Button(window, text="Transfer", command=transfer).pack(pady=20)

    def transaction_screen(self):
        window = tk.Toplevel(self.root)
        window.title("Transaction History")
        window.geometry("700x400")

        tree = ttk.Treeview(window, columns=("Type", "Amount", "Date"), show="headings")

        tree.heading("Type", text="Transaction Type")
        tree.heading("Amount", text="Amount")
        tree.heading("Date", text="Date")

        tree.pack(fill="both", expand=True)

        self.cursor.execute(
            "SELECT type, amount, date FROM transactions WHERE account_number=? ORDER BY id DESC",
            (self.current_user,)
        )

        rows = self.cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)

    def add_transaction(self, account_number, transaction_type, amount):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute('''
        INSERT INTO transactions(account_number, type, amount, date)
        VALUES (?, ?, ?, ?)
        ''', (account_number, transaction_type, amount, date))

        self.conn.commit()


root = tk.Tk()
app = BankingSystem(root)
root.mainloop()
