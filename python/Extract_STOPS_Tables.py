# Tilte: Extract_STOPS_Tables
# Purpose: Extracts specified tables from the STOPS report
# Description: Identifies specified tables and writes out each table a text file
# 
# Author: Amar Sarvepalli 
# Email: sarvepalli@pbworld.com
# Data: April 27, 2017

###############################################################################
# User's Settings
# dir = '/Volumes/C/projects/SMART Plan Systemwide STOPS/AC_MDTEXIST#MDTNOB#MDTBLD_STOPSY2015Results'
dir = "/Volumes/C/projects/SEFL_STOPS/test_run_review"
txt_dir = "txt_extract"
csv_dir = "csv_dir"

stops_report = "AC_MDTEXIST#MDTNOB#MDTBLD_STOPSY2015Results.prn"

tables = [1.01, 1.02, 
          2.01, 2.02, 2.03, 2.04, 2.05, 
          3.01, 3.02, 3.03, 3.04, 3.05, 3.06, 3.07,
          4.01, 4.02, 4.03, 4.04,
          5.01, 5.02, 5.03, 5.04,
          6.01, 6.02, 6.03, 6.04,
          7.01, 7.02, 7.03, 7.04,
          8.01,
          9.01, 
          10.01, 10.02, 10.03, 10.04,
          11.01, 11.02, 11.03, 11.04,
          12.01,
          13.01, 13.02, 13.03, 13.04, 13.05, 13.05, 13.06, 13.07, 13.08, 13.09]

fixed_tables = [ 9.01, 
                10.01, 10.02, 10.03, 10.04,
                11.01, 11.02, 11.03, 11.04,
                12.01]

# TODO: Not sure if we want to two extraction process
# Field widths for fixed tables
table_info = {} 
table_info[(10.01)] = [9, 41,51, 61, 71, 81, 91, 101, 111, 121, 131, 141, 151, 161]
table_info[(1.02)] = [8, 17, 27, 37, 47, 57, 78, 88, 101, 106, 116, 127, 136, 145, 154, 163, 172]
table_info[(9.01)] = [22, 32, 42, 52, 62, 72, 82, 92, 102, 112, 122, 132, 142, 152, 162, 171]

###############################################################################
# Program starts here
import os, csv, Clean_Extracted_Tables as cet

# table_end = '-------------------------------------------------------------------------------------------------------------------------------------'

# 1. Create output directory
cet.create_directory(dir, txt_dir)
cet.create_directory(dir, csv_dir)

# 2. Extract tables from report
report_file = os.path.join(dir, stops_report)
output_dir = os.path.join(dir, txt_dir)
cet.extractTables(report_file, tables, output_dir)


# 3. Convert selected tables to csv file
tables_files = cet.getFiles(os.path.join(dir, txt_dir))

# selected tables 
# tables = [2.04, 10.01, 9.01]
# tables = [2.04]

# process tables text files
for file in tables_files:
    for t in range(len(tables)):
        tbl_no = tables[t]
        # col_widths = table_info[tbl_no]

        if tbl_no in table_info.keys():
            col_widths = table_info[tbl_no]
        else: 
            col_widths = None

        # table name contains table number
        if file.find(str(tbl_no),9,14) != -1: 
            txt_file = os.path.join(dir, txt_dir, file)
            csv_file = os.path.join(dir, csv_dir, file)
            # table_rows = cet.extractTableContents(txt_file, col_widths)

            if col_widths != None:
                table_rows = cet.extractTableContentsFixed(txt_file, col_widths)
            else:    
                table_rows = cet.extractTableContentsDelimited(txt_file)
            
            # Output csv file name
            csv_file_name = cet.get_csv_filename(csv_file)
            print(csv_file_name)
            
            # write table to csv
            cet.write_table_to_csv(table_rows, csv_file_name)





