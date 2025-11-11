# Bus Ticket booking System  

import csv  
import os

# Check if the file exists
try:
    file = open("mobile_products.csv")

    # Read the file content
    try:
        print(file.read())
        file.close()

    # Handle any error that occurs while reading the file
    except:
        print("something went wrong, cannot read the file")
 
# Handle the error if the file does not exist
except:
    print("file does not exist")



