import os
import sqlite3
from termcolor import colored
from prettytable import PrettyTable
from collections import Counter

# Check if the database file exists
if not os.path.exists('inventory.db'):
    # Create a connection to the database
    db_conn = sqlite3.connect('inventory.db')

    # Create a cursor object to execute SQL statements
    db_cursor = db_conn.cursor()

    db_cursor.execute("CREATE TABLE inventory (id INTEGER PRIMARY KEY, name TEXT)")
else: 
        
    # Create a connection to the database
    db_conn = sqlite3.connect('inventory.db')
        
    # Create a cursor object to execute SQL statements
    db_cursor = db_conn.cursor()

# Add a new item to the inventory
def add_item(name):
    # Split the input string on the comma character to get a list of values
    values = name.split(",")

    # Add each value to the database
    for value in values:
        db_cursor.execute("INSERT INTO inventory (name) VALUES (?)", (value,))
    db_conn.commit()

def delete_item():
    # Show the contents of the inventory in a table
    db_cursor.execute("SELECT * FROM inventory")
    items = db_cursor.fetchall()

    if items:
        # Count the occurrences of each item in the database
        item_counts = Counter(item[1] for item in items)

        table = PrettyTable()
        table.field_names = ["ID", "Item", "Count"]
        for item, count in item_counts.items():
            # Create a comma-separated list of the IDs of the items with the same value
            ids = [i[0] for i in items if i[1] == item]
            ids_str = ", ".join(str(i) for i in ids)
            table.add_row([ids_str, item, count])

        print(table)

        # Prompt the user to enter the ID of the item to delete
        id = input("Enter the ID of the item to delete: ")

        if(id == 'exit'):
            exit()
        else:
            # Split the input string on the comma character to get a list of IDs
            ids = id.split(",")
            for item_id in ids:
                # Delete the item from the inventory
                db_cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            db_conn.commit()
    else:
        print(colored('No items found', 'red'))

def search_item(name):
    # Search for items in the inventory with a given name
    db_cursor.execute("SELECT * FROM inventory WHERE name LIKE ?", (name,))
    items = db_cursor.fetchall()
    # Print the number of items on the search result
    if(len(items) > 0):
        print(colored(f"{len(items)} items found on the search result:", "green"))
    else:
        print(colored("No items found", "red"))

# Add a value to the database multiple times
def multiple(name, times):
    for i in range(times):
        add_item(name)

# Main program loop
while True:
    # Display the menu and get the user's input
    print("1. Add an item")
    print("3. Delete an item")
    print("4. Search for an item")
    print("5. Add Multiple items")
    print("6. Exit")
    choice = input("Enter your choice: ")

    # Add an item to the inventory
    if choice == "1":
        name = input("Enter the item value: ")
        add_item(name)
    # Delete an item from the inventory
    elif choice == "3":
        delete_item()
    # Search for items in the inventory
    elif choice == "4":
        name = input("Enter the search term: ")
        search_item(name)
    # Add Multiple items given the value and times
    elif choice == "5":
        item_value = input("Enter the item value: ")
        times = input("How many times do you want this to be added: ")
        multiple(item_value, times)
    # Exit the program
    elif choice == "6":
        break
    else:
        print("Invalid choice. Try again.")

# Close the connection to the database
db_conn.close()