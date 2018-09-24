de_dup.py takes two txt files and returns a txt file that has been de duplicated

To run de_dup.py from the command line:
navagate to the directory with de_dup.py

run the command:

python de_dup.py medical_exome_gene_list_name.txt HPO_gene_list_name.txt

It will return a gene list named: HPO_gene_list_name_de_duped.txt

This is the same as the medical_exome_gene_list but with all entries removed that were also present in the HPO_gene_list. 