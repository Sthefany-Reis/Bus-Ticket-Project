# Bus Ticket booking System  

import csv  
import os
import re


# Function to remove specific columns from the CSV file
def removeIdColumns():
    deleteIdColumns = ["category_id", "topup_passenger_class_id", "topup_id"]

    while True:
        # Handle the error if the products file does not exist
        if not os.path.exists("mobile_products.csv"):
            print("mobile_products.csv file does not exist")
            raise FileNotFoundError

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
            except:
                print("something went wrong, cannot read the file")
                break

        # Exit the loop after one complete operation
        break

# Call the function to remove ID columns from the CSV file
removeIdColumns()




# Admin login details (FOR NOW)
admLogin = {"name": "admin", "email": "admin@email.com", "password": "adm1", "role": "admin"}




# Customer/User Menu
class user():
    def __init__(self):
        pass

    # If file no file, write the header amd admin login details
    try:
        with open("users.csv", "r") as file:
            pass
    except FileNotFoundError:
        with open("users.csv", "w", newline="") as file:
            if os.path.getsize("users.csv") == 0:
                writer = csv.writer(file)
                writer.writerow(["name", "email", "password", "role"])
                writer.writerow([admLogin["name"], admLogin["email"], admLogin["password"], admLogin["role"]])

    # Function to register a new user
    def registerUser(self): 

        # Read existing users from the CSV file
        users = []
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)

            name = input("Enter your name: ").strip().lower()
            email = input("Enter your email: ").strip().lower()
            # Validate email format
            if not self.validEmail(email):
                print("Invalid email format. Please try again.")
                return
                   
            # Check if email already exists
            if any(user["email"] == email for user in users):
                print("This email is already registered. Please try logging in.")
                return

            password = input("Enter your password: ")
            tempPassword = input("Confirm your password: ")

            if password != tempPassword:
                print("Passwords do not match. Please try again.")
                return

            # If file is not empty, just append the user data
            else:
                with open("users.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([name, email, password, "user"])
                    print("User registered successfully!")


                    

                    



    # Validate email format using a regular expression
    def validEmail(self, email):
        valid = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(valid, email) is not None


    # User Menu
    def menu(self):
        while True:
            print("""
User Menu: 
1. Register User
2. Login
3. Exit
            """)



# Main function
class main:
    def __init__(self, user):  
        self.user = user
        print("Welcome to the Bus Ticket Booking System")

        # Main loop

        while True:
            print("""
Main Menu:
1. Register User
2. Login
3. Exit
            """)
            choice = input("Enter your choice: ")
            if choice == "1":
                self.user.registerUser()
                pass
            elif choice == "2":
                #login() 
                pass
            elif choice == "3":
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main(user())
