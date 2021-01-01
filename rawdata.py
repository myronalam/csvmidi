# Raw data parsing - returns tuple:
# [0] list of dict, data
# [1] list, column names

import csv

def parse(formInput):
    # Get rid of spaces
    formInput = formInput.strip()

    # f is the CSV formated data, can use functions from csv library
    f = formInput.splitlines()

    print(f)
    
    # (1) Get column names
    reader = csv.DictReader(f)
    columns = reader.fieldnames

    # (2) Created ordered dictionary from CSV
    data = []
    for row in reader:
        data.append(row)
    
    return data, columns