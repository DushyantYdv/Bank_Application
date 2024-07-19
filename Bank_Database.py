import mysql.connector

# Establish a connection to the MySQL database
def create_database_connection():
    global conn, cu

    conn = mysql.connector.connect(
        user="root",
        host="localhost",
        password="12345"
    )

    cu = conn.cursor()
    
    # Create database if it does not exist
    cu.execute("CREATE DATABASE IF NOT EXISTS YONO_BANK")
    cu.execute("USE YONO_BANK")
    
    # Create customer table if it does not exist
    cu.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            acc_no INT AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL,
            dob DATE NOT NULL,
            amount FLOAT NOT NULL,
            PRIMARY KEY (acc_no)
        );
    """)

    # Set the initial AUTO_INCREMENT value
    cu.execute("ALTER TABLE customer AUTO_INCREMENT = 100000")

# Sign up new customers
def sign_up():
    print("SIGN UP WINDOW".center(100, '-'))
    
    # Collect user information
    name = input("Enter the Name: ")
    email = input("Enter the Email: ")
    password = input("Enter the Password: ")
    dob = input("Enter the DOB (YYYY-MM-DD): ")
    amount = float(input("Enter the Amount: "))

    # Insert the collected data into the database
    query = """
    INSERT INTO customer (name, email, password, dob, amount)
    VALUES (%s, %s, %s, %s, %s)
    """
    cu.execute(query, (name, email, password, dob, amount))
    conn.commit() 

    # Retrieve the account number for the newly created account
    cu.execute("SELECT acc_no FROM customer WHERE name = %s AND email = %s", (name, email))
    account_db = cu.fetchone()
    
    if account_db:
        print(f"Congratulations! Account Created Successfully, Account No: {account_db[0]}")
    else:
        print("Error: Account number not found.")

# Login existing customers
def login():
    print("LOGIN WINDOW".center(100, '-'))
    
    # Collect login credentials
    email = input("Enter the Email: ")
    password = input("Enter the Password: ")

    # Validate credentials against the database
    cu.execute("SELECT * FROM customer WHERE email = %s AND password = %s", (email, password))
    user = cu.fetchone()
    
    if user:
        print("Login successful!")
        print(user)
        login_menu(email, password)
    else:
        print("Login failed! Check your email and password.")

# Display menu after successful login
def login_menu(email, password):
    print("WELCOME TO YOUR SESSION IN YONO BANK".center(100, '-'))

    while True:
        # Display options to the user
        choice = input("""
                    1. Deposit Money
                    2. Withdraw Money
                    3. Change Email
                    4. Change Password
                    5. Change Date Of Birth
                    6. Check Balance
                    Press Enter To Exit......""")

        # Call the respective function based on user's choice
        if choice == "1":
            deposit_money(email, password)
        elif choice == "2":
            withdraw_money(email, password)
        elif choice == "3":
            change_email(email, password)
        elif choice == "4":
            change_pass(email, password)
        elif choice == "5":
            change_dob(email, password)
        elif choice == "6":
            check_balance(email, password)
        else:
            print("Exiting The Application.....")
            break

# Function to deposit money
def deposit_money(email, password):
    cu.execute("SELECT amount FROM customer WHERE email = %s AND password = %s", (email, password))
    balance_db = cu.fetchone()

    if balance_db:
        current_balance = balance_db[0]
        print(f"Current Balance: {current_balance}")

        amount = float(input("Enter Amount To Deposit: "))
        if amount > 0:
            updated_balance = current_balance + amount
            cu.execute("UPDATE customer SET amount = %s WHERE email = %s AND password = %s", (updated_balance, email, password))
            conn.commit()

            print(f"Congratulations! Your balance was deposited successfully. Updated Balance = {updated_balance}")
        else:
            print("Invalid deposit amount. Please enter a positive amount.")
    else:
        print("Incorrect email or password.")

# Function to withdraw money
def withdraw_money(email, password):
    cu.execute("SELECT amount FROM customer WHERE email = %s AND password = %s", (email, password))
    balance_db = cu.fetchone()

    if balance_db:
        current_balance = balance_db[0]
        print(f"Current Balance: {current_balance}")

        amount = float(input("Enter Amount To Withdraw: "))
        if amount > 0 and amount <= current_balance:
            updated_balance = current_balance - amount
            cu.execute("UPDATE customer SET amount = %s WHERE email = %s AND password = %s", (updated_balance, email, password))
            conn.commit()

            print(f"Congratulations! Your {amount} was withdrawn successfully. Updated Balance = {updated_balance}")
        else:
            print("Invalid withdraw amount. Please enter an amount less than or equal to your current balance.")
    else:
        print("Incorrect email or password.")

# Function to change email
def change_email(email, password):
    new_email = input("Enter Your New Email: ")
    cu.execute("UPDATE customer SET email = %s WHERE email = %s AND password = %s", (new_email, email, password))
    conn.commit()
    print("Congrats! Email changed successfully. Updated Email =", new_email)

# Function to change password
def change_pass(email, password):
    new_password = input("Enter Your New Password: ")
    conf_password = input("Confirm Your New Password: ")

    if new_password == conf_password:
        cu.execute("UPDATE customer SET password = %s WHERE email = %s AND password = %s", (new_password, email, password))
        conn.commit()
        print("Congrats! Password changed successfully. Updated Password =", new_password)
    else:
        print("New Password and Confirm Password do not match.")
        print("Exiting the application...")

# Function to change date of birth
def change_dob(email, password):
    new_dob = input("Enter Date Of Birth In YYYY-MM-DD Format: ")
    cu.execute("UPDATE customer SET dob = %s WHERE email = %s AND password = %s", (new_dob, email, password))
    conn.commit()
    print("Congrats! Date of Birth changed successfully. Updated DOB =", new_dob)

# Function to check account balance
def check_balance(email, password):
    cu.execute("SELECT amount FROM customer WHERE email = %s AND password = %s", (email, password))
    balance_db = cu.fetchone()

    if balance_db:
        print("Your Account Balance:", balance_db[0])
    else:
        print("Incorrect email or password.")

