# Title: Clean_Extracted_Tables

# dir = '/Volumes/C/projects/SMART Plan Systemwide STOPS/AC_MDTEXIST#MDTNOB#MDTBLD_STOPSY2015Results'
# txt_dir = "txt_extract"
# csv_dir = "csv_dir"

import os, csv

###############################################################################
# Define functions
###############################################################################

# Function extract tables (*.txt) from report (*.prn)
def extractTables(report_file, tables, output_dir):
    # initialize
    count = 0
    found_table_no = 0
    is_outfile_open = 'False'
    table_end = '-------------------------------------------------------------------------------------------------------------------------------------'

    with open(report_file, "rt") as in_file:
        for line in in_file:

            if found_table_no < len(tables):
                table_number = 'Table' + str(tables[found_table_no]).rjust(9,)
                
            #  At Table start
            if (line.find(table_number, 0, 14) != -1):
                count = 1
                found_table_no += 1
                output_table = table_number + '.txt' #'Table' + str(tables[found_table_no]) +'.txt'
                is_outfile_open = 'True'
                out_file = open(os.path.join(output_dir, output_table),'w')
            
            # At Table end
            if line.find(table_end, 0, 134) != -1:
                count = 0
                if is_outfile_open == 'True':
                    out_file.close()
                is_outfile_open = 'False'

            # Extract Table contents
            if count > 0:
                #table_raw.append(line)
                out_file.write(line)



# Function: Get list of text files
def getFiles(dir):
   table_files = []
   for file in os.listdir(dir):
        if file.startswith("Table") & file.endswith(".txt"):
            table_files.append(file) 
   return table_files

# Function to extract data
def extractTableContents(dir_file, col_widths):
    if col_widths != None:
        extractTableContentsFixed(dir_file, col_widths)    
    else:
        extractTableContentsDelimited(dir_file)


# Function to extract fixed column table data
def extractTableContentsFixed(dir_file, col_widths):
    table_rows = []

    with open (dir_file, 'rt') as in_file:

        # get rows
        for line in in_file:
            
            # check last column data to identify table
            last_col = line[ col_widths[len(col_widths) - 2] + 1 : col_widths[len(col_widths) - 1] ]  
            data_col = last_col.lstrip()

            # identifier to remove header separator
            if (len(data_col) > 0) and  ('=' not in data_col) :  
                
                # get row elements
                row_elements = []
                for e in range(len(col_widths)):
                    if e == 0:
                        row_elements.append(line[0: col_widths[e] -1])
                    else:
                        row_elements.append(line[col_widths[e - 1] : col_widths[e] - 1])

                # append row elements to table         
                table_rows.append(row_elements)
                # print(table_rows)
    return table_rows


# Function to extract space delimited table data
def extractTableContentsDelimited(dir_file):
    table_rows = []
    found_header = 0
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
                        if len(e_value) > 0 and e_value != ":":
                            if e_value == "-":
                                e_value = 0
                            row_elements.append(e_value)  
                    table_rows.append(row_elements)

            # store previous line (to get header)
            prev_line = line

    return table_rows


# Funtion: Generate csv filename from raw table name
def get_csv_filename(file):
    file_no_ext = file.split(".txt")[0] 
    csv_file_name = os.path.join(dir, file_no_ext + '.csv')
    return csv_file_name


# Function: write table to csv
def write_table_to_csv(data, csv_file_name):
    with open(csv_file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row) 

# Function to create directory
def create_directory(dir, folder):
    directory = os.path.join(dir, folder)
    if not os.path.exists(directory):
        os.makedirs(directory)           

# Function to get all files
def getAllFiles(dir):
   table_files = []
   for file in os.listdir(dir):
        table_files.append(file) 
   return table_files


            
