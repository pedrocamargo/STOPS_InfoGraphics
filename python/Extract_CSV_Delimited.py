# Extract_CSV_Delimited.py

dir = '/Volumes/C/projects/SMART Plan Systemwide STOPS/AC_MDTEXIST#MDTNOB#MDTBLD_STOPSY2015Results'
txt_dir = "txt_extract"
csv_dir = "csv_dir"
test_file = "Table     2.04.txt"
test_csv_file = "Table     2.04.csv"

# Second Method to extract table contents based on delimiter
table_rows = []
found_header = 0

import os, csv, pandas as pd

def write_table_to_csv(data, csv_file_name):
    with open(csv_file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row) 


dir_file = os.path.join(dir, txt_dir, test_file)
csv_file_name = os.path.join(dir, csv_dir, test_csv_file)


# Extract table text contents to csv
with open (dir_file, 'rt') as in_file:
    # get rows
    for line in in_file:
        
        # check header separator (start of table)
        header_separator = "======"
        row_elements = []
        
        # get table header (fieldnames)
        if line.find(header_separator, len(header_separator)) != -1 and found_header == 0:
            fieldNames = prev_line.split(" ")
            if len(fieldNames) > 1: # at least 3 columns
                found_header = 1
                for e in fieldNames:
                    e_value = e.strip()
                    if len(e_value) > 0 and e_value != ":" :
                        row_elements.append(e_value)
                table_rows.append(row_elements)

        # get table contents            
        if line.find(header_separator, len(header_separator)) == -1 and found_header == 1:
            elements = line.split(" ")
            if len(elements) > 1: # at least 3 columns
                for e in elements:
                    e_value = e.strip()
                    if len(e_value) > 0 and e_value != ":" :
                        row_elements.append(e_value)  
                table_rows.append(row_elements)

        # store previous line (to get header)
        prev_line = line

    write_table_to_csv(table_rows, csv_file_name)
    print("Finished Converting " + test_file + " to " + test_csv_file)

    # fix header column issue with pandas (read csv file and use index to get colnames and replace rownames and save to same csv file)
    # df = pd.read_csv(csv_file_name, skiprows = 1,
    # rownames = list(df.index)
    # colnames = list(df)
    # # df.columns = df.index
    # # col1 = df['1-South_:']
    # print(colnames)
    # print(rownames)
    # print(df.shape)
    # # print(col1)


