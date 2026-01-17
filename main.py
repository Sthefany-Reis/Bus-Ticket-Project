# Bus Ticket booking System  

import csv  
import os
import re


# Admin login details (FOR NOW)
admLogin = {"name": "admin", "email": "admin@email.com", "password": "adm1", "role": "admin"}


# User class
class user():
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
    

# Main class
class main:
    def __init__(self): 
        self.usersList = []
        self.removeIdColumns()
        self.userFile()
        self.loadUsers()


    # Load users from the CSV file
    def loadUsers(self):
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.usersList.append({"name": row["name"], "email": row["email"], "password": row["password"], "role": row["role"]})

    # Create users.csv file if it does not exist
    def userFile(self):
        if not os.path.exists("users.csv"):
            with open("users.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["name", "email", "password", "role"])
                # Add admin login details to the file
                writer.writerow([admLogin["name"], admLogin["email"], admLogin["password"], admLogin["role"]])


    # Function to remove specific columns from the CSV file
    def removeIdColumns(self):
        deleteIdColumns = ["category_id", "topup_passenger_class_id", "topup_id"]
        # Handle the error if the products file does not exist
        if not os.path.exists("mobile_products.csv"):
            print("mobile_products.csv file does not exist")
        else:
        # Read the file content
            try:
                # Create an empty file if updated_file.csv does not exist
                if not os.path.exists("updated_file.csv"):
                    open("updated_file.csv", "a").close()

                # Open the CSV file for reading and writing
                with open("mobile_products.csv", "r") as file, \
                        open("updated_file.csv", "w", newline="") as newFile:
                    reader = csv.DictReader(file)


                    # Check if the new file is empty before writing
                    if os.path.getsize("updated_file.csv") == 0:

                        columns = []
                        # New header without the deleted columns
                        for column in reader.fieldnames:
                            if column not in deleteIdColumns:
                                columns.append(column)
            
                        # Write the updated content to the new file
                        writer = csv.DictWriter(newFile, fieldnames=columns)
                        writer.writeheader()
                        for row in reader:
                            for column in deleteIdColumns:
                                if column in row:
                                    del row[column]
                            writer.writerow(row)
                    
                    # If the new file already has data, do not write again
                    else: 
                        print("updated_file.csv already has data, skipping write operation.")

            # Handle error that occurs while reading the file
            except FileNotFoundError:
                print("something went wrong, cannot read the file")
                return self.removeIdColumns()

        
    # Function to register a new user
    def registerUser(self): 
            print("\nRegister New User")
            name = input("Enter your name: ").strip()

            # Check for empty name
            if not name:
                print("Name cannot be empty. Please try again.\n")
                return self.registerUser()
            
           
            email = input("Enter your email: ").strip().lower()

            # Check for empty email
            if not email:
                print("Email cannot be empty. Please try again.\n")
                return self.registerUser()

            # Validate email format
            if not self.validEmail(email):
                print("Invalid email format. Please try again.\n")
                return self.registerUser()
                  

            else:
                password = input("Enter your password: ")
                tempPassword = input("Confirm your password: ")

                # Check for empty password
                if not password:
                    print("Password cannot be empty. Please try again.\n")
                    return self.registerUser()

                else:
                    if password != tempPassword:
                                print("Passwords do not match. Please try again.\n")
                                return self.registerUser()
                    
                    elif any(user["email"] == email for user in self.usersList):
                        print("Email already exists. Please try again with a different email.\n")
                        return self.registerUser()

                    # If all validations pass, register the user
                    else:
                        self.save(name, email, password)
                        print("Registration successful! You can now log in.\n")

                        return self.mainMenu()

    # Save new user to the CSV file
    def save(self, name, email, password):
        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, password, "user"])
        # Reload users list after adding a new user
        self.usersList = []
        self.loadUsers()

    # Validate email format using a regular expression
    def validEmail(self, email):
        valid = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(valid, email) is not None

    # User login function
    def login(self):
        print("\nUser Login")
        email = input("Enter your email: ").strip().lower()
        # Validate email format
        if not self.validEmail(email):
            print("Invalid email format. Please try again.\n")
            return self.login()

        # Check for empty email
        elif not email:
            print("Email cannot be empty. Please try again.\n")
            return self.login()

        else:
            password = input("Enter your password: ")

            # Check for empty password
            if not password:
                print("Password cannot be empty. Please try again.\n")
                return self.login()
            else:
                # Authenticate user
                for user in self.usersList:
                    if user["email"] == email and user["password"] == password:
                        print(f"Login successful! Welcome, {user['name']}.\n")
                        if user["role"] == "admin":
                            self.admMenu()
                        else:
                            self.userMenu()
                        return
                print("Invalid email or password. Please try again.\n")
                return self.login()


    # User Menu
    def userMenu(self):
        while True:
            print("""
User Menu:
1. Purchase Ticket
2. Logout
3. Exit
            """)
            choice = input("Enter your choice: ")
            if choice == "1":
                print("Purchase Ticket")
            elif choice == "2":
                print("Logout")
                self.mainMenu()
            elif choice == "3":
                print("Exiting the system. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")
                return self.userMenu()


    # Admin Menu
    def admMenu(self):
        while True:
            print("""
Admin Menu:
1. Update Ticket Price
2. Purchase Chart
3. Logout
4. Exit
            """)
            choice = input("Enter your choice: ")
            if choice == "1":
                print("Update Ticket Price")
            elif choice == "2":
                print("Purchase Chart")
            elif choice == "3":
                print("Logout")
                self.mainMenu()
            elif choice == "4":
                print("Exiting the system. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")
                return self.admMenu()



    # Main Menu
    def mainMenu(self):        
        print("Welcome to the Bus Ticket Booking System")
        while True:
            print("""
Main Menu:
1. Register User
2. Login
3. Exit
            """)
            choice = input("Enter your choice: ")
            if choice == "1":
                self.registerUser()
            elif choice == "2":
                self.login() 
            elif choice == "3":
                print("Exiting the system. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")
                return self.mainMenu()
       

# Run the main program
if __name__ == "__main__":
    main().mainMenu()