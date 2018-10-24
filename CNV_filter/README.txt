READ ME for gene_filter.py
Eleanor Campbell


Filters a CNV list based on a gene list and by frequency. 
Writes three new CNV lists with only entries that have relevant genes, one has all relevant genes, one has only relevant genes with a frequency of less than .05 the final with less than .01.

To run gene_filter.py from the command line:
Make sure that the three needed files are in the directory:
    gene_filter_v2.py
    CNV_file: a tab delimited file with columns labeled 'GENES', 'DEL/DUP', 'POP DEL AF', and 'POP DUP AF'. Dosen't necessarily have to be a CNV file but must be tab delimited and must have a those headers in the first line. The genes listed in a line can be delimited by any combination of commas (,), semicolons(;) and dashes(-). Usually a tsv or txt
    Gene list: a text file with a list of genes, one gene per line. Ususally a txt.

Run this line but with the actual file names:
    python gene_filter_v2.py cnv_file.tsv gene_list.txt
    
Alternatively if you want to check against two gene lists at the same time (say the HPO list and the Medical Exome list) then just be sure to have both gene lists in the directory and call like this:
    python gene_filter_v2.py cnv_file.tsv gene_list_1.txt gene_list_2.txt