# Bus Ticket booking System  

import csv  
from nt import system
import os


# Function to register a new user
def registerUser():
    while True:
        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)

            # If file is empty, write the header
            if os.path.getsize("users.csv") == 0:
                writer.writerow(["name", "email", "password"])

            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            tempPassword = input("Confirm your password: ")

            if password != tempPassword:
                print("Passwords do not match. Please try again.")
                continue

            # If file is not empty, just append the user data
            else:
                writer.writerow([name, email, password])
                print("User registered successfully!")

            choice = input("Do you want to register another user? (yes/no): ").strip().lower()
            
            # Handle user choice
            if choice in ("yes", "y"):
                continue
            elif choice in ("no", "n"):
                print("Registration process completed.")
                break

            else:
                print("Invalid choice.")
                choice = input("Do you want to register another user? (yes/no): ").strip().lower()
                


registerUser() #checking user registration functionality




deleteIdColumns = ["category_id", "topup_passenger_class_id", "topup_id"]

# Check if the file exists
try:
    file = open("mobile_products.csv")
    file.close()

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
             
               

    # Handle any error that occurs while reading the file
    except:
        print("something went wrong, cannot read the files")
 
# Handle the error if the products file does not exist
except:
    print("file does not exist")

