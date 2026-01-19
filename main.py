# Bus Ticket booking System  

import csv  
import os
import re
from datetime import datetime


# Admin login details (FOR NOW)
admLogin = {"name": "admin", "email": "admin@email.com", "password": "adm1", "role": "admin"}

    
# Category class
class category():
    def __init__(self, title, description, code):
        self.title = title
        self.description = description
        self.code = code

# TopUp class
class topUp:
    def __init__(self, title, description, entType, entUnit, entValue, entQuantity, entStart, entEnd, className, classQuantity,  price, category, code):
        self.title = title
        self.description = description
        self.entType = entType
        self.entUnit = entUnit
        self.entValue = entValue
        self.entQuantity = entQuantity
        self.entStart = entStart
        self.entEnd = entEnd
        self.className = className
        self.classQuantity = classQuantity
        self.price = int(price)
        self.category = category
        self.code = code


# Main class
class main:
    def __init__(self): 
        self.purchases = {}
        self.tempPurchases = {}
        self.usersList = []
        self.categories = []
        self.topUps = []

        self.removeIdColumns()
        self.userFile()
        self.loadUsers()
        self.loadCategories()
        self.loadTopUps()
        self.purchaseFile()
        self.loadPurchases()

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
                return

    # Create users.csv file if it does not exist
    def userFile(self):
        if not os.path.exists("users.csv"):
            with open("users.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["name", "email", "password", "role"])
                # Add admin login details to the file
                writer.writerow([admLogin["name"], admLogin["email"], admLogin["password"], admLogin["role"]])

    # Create purchase.csv file if it does not exist
    def purchaseFile(self):
        if not os.path.exists("purchase.csv"):
            with open("purchase.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "quantity"])

   # Load users from the CSV file
    def loadUsers(self):
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.usersList.append({"name": row["name"], "email": row["email"], "password": row["password"], "role": row["role"]})
 
    # Load categories from the CSV file
    def loadCategories(self):
        # Avoid duplicate categories
        seen = set()
        code = 0
        with open("updated_file.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["category_title"] not in seen:
                    self.categories.append(category(
                        row["category_title"],
                        row["category_description"],
                        code))
                    seen.add(row["category_title"])
                    code += 1


    # Load top-ups from the CSV file
    def loadTopUps(self):
        code = 0
        with open("updated_file.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.topUps.append(topUp(
                    row["topup_title"],
                    row["topup_description"],
                    row["topup_entitlement_type"],
                    row["topup_entitlement_unit"],
                    row["topup_entitlement_value"],
                    row["topup_entitlement_quantity"],
                    row["topup_entitlement_start_date"],
                    row["topup_entitlement_end_date"],
                    row["topup_passenger_class_name"],
                    row["topup_passenger_class_quantity"],
                    row["topup_price_in_pence"],
                    row["category_title"],
                    code))
                code += 1

    # Load purchases from the CSV file
    def loadPurchases(self):
        with open("purchase.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.purchases[row["title"]] = int(row["quantity"])


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

    # Function to register a new user
    def registerUser(self): 
            print("\nRegister New User")
            name = input("Enter your name: ").strip()
            # Check for empty name
            if not name:
                print("Name cannot be empty. Please try again.\n")
                return self.registerUser()
            else:
                email = input("Enter your email: ").strip().lower()
                # Check for empty email
                if not email:
                    print("Email cannot be empty. Please try again.\n")
                    return self.registerUser()
                # Validate email format
                elif not self.validEmail(email):
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
            elif password:
                # Authenticate user
                for user in self.usersList:
                    if user["email"] == email and user["password"] == password:
                        print(f"\nLogin successful! Welcome, {user['name']}.")
                        if user["role"] == "admin":
                            return self.admMenu()  
                        else:
                            return self.userMenu()
                else:
                    print("Invalid email or password. Please try again.\n")
                    return self.login()

    # Category and Top-Up Selection
    def catChoice(self): 
        while True:
            print("\nCategories:")
            for cat in self.categories:
                print(f"{cat.code}. {cat.title}")
            try:
                choice = input("\nSelect a Category by entering its code or 'b' to go back: ")
                # Validate category choice
                if choice.isdigit():
                    choice = int(choice)
                    if choice < 0 or choice >= len(self.categories):
                        print("Invalid choice. Please try again.")
                        return self.catChoice()
                    else:
                        selectedCat = next(
                            cat                # take this category
                            for cat in self.categories   # from the list of categories
                            if cat.code == choice )       # only if the code matches the user's choice
                        print(f"\nYou selected category: {selectedCat.title}")
                        print(f"Description: {selectedCat.description}\n")
                        print("Available Top-Ups:")
                        for topup in self.topUps:
                            if topup.category == selectedCat.title:
                                print(f"{topup.code}. {topup.title} - Price: {topup.price/100:.2f} pounds")
                        choice = input("\nSelect a Top-Up by entering its code or 'b' to go back: ")
                        # Validate top-up choice
                        if not choice.isdigit():
                            if choice in ('b', 'B'):
                                print("Going back to Categories.\n")
                                return self.catChoice()
                            else:
                                print("Invalid choice. Please try again.")
                                return self.catChoice()
                        else:
                            choice = int(choice)
                        # check if the selected top-up belongs to the selected category
                        if not any(topup.code == choice and topup.category == selectedCat.title for topup in self.topUps): 
                            print("Invalid choice. Please try again.")
                            return self.catChoice()
                        elif choice < 0 or choice >= len(self.topUps):
                            print("Invalid choice. Please try again.")
                            return self.catChoice()
                        else:
                            selectedTop = next(
                                topup                  # take this top-up
                                for topup in self.topUps    # from the list of top-ups
                                if topup.code == choice     # only if the code matches the user's choice
                                and topup.category == selectedCat.title)    # and belongs to the selected category
                            print(f"You selected Top-Up: {selectedTop.title}"
                                  f"Description: {selectedTop.description}"
                                  f"Price: {selectedTop.price/100:.2f} pounds"
                                  f"Passenger Class: {selectedTop.className}\n")
                            confirm = input("Do you want to proceed with the purchase? \nyes/y to confirm or any other key to cancel: ").strip().lower()
                            if confirm in ("yes", "y"):
                                print("Purchase successful!\n")
                                # Existing purchase, increment quantity
                                if selectedTop.title in self.purchases:
                                    self.purchases[selectedTop.title] += 1
                                    self.tempPurchases[selectedTop.title] = self.tempPurchases.get(selectedTop.title, 0) + 1
                                # New purchase, set quantity to 1
                                else:
                                    self.purchases[selectedTop.title] = 1
                                    self.tempPurchases[selectedTop.title] = 1
                                # Save updated purchases to the CSV file
                                with open("purchase.csv", "w", newline="") as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["title", "quantity"])
                                    for title, quantity in self.purchases.items():
                                        writer.writerow([title, quantity])
                                return self.displayPurchase(selectedTop)
                            else:
                                print("Purchase cancelled.\n")
                                return self.catChoice()
                # Go back to User Menu
                elif choice in ('b', 'B'):
                    print("Going back to User Menu.\n")
                    return self.userMenu()
                # Invalid input
                else:
                    print("Invalid choice. Please try again.")
                    return self.catChoice()
            # Handle non-integer input
            except ValueError:
                print("Invalid input. Please enter a valid code.")
                return self.catChoice()


    def displayPurchase(self, selectedTop):
        # Only parse dates for fixed_date entitlements and when values exist
        startDate = endDate = None
        # Parse dates if entitlement type is fixed_date
        if selectedTop.entType and selectedTop.entType.lower() == "fixed_date":
            if selectedTop.entStart and selectedTop.entEnd:
                try:
                    # Convert ISO 8601 string to datetime object
                    startDate = datetime.fromisoformat(selectedTop.entStart)
                    endDate = datetime.fromisoformat(selectedTop.entEnd)
                except ValueError:
                    print("Top-Up has invalid date format; dates unavailable.")
            else:
                print("Top-Up has no start/end dates; dates unavailable.")
        print(
            f"Title: {selectedTop.title}\n"
            f"Description: {selectedTop.description}\n"
            f"Price: {selectedTop.price / 100:.2f} pounds\n"
            f"Passenger Class: {selectedTop.className}")
        # Display entitlement details based on type
        if selectedTop.entType and selectedTop.entType.lower() == "fixed_date":
            if startDate and endDate:
                print(f"Valid: From {startDate.strftime('%d %b %Y %H:%M')} to {endDate.strftime('%d %b %Y %H:%M')}\n")
            else:
                print("Valid: Date information not available.\n")
        elif selectedTop.entType and selectedTop.entType.lower() == "flexible":
            print(f"Quantity: {selectedTop.entQuantity} passes, each valid for {selectedTop.entValue} {selectedTop.entUnit} from the first use.\n")
        else:
            print("Unknown entitlement type.\n")
        # Ask if the user wants to purchase another Top-Up  
        continuePurchase = input("Do you want to purchase another Top-Up? (yes/no): ").strip().lower()
        if continuePurchase in ("yes", "y"):
            return self.catChoice()
        elif continuePurchase in ("no", "n"):
            # Display purchase summary
            print("\nPurchase Summary:") 
            total = 0
            # Show only the Top-Ups purchased in this session
            for title, quantity in self.tempPurchases.items():
                print(f"{title}: {quantity}")
                total += quantity
            self.tempPurchases = {}  # Clear temporary purchases after displaying
            print(f"\nTotal Top-Ups Purchased: {total}\n")
            print("Thank you for your purchase! Returning to User Menu.\n")
            return self.userMenu()
        else:
            print("Invalid choice. Please try again.")
            return self.displayPurchase(selectedTop)



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
                print("\nPurchase Ticket")
                self.catChoice()
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
1. View TopUps Available
2. Update Ticket Price
3. Purchase Chart
4. Logout
5. Exit
            """)
            choice = input("Enter your choice: ")
            if choice == "1":
                print("\nTop-Ups Available:\n")
                # Display all top-ups with details
                for topup in self.topUps:
                    print(f"{topup.code}. {topup.title} - Class: {topup.className} - Price: {topup.price/100:.2f} pounds / {topup.price} pence")
                print("Press Enter to return to Admin Menu.")
                input()
            elif choice == "2":
                print("Update TopUp Price:")
                # Display all top-ups with current prices
                for topup in self.topUps:
                    print(f"{topup.code}. {topup.title} - Class: {topup.className} - Current Price: {topup.price/100:.2f} pounds / {topup.price} pence")
                choice = input("\nSelect a Top-Up to update by entering its code or 'b' to go back: ")
                # Validate top-up choice
                if not choice.isdigit():
                    if choice in ('b', 'B'):
                        print("Going back to Admin Menu.\n")
                        return self.admMenu()
                    else:
                        print("Invalid choice. Please try again.")
                        return self.admMenu()
                else:
                    choice = int(choice)
                    # check if the selected top-up code is valid
                    if choice < 0 or choice >= len(self.topUps):
                        print("Invalid choice. Please try again.")
                        return self.admMenu()
                    else:
                        # Get the selected top-up
                        selectedTop = next(
                            topup                  # take this top-up
                            for topup in self.topUps    # from the list of top-ups
                            if topup.code == choice)     # only if the code matches the user's choice
                        print(f"\nYou selected: \nTop-Up: {selectedTop.title}"
                              f"Class: {selectedTop.className}"
                              f"Current Price: {selectedTop.price/100:.2f} pounds / {selectedTop.price} pence")
                        newPrice = input("Enter the new price in pence: ")
                        if not newPrice.isdigit() or int(newPrice) < 0:
                            print("Invalid price. Please enter a valid positive integer.")
                            return self.admMenu()
                        else:
                            selectedTop.price = int(newPrice)
                            # Update the price in the CSV file
                            with open("updated_file.csv", "r") as file:
                                reader = csv.DictReader(file)
                                rows = list(reader)
                                with open("updated_file.csv", "w", newline="") as file:
                                    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                                    writer.writeheader()
                                    # Update the specific top-up price
                                    for row in rows:
                                        if row["topup_title"] == selectedTop.title and row["topup_passenger_class_name"] == selectedTop.className:
                                            row["topup_price_in_pence"] = str(selectedTop.price)
                                        writer.writerow(row)
                            print(f"\nPrice of {selectedTop.title} for {selectedTop.className} was updated successfully to {selectedTop.price/100:.2f} pounds / {selectedTop.price} pence.\n")
                            print("Press Enter to return to Admin Menu.")
                            input()
                            return self.admMenu()

            elif choice == "3":
                print("Purchase Chart")
            elif choice == "4":
                print("Logout")
                self.mainMenu()
            elif choice == "5":
                print("Exiting the system. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")
                return self.admMenu()



    # Main Menu
    def mainMenu(self):        
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
    print("Welcome to the Bus Ticket Booking System")
    main().mainMenu()