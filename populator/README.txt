Populator is currently built to run via the command line.

Step 1: Save your excel sheet as a tab seperated file, ususally a txt or tsv, either extension will work as long as it is formatted correctly.

Step 2: Make sure that you have all needed documents in your directory: 
    the python file itself populate_tsv.py
    the TSV file you want to populate 
    the OMIM file genemap2.txt
    the orphanet file currently known as orphanet_data_1.txt (Updated versions available at http://www.orphadata.org/cgi-bin/index.php/, under the name Epidemiological data)
    the orphanet file currently known as orphanet_data_symbol_to_disorder.txt (updated versions available at http://www.orphadata.org/cgi-bin/index.php/ under the name Disorders with thier associated genes)
    
Step 3: Navagate to the directory in the command line, and run this code:
    python populate_tsv.py tsv_file_name.tsv

Outputs: A number of tsv files will be created, if they have the word Temp at the end of thier file name it is safe to delete. 
The file you are looking for ends in "_populated.tsv"


Troubleshooting:

If the command line says python is not a valid command, go online and download python for your computer. 

If the error thrown says a file does not exist then check for all the files in Step 2. 
If you have all the files but some are named differently then either rename them to fit the names given here or edit the names to match in the populate_tsv.py file around line 227 under the heading #data files

If the script is running but not filling in the columns properly then check to make sure the indicies are correct in populate_tsv.py around line 207 under the heading #Indicies. Remember that python starts its numbering system at 0, so index 1 means the second column. If you can tell which column is filled in but not correctly check that column's index before checking blank column's indecies.

The only index in the input file that matters is the index of the gene symbol, which currently is assumed to be in the SECOND column (B).