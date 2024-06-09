import mysql.connector
import re

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='milk_store'
    )
menu3 = {
    "1":"Yoghurt",
    "2":"Milk",
    "3":"Cheese",
    "4":"Exit"
}
menu1 = {
    "1": "Register",
    "2": "Login",
    "3": "Exit"
}
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

def is_valid_phone_number(phone_number):
    return re.match(r'^(078|079|072|073)\d{7}$', phone_number)

def is_valid_pin(pin):
    return re.match(r'^\d{4}$', pin)

def register_customer():
    print("Customer Information ...")
    cust_id = input("Customer ID: ")
    cust_email = input("Email: ")
    cust_phone = input("Phone Number: ")
    cust_road_nbr = input("Road Number: ")
    cust_pin = input("PIN: ")

    if not is_valid_email(cust_email):
        print("Invalid email address. Please try again.")
        return

    if not is_valid_phone_number(cust_phone):
        print("Invalid phone number. It must start with 078, 079, 072, or 073 and be 10 digits long.")
        return

    if not is_valid_pin(cust_pin):
        print("Invalid PIN. It must be 4 digits long.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customers (C_id, Email, Phone, Road_nbr, Pin) VALUES (%s, %s, %s, %s, %s)',
                   (cust_id, cust_email, cust_phone, cust_road_nbr, cust_pin))
    conn.commit()
    cursor.close()
    conn.close()
    print("Registration is successful, please place your order now")
    print("________________________________________________________________")

def login_customer():
    print("Customer Login ...")
    username = input("Email or Phone Number: ")
    pin = input("PIN: ")

    if not is_valid_pin(pin):
        print("Invalid PIN. It must be 4 digits long.")
        return None

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT C_id, Email, Phone FROM customers WHERE (Email = %s OR Phone = %s) AND Pin = %s',
                   (username, username, pin))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        cust_id, email, phone = result
        print(f"Login successful for Customer ID: {cust_id}")
        return cust_id
    else:
        print("Invalid username or PIN. Please try again.")
        return None

def place_order(cust_id):
    while True:
        print("Select Product: ")
        for option, action in menu3.items():
            print(f"{option}. {action}")

        product_input = input("")
        
        if product_input in ["1", "2", "3"]:
            process_product_order(cust_id, product_input)
        elif product_input == "4":
            break
        else:
            print("Invalid Product, Try Again!")

def process_product_order(cust_id, product_input):
    if product_input == "1":
        product_name = "Yoghurt"
    elif product_input == "2":
        product_name = "Milk"
    elif product_input == "3":
        product_name = "Cheese"
    
    size = get_size_options(product_name)
    
    print("Select Size: ")
    for option, action in size.items():
        print(f"{option}. {action}")
    size_input = input("")
    
    if size_input in size:
        p_categ = size[size_input]
        qnty = int(input("Enter Quantity: "))
        confirm_order(cust_id, product_name, p_categ, qnty)
    else:
        print("Invalid Choice, Try Again!")

def get_size_options(product_name):
    if product_name == "Yoghurt":
        return {"1": "Big", "2": "Medium", "3": "Small"}
    elif product_name == "Milk":
        return {"1": "5L", "2": "3L", "3": "1L", "4": "250Ml"}
    elif product_name == "Cheese":
        return {"1": "Good"}

def confirm_order(cust_id, p_name, p_categ, qnty):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT P_id, P_name, P_unitprice, P_category FROM products WHERE P_name = %s AND P_category = %s',
                   (p_name, p_categ))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        p_id, name, price, categ = result
        print(f"Product: {name}")
        print(f"Size: {categ}")
        print(f"Quantity: {qnty}")
        total = price * qnty
        print(f"Total Price: {total}")

        confirm = input("1. Confirm\n2. Cancel\n")
        if confirm == "1":
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO orders (C_id, P_id, Order_amount, Order_totalprice) VALUES (%s, %s, %s, %s)',
                           (cust_id, p_id, qnty, total))
            conn.commit()
            cursor.close()
            conn.close()
            print("Thank You for making Order, Your Order is Received!")
        elif confirm == "2":
            print("Order Cancelled")
        else:
            print("Invalid Choice, Try Again!")
    else:
        print("Product not found.")

def main_menu():
    while True:
        print("Welcome to MUKAMIRA Dairy Ltd")
        for option, action in menu1.items():
            print(f"{option}. {action}")
        cust_input = input("")

        if cust_input == "1":
            register_customer()
        elif cust_input == "2":
            cust_id = login_customer()
            if cust_id:
                place_order(cust_id)
        elif cust_input == "3":
            break
        else:
            print("Invalid Choice, Try Again!")

if __name__ == "__main__":
    ussd = input("")
    if ussd == "*102#":
        main_menu()
    else:
        print("Unknown USSD code.")
