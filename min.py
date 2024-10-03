
import os
import tkinter as tk
from tkinter import ttk, messagebox
import json
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.logged_in = False

        if not os.path.exists("expenses.json"):
            with open("expenses.json", "w"):
                pass

    def login(self):
        
        username = self.username_entry.get()
        password = self.password_entry.get()

        
        if username == "admin" and password == "12341234":
            self.logged_in = True
            messagebox.showinfo("Login", "Login successful!")
            self.load_expenses()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def load_expenses(self):
        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.grid(row=4, column=0, padx=5, pady=5)
        self.selected_category = ttk.Combobox(root, values=["Food", "Transportation", "Entertainment", "Salary", "Other"])
        self.selected_category.grid(row=4, column=1, padx=5, pady=5)

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=5, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=5, column=1, padx=5, pady=5)

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        self.columns = ("Date", "Category", "Amount")
        self.expenses_tree = ttk.Treeview(root, columns=self.columns, show="headings")
        self.expenses_tree.heading("Date", text="Date")
        self.expenses_tree.heading("Category", text="Category")
        self.expenses_tree.heading("Amount", text="Amount")
        self.expenses_tree.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.total_label = tk.Label(root, text="")
        self.total_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.view_button = tk.Button(root, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=10, column=0, padx=5, pady=10)

        self.delete_button = tk.Button(root, text="Delete Expense", command=self.delete_expense)
        self.delete_button.grid(row=10, column=1, padx=5, pady=10)

        self.show_chart_button = tk.Button(root, text="Show Expenses Chart", command=self.show_expenses_chart)
        self.show_chart_button.grid(row=11, column=0, columnspan=2, padx=5, pady=10)

        self.show_reports_button = tk.Button(root, text="Generate Basic Reports", command=self.show_basic_reports)
        self.show_reports_button.grid(row=12, column=0, columnspan=2, padx=5, pady=10)

        self.view_expenses()

    def add_expense(self):
        if not self.logged_in:
            messagebox.showerror("Access Denied", "Please log in first.")
            return

        date = self.date_entry.get()
        category = self.selected_category.get()
        amount = self.amount_entry.get()

        if date and category and amount:
            with open("expenses.json", "a") as file:
                data = {"date": date, "category": category, "amount": amount}
                json.dump(data, file)
                file.write("\n")
            self.status_label.config(text="Expense added successfully!", fg="green")
            self.date_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.view_expenses()
        else:
            self.status_label.config(text="Please fill all the fields!", fg="red")

    def delete_expense(self):
        if not self.logged_in:
            messagebox.showerror("Access Denied", "Please log in first.")
            return

        selected_item = self.expenses_tree.selection()
        if selected_item:
            item_text = self.expenses_tree.item(selected_item, "values")
            date, category, amount = item_text
            with open("expenses.json", "r") as file:
                data = file.readlines()
            with open("expenses.json", "w") as file:
                for line in data:
                    if json.loads(line.strip()) != {"date": date, "category": category, "amount": amount}:
                        file.write(line)
            self.status_label.config(text="Expense deleted successfully!", fg="green")
            self.view_expenses()
        else:
            self.status_label.config(text="Please select an expense to delete!", fg="red")

    def view_expenses(self):
        if os.path.exists("expenses.json"):
            total_expense = 0
            self.expenses_tree.delete(*self.expenses_tree.get_children())
            with open("expenses.json", "r") as file:
                for line in file:
                    data = json.loads(line.strip())
                    date, category, amount = data["date"], data["category"], data["amount"]
                    self.expenses_tree.insert("", tk.END, values=(date, category, amount))
                    total_expense += float(amount)
            self.total_label.config(text=f"Total Expense:{total_expense:.2f}")
            total_income = self.get_total_income()
            self.total_label.config(text=f"Total Expense: {total_expense:.2f}, Total Income: {total_income:.2f}")
        else:
            self.total_label.config(text="No expenses recorded.")
            self.expenses_tree.delete(*self.expenses_tree.get_children())

    def show_expenses_chart(self):
        categories = []
        amounts = []
        with open("expenses.json", "r") as file:
            for line in file:
                data = json.loads(line.strip())
                categories.append(data["category"])
                amounts.append(float(data["amount"]))
        category_expense = {}
        for category, amount in zip(categories, amounts):
            category_expense[category] = category_expense.get(category, 0) + amount
        categories = list(category_expense.keys())
        expenses = list(category_expense.values())
        plt.figure(figsize=(8, 6))
        plt.pie(expenses, labels=categories, autopct="%1.1f%%", startangle=140, shadow=True)
        plt.axis("equal")
        plt.title("Expense Categories Distribution")
        plt.show()

    def show_basic_reports(self):
        total_expenses = self.get_total_expenses()
        total_income = self.get_total_income()
        spending_by_category = self.get_spending_by_category()
        transactions_by_category = self.get_transactions_by_category()
        average_transaction_value_by_category = self.get_average_transaction_value_by_category()

        report_text = f"Total Expenses: {total_expenses:.2f}\n\n"
        report_text += f"Total Income: {total_income:.2f}\n\n"
        report_text += "Spending by Category:\n"

        for category, amount in spending_by_category.items():
            report_text += f"{category}: {amount:.2f}\n"
        report_text += "\nTransactions by Category:\n"
        for category, transactions in transactions_by_category.items():
            report_text += f"{category}:\n"
            for transaction in transactions:
                report_text += f"{transaction}\n"
        report_text += "\nAverage Transaction Value by Category:\n"
        for category, average in average_transaction_value_by_category.items():
            report_text += f"{category}: {average:.2f}\n"

        messagebox.showinfo("Basic Reports", report_text)

    def get_total_expenses(self):
        total_expense = 0
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                for line in file:
                    data = json.loads(line.strip())
                    total_expense += float(data["amount"])
        return total_expense

    def get_total_income(self):
        total_income = 0
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                for line in file:
                    data = json.loads(line.strip())
                    if data["category"] == "Salary":
                        total_income += float(data["amount"])
                    else:
                        total_income -= float(data["amount"])
        return total_income

    def get_spending_by_category(self):
        categories = {}
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                for line in file:
                    data = json.loads(line.strip())
                    category = data["category"]
                    amount = float(data["amount"])
                    categories[category] = categories.get(category, 0) + amount
        return categories

    def get_transactions_by_category(self):
        transactions = {}
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                for line in file:
                    data = json.loads(line.strip())
                    category = data["category"]
                    transaction = f"Date: {data['date']}, Amount: {data['amount']}"
                    transactions.setdefault(category, []).append(transaction)
        return transactions

    def get_average_transaction_value_by_category(self):
        categories = {}
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as file:
                for line in file:
                    data = json.loads(line.strip())
                    category = data["category"]
                    amount = float(data["amount"])
                    categories.setdefault(category, [0, 0])
                    categories[category][0] += amount
                    categories[category][1] += 1

        averages = {category: total_amount / count for category, (total_amount, count) in categories.items()}
        return averages

root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()

