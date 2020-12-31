# Raw data parsing - returns dict formOutput
# formOutput = {'column': [value1, value2], 'column2': [value3, value4]}

def parse(formInput):
    # Get rid of leading and trailing spaces
    formInput = formInput.lstrip(" \r\n")
    formInput = formInput.rstrip(" \r\n")

    # hard coded, modify to accept inputs in the future
    delimiter = ","

    # Create list of rows from raw data, store in temp
    temp = formInput.split("\r")

    # Remove new line character from each row, separate data by delimiter
    temp2 = []
    for item in temp:
        temp2.append(item.strip("\n").split(delimiter))
    
    firstRow = temp2[0]
    print(f"firstRow = {firstRow}")
    numColumns = len(temp2[0])

    # Generate keys (column headers) for dictionary formOutput
    formOutput = {}
    for header in temp2[0]:
        formOutput[header] = []

    # Iterate through data to add to dict formOutput, skipping first row
    count = 0
    for row in range(1,len(temp2)):
        for item in temp2[row]:
            print(item)
            formOutput[firstRow[count % numColumns]].append(item)
            count += 1

    return formOutput