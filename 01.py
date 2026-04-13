import csv
import matplotlib.pyplot as plt

expenses = []

# Load previous data from CSV
try:
    with open("expenses.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            expenses.append((row[0], row[1], float(row[2])))
except:
    pass

while True:
    print("\n1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expense")
    print("4. Show Graph")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter expense name: ")
        category = input("Enter category (Food/Travel/etc): ")
        amount = float(input("Enter amount: "))

        expenses.append((name, category, amount))

        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, category, amount])

        print("Expense saved!")

    elif choice == "2":
        print("\nYour Expenses:")
        for item in expenses:
            print(item[0], "|", item[1], "|", item[2])

    elif choice == "3":
        total = sum(x[2] for x in expenses)
        print("Total Expense:", total)

    elif choice == "4":
        category_data = {}

        for item in expenses:
            category = item[1]
            amount = item[2]
            if category in category_data:
                category_data[category] += amount
            else:
                category_data[category] = amount

        labels = list(category_data.keys())
        values = list(category_data.values())

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Expense Distribution")
        plt.show()

    elif choice == "5":
        print("Bye!")
        break

    else:
        print("Invalid choice")