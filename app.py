import tkinter as tk
from tkinter import ttk
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# ================= FUNCTIONS ================= #

def add_expense():
    name = entry_name.get()
    category = entry_category.get()
    amount = entry_amount.get()
    date = datetime.now().strftime("%Y-%m")

    if name == "" or category == "" or amount == "":
        result_label.config(text="⚠️ Please fill all fields")
        return

    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, category, amount, date])

    result_label.config(text=f"Added: {name} | {category} | ₹{amount}")

    entry_name.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)


def read_data():
    data = {}
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[1]
                amount = float(row[2])
                data[category] = data.get(category, 0) + amount
    except:
        pass
    return data


def show_graph():
    data = read_data()
    if not data:
        result_label.config(text="No data to show")
        return

    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    plt.title("Expense Distribution")
    plt.show()


def show_bar_chart():
    data = read_data()
    if not data:
        result_label.config(text="No data to show")
        return

    plt.bar(data.keys(), data.values())
    plt.title("Category-wise Spending")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.show()


def show_insight():
    data = read_data()
    if not data:
        result_label.config(text="No data available")
        return

    max_category = max(data, key=data.get)
    result_label.config(text=f"⚠️ You spend most on: {max_category}")


def show_monthly_trend():
    monthly = {}

    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                month = row[3]
                amount = float(row[2])
                monthly[month] = monthly.get(month, 0) + amount
    except:
        pass

    if not monthly:
        result_label.config(text="No data available")
        return

    plt.plot(list(monthly.keys()), list(monthly.values()), marker='o')
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.show()


def clear_all_data():
    try:
        with open("expenses.csv", "w", newline="") as file:
            pass
        result_label.config(text="🗑️ All expenses cleared!")
    except:
        result_label.config(text="Error clearing data")


def show_table():
    table_window = tk.Toplevel(root)
    table_window.title("All Expenses")

    tree = ttk.Treeview(table_window, columns=("Name", "Category", "Amount", "Month"), show='headings')

    tree.heading("Name", text="Name")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    tree.heading("Month", text="Month")

    tree.pack(fill="both", expand=True)

    # Load data
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", tk.END, values=row)
    except:
        pass

    # Delete function
    def delete_selected():
        selected_item = tree.selection()
        if not selected_item:
            return

        values = tree.item(selected_item)['values']
        tree.delete(selected_item)

        updated_rows = []
        try:
            with open("expenses.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row != list(map(str, values)):
                        updated_rows.append(row)
        except:
            pass

        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

    tk.Button(table_window, text="Delete Selected", bg="red", fg="white", command=delete_selected).pack(pady=10)


# ================= LOGIN SYSTEM ================= #

def open_main_app():
    login_window.destroy()
    root.deiconify()


def check_login():
    username = entry_user.get()
    password = entry_pass.get()

    if username == "swasti" and password == "1308":
        open_main_app()
    else:
        login_status.config(text="❌ Invalid Login")


# ================= GUI ================= #

root = tk.Tk()
root.title("Smart Personal Finance Analyzer")
root.geometry("420x500")
root.withdraw()  # hide main window first

# Inputs
tk.Label(root, text="Expense Name").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Category").grid(row=1, column=0, padx=10, pady=5)
entry_category = tk.Entry(root)
entry_category.grid(row=1, column=1)

tk.Label(root, text="Amount").grid(row=2, column=0, padx=10, pady=5)
entry_amount = tk.Entry(root)
entry_amount.grid(row=2, column=1)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).grid(row=3, column=0, columnspan=2, pady=10)

tk.Button(root, text="Show Pie Chart", command=show_graph).grid(row=4, column=0, columnspan=2)

tk.Button(root, text="Bar Chart", command=show_bar_chart).grid(row=5, column=0, columnspan=2)

tk.Button(root, text="Monthly Trend", command=show_monthly_trend).grid(row=6, column=0, columnspan=2)

tk.Button(root, text="Show Table", command=show_table).grid(row=7, column=0, columnspan=2)

tk.Button(root, text="Smart Insight", command=show_insight).grid(row=8, column=0, columnspan=2)

tk.Button(root, text="Clear All Data", command=clear_all_data, bg="red", fg="white").grid(row=9, column=0, columnspan=2, pady=5)

# Result label
result_label = tk.Label(root, text="", fg="blue")
result_label.grid(row=10, column=0, columnspan=2, pady=10)

# ================= LOGIN WINDOW ================= #

login_window = tk.Toplevel()
login_window.title("Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack(pady=5)
entry_user = tk.Entry(login_window)
entry_user.pack()

tk.Label(login_window, text="Password").pack(pady=5)
entry_pass = tk.Entry(login_window, show="*")
entry_pass.pack()

tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

login_status = tk.Label(login_window, text="", fg="red")
login_status.pack()

root.mainloop()