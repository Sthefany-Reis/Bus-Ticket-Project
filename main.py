# Bus Ticket booking System  

import csv  
import os

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
                open("updated_file.csv", "a", newline="") as newFile:
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
             
            else: 
                print("updated_file.csv already contains data") #checkpoint
             

            




                    

    # Handle any error that occurs while reading the file
    except:
        print("something went wrong, cannot read the files")
 
# Handle the error if the products file does not exist
except:
    print("file does not exist")

