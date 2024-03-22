"""
Student: Joseph Murphy
Team: The Fellowship of The Code
CIST 05B
Description:a menu-driven program for De Anza College Food Court,Use a data structure to save the quantities
            of the order. 
Date: 02/27/2024
"""
from typing import List, Any


# Define the superclass
class MenuItem:

    def __init__(self, name: object, price: object, size: object) -> object:
        self.name = name
        self.price = price
        self.size = size

    def display(self):
        return f"{self.name} - ${self.price:.2f}"


# Define the subclasses
class Burger(MenuItem):
    def __init__(self, name, price, patty_type, none=None):
        super().__init__(name, price, size=none)
        self.patty_type = patty_type


class Drink(MenuItem):
    def __init__(self, name, price, size):
        super().__init__(name, price, size)
        self.size = size


class Side(MenuItem):
    def __init__(self, name, price, size):
        assert isinstance(size, object)
        super().__init__(name, price, size)
        self.size = size


def get_user_status():
    """
    Ask the user whether he/she is a student or a staff.
    """
    while True:
        user_input = input("Are you a student? (y/n): ").lower()
        if user_input == 'y':
            return True  # Student
        elif user_input == 'n':
            return False  # Staff
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def main():
    order_instance = Order()

    while True:
        order_instance.display_menu()
        order_instance.get_inputs()
        is_student = get_user_status()  # Ask if user is a student
        order_instance.calculate(is_student)  # Pass is_student argument here
        order_instance.print_bill()
        order_instance.save_to_file()

        user_input_to_continue = input("Continue for another order (Any keys= Yes, n= No)?")

        order_instance.order_items = []

        if user_input_to_continue.lower() == 'n':
            print("The system is shutting down!")
            break


