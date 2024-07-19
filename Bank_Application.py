# main.py

from Bank_Database import *

print("YONO Bank Application".center(100, '-'))

# Create the database and table
create_database_connection()

# Main application loop
while True:
    choice = input("""
               1: Sign Up
               2: Login
               Press anything else to exit
               """)

    if choice == "1":
        sign_up()
    elif choice == "2":
        login()
    else:
        print("Exiting This Application....")
        exit()



