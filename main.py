# Bus Ticket booking System  

import csv  
import os

# Check if the file exists
try:
    file = open("mobile_products.csv")
    file.close()

    # Read the file content
    try:

        # Create an empty file if updated_file.csv does not exist
        if not os.path.exists("updated_file.csv"):
            print("Creating updated_file.csv as it does not exist") #checkpoint
            open("updated_file.csv", "a").close()

        # Open the CSV file for reading
        with open("mobile_products.csv", "r") as file:
            reader = csv.DictReader(file)

            # Open the updated file for writing
            with open("updated_file.csv", "w") as newFile:

                    header =["category_title",	"category_description",	"topup_title",	"topup_description",	\
                            "topup_price_in_pence",	"topup_entitlement_type",	"topup_entitlement_unit",	"topup_entitlement_value",	\
                            "topup_entitlement_quantity",	"topup_entitlement_start_date",	"topup_entitlement_end_date",	"topup_passenger_class_id",	"topup_passenger_class_name",	"topup_passenger_class_quantity"]
                    writer = csv.DictWriter(newFile, fieldnames=header, delimiter="\t")
                    writer.writeheader()
                    print("Writing to updated_file.csv") #checkpoint

    # Handle any error that occurs while reading the file
    except:
        print("something went wrong, cannot read the files")
 
# Handle the error if the products file does not exist
except:
    print("file does not exist")
