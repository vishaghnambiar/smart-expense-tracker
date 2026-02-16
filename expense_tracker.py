import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "expenses.csv"
MONTHLY_BUDGET = 5000  # Change this to your desired monthly budget


# ------------------ DATA FUNCTIONS ------------------ #

def save_expense(amount, category, note):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Amount", "Category", "Note"])

        today = datetime.now().strftime("%Y-%m-%d")
        writer.writerow([today, amount, category, note])


def load_expenses():
    expenses = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)

    return expenses


# ------------------ BUDGET CHECK ------------------ #

def check_budget():
    expenses = load_expenses()
    current_month = datetime.now().strftime("%Y-%m")

    total = 0
    for exp in expenses:
        if exp["Date"].startswith(current_month):
            total += float(exp["Amount"])

    if total > MONTHLY_BUDGET:
        messagebox.showwarning(
            "Budget Exceeded!",
            f"You spent ₹{total} this month!\nBudget was ₹{MONTHLY_BUDGET}"
        )


# ------------------ CHART FUNCTION ------------------ #

def show_charts():
    expenses = load_expenses()

    if not expenses:
        messagebox.showinfo("No Data", "No expenses to show!")
        return

    category_totals = defaultdict(float)
    monthly_totals = defaultdict(float)

    for exp in expenses:
        category_totals[exp["Category"]] += float(exp["Amount"])

        month = exp["Date"][:7]  # YYYY-MM
        monthly_totals[month] += float(exp["Amount"])

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    months = sorted(monthly_totals.keys())
    monthly_amounts = [monthly_totals[m] for m in months]

    plt.figure(figsize=(10,5))

    # Pie Chart
    plt.subplot(1,2,1)
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Spending by Category")

    # Monthly Trend
    plt.subplot(1,2,2)
    plt.plot(months, monthly_amounts, marker="o")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount")

    plt.tight_layout()
    plt.show()


# ------------------ UI FUNCTIONS ------------------ #

def add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    note = note_entry.get()

    if not amount:
        messagebox.showerror("Error", "Amount required!")
        return

    try:
        float(amount)
    except:
        messagebox.showerror("Error", "Amount must be numeric!")
        return

    save_expense(amount, category, note)
    refresh_table()
    check_budget()

    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)


def refresh_table():
    for row in table.get_children():
        table.delete(row)

    expenses = load_expenses()

    for exp in expenses:
        table.insert("", tk.END, values=(
            exp["Date"],
            exp["Amount"],
            exp["Category"],
            exp["Note"]
        ))


# ------------------ MAIN WINDOW ------------------ #

root = tk.Tk()
root.title("Smart Expense Tracker")
root.geometry("700x450")

frame = tk.Frame(root)
frame.pack(pady=10)

# Amount
tk.Label(frame, text="Amount").grid(row=0, column=0, padx=5)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=0, column=1)

# Category Dropdown
tk.Label(frame, text="Category").grid(row=0, column=2, padx=5)
category_options = ["Food", "Travel", "Bills", "Shopping", "Health", "Other"]
category_entry = ttk.Combobox(frame, values=category_options, state="readonly")
category_entry.current(0)
category_entry.grid(row=0, column=3)

# Note
tk.Label(frame, text="Note").grid(row=1, column=0, padx=5)
note_entry = tk.Entry(frame, width=40)
note_entry.grid(row=1, column=1, columnspan=3)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="Show Analytics", command=show_charts).pack(pady=5)

# Table
columns = ("Date", "Amount", "Category", "Note")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")

table.pack(fill="both", expand=True)

refresh_table()

root.mainloop()