class Order:
    """
    Class representing an order at the De Anza College Food Court.
    """
    total_after_tax: None
    tax: None
    order_items: list[Any]
    menu: list[Burger | Side | Drink]

    def __init__(self):
        self.total_after_tax = None
        self.tax = None
        self.menu = [
            Burger("Cheeseburger", 5.99, "Beef"),
            Burger("Veggie Burger", 4.99, "Vegetarian"),
            Side("Fries", 2.99, "Regular"),
            Side("Onion Rings", 2.99, "Regular"),
            Drink("Soda", 1.99, "Medium"),
            Drink("Water", 0.99, "Small")
        ]
        self.order_items = []

    def display_menu(self):
        """
        Display the food menu to the user.
        """
        print("----------- Food Court Menu -----------")
        for index, item in enumerate(self.menu, start=1):
            print(f"{index}. {item.display()}")

    def get_inputs(self):
        """
        Ask the user what he/she wants and how many of them.
        """
        while True:
            try:
                choice = int(input("Enter the item number you want to order (or 6 to exit): "))
                if choice == 6:
                    break
                elif 1 <= choice <= len(self.menu):
                    quantity = int(input("Enter the quantity: "))
                    if quantity > 0:
                        self.order_items.append((self.menu[choice - 1], quantity))
                    else:
                        print("Invalid quantity. Please enter a positive number.")
                else:
                    print("Invalid item number. Please choose a valid item.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def calculate(self, is_student=False):
        """
        Calculate the total price of the order and apply tax.
        """
        total_before_tax = sum(item[0].price * item[1] for item in self.order_items)
        tax_rate = 0.09 if not is_student else 0  # Apply tax only if not a student
        self.tax = total_before_tax * tax_rate
        self.total_after_tax = total_before_tax + self.tax

    def print_bill(self):
        """
        Print the bill to the user.
        """
        print("\n----------- Your Bill -----------")
        for item, quantity in self.order_items:
            print(f"{item.name} x {quantity}: ${item.price * quantity:.2f}")
        print(f"\nTotal Before Tax: ${sum(item[0].price * item[1] for item in self.order_items):.2f}")
        print(f"Tax: ${self.tax:.2f}")
        print(f"Total After Tax: ${self.total_after_tax:.2f}")

    def save_to_file(self):
        """
        Save the bill to a file named 'order.txt'.
        """
        order_timestamp = "order.txt"
        with open(order_timestamp, 'w') as file_handle_to_save_the_bill:
            file_handle_to_save_the_bill.write("----------- Your Bill -----------\n")
            for item, quantity in self.order_items:
                file_handle_to_save_the_bill.write(f"{item.name} x {quantity}: ${item.price * quantity:.2f}\n")
            file_handle_to_save_the_bill.write(
                f"\nTotal Before Tax: ${sum(item[0].price * item[1] for item in self.order_items):.2f}\n")
            file_handle_to_save_the_bill.write(f"Tax: ${self.tax:.2f}\n")
            file_handle_to_save_the_bill.write(f"Total After Tax: ${self.total_after_tax:.2f}\n")

    # CRUD

    def add_order(self, item_name, quantity):
        """
        Add a new order item to the order.
        """
        # Find the item object from the menu using its name
        item = None
        for menu_item in self.menu:
            if menu_item.name == item_name:
                item = menu_item
                break

        if item:
            self.order_items.append((item, quantity))
        else:
            print(f"Item '{item_name}' not found in the menu.")

    def read_order(self):
        """
        Read or print the current order with prices.
        """
        print("\n----------- Current Order -----------")
        for item, quantity in self.order_items:
            total_price = item.price * quantity
            print(f"{item.name} x {quantity}: ${total_price:.2f} ({item.price:.2f} each)")
        print("-------------------------------------")

    def update_order(self, item_index, new_quantity):
        """
        Update and edit the quantity of an order item.
        """
        if 0 <= item_index < len(self.order_items):
            self.order_items[item_index] = (self.order_items[item_index][0], new_quantity)
            print("Order item updated successfully.")
        else:
            print("Invalid item index.")

    def delete_order(self, item_index):
        """
        Delete an order item.
        """
        if 0 <= item_index < len(self.order_items):
            del self.order_items[item_index]
            print("Order item deleted successfully.")
        else:
            print("Invalid item index.")


if __name__ == "__main__":
    main()

"""
----------- Food Court Menu -----------
1. Cheeseburger - $5.99
2. Veggie Burger - $4.99
3. Fries - $2.99
4. Onion Rings - $2.99
5. Soda - $1.99
6. Water - $0.99
Enter the item number you want to order (or 6 to exit): 3
Enter the quantity: 2
Enter the item number you want to order (or 6 to exit): 1
Enter the quantity: 2
Enter the item number you want to order (or 6 to exit): 6
Are you a student? (y/n): y

----------- Your Bill -----------
Fries x 2: $5.98
Cheeseburger x 2: $11.98

Total Before Tax: $17.96
Tax: $0.00
Total After Tax: $17.96
Continue for another order (Any keys= Yes, n= No)?y
----------- Food Court Menu -----------
1. Cheeseburger - $5.99
2. Veggie Burger - $4.99
3. Fries - $2.99
4. Onion Rings - $2.99
5. Soda - $1.99
6. Water - $0.99
Enter the item number you want to order (or 6 to exit): 1
Enter the quantity: 5
Enter the item number you want to order (or 6 to exit): 1
Enter the quantity: 0
Invalid quantity. Please enter a positive number.
Enter the item number you want to order (or 6 to exit): 2
Enter the quantity: 3
Enter the item number you want to order (or 6 to exit): 5
Enter the quantity: 4
Enter the item number you want to order (or 6 to exit): 6
Are you a student? (y/n): n

----------- Your Bill -----------
Cheeseburger x 5: $29.95
Veggie Burger x 3: $14.97
Soda x 4: $7.96

Total Before Tax: $52.88
Tax: $4.76
Total After Tax: $57.64
Continue for another order (Any keys= Yes, n= No)?n
The system is shutting down!

Process finished with exit code 0
"""

"""
----------- Food Court Menu -----------
1. Cheeseburger - $5.99
2. Veggie Burger - $4.99
3. Fries - $2.99
4. Onion Rings - $2.99
5. Soda - $1.99
6. Water - $0.99
Enter the item number you want to order (or 6 to exit): 30
Invalid item number. Please choose a valid item.
Enter the item number you want to order (or 6 to exit): f
Invalid input. Please enter a number.
Enter the item number you want to order (or 6 to exit): .
Invalid input. Please enter a number.
Enter the item number you want to order (or 6 to exit): 1
Enter the quantity: g
Invalid input. Please enter a number.
Enter the item number you want to order (or 6 to exit): 2
Enter the quantity: 2
Enter the item number you want to order (or 6 to exit): 6
Are you a student? (y/n): h
Invalid input. Please enter 'y' for yes or 'n' for no.
Are you a student? (y/n): y

----------- Your Bill -----------
Veggie Burger x 2: $9.98

Total Before Tax: $9.98
Tax: $0.00
Total After Tax: $9.98
Continue for another order (Any keys= Yes, n= No)?n
The system is shutting down!
"""
