"""
    Populates a tsv file with Orphanet and OMIM data
    Run with one argument: name of the tsv file to be populated
    Eleanor Campbell
"""

#import statements
import sys

def build_dictionary(data_file_name, search_index, info_index, filter_on = False, filter_index = 32, filter_by = 'OMIM'):
    """Builds a dictionary of search term and info entries.
    Returns a dictionary.
    Parameters: File - tab delimited, index of the search term, index of the information, 
    Optional: turn on the filter to filter by the value in another term. filter on (true/false), index of the term to filter by, term needed to pass the filter.
    """
    #open the file with the needed data
    data_file = open(data_file_name, 'r')
    
    #Start the data dictionary
    data_dictionary = {}
    
    #populate the dictionary
    #loop over each entry
    for line in data_file:
        #split the entry into an array where each spot is one peice of information from that entry
        data_entry = line.split('\t')
        #check to be sure the entry has all the needed information
        if len(data_entry) > max(search_index, info_index):
            #extract the needed information from the array and assign to variables
            search = data_entry[search_index].strip(' ')
            info = data_entry[info_index]
            #.replace(',',';')
            #check if using the filter and the entry is long enough to use the filter
            if filter_on and len(data_entry) > filter_index:
                #get the info from the entry at the filter index
                filter_info = data_entry[filter_index].strip(' ')
                #if the filter does not pass then remove the info from the dictionary
                if filter_info != filter_by:
                    info = ''
            #check if the search term is already in the dictionary
            if search in data_dictionary:
                #if the search is in the dictionary then append the new value to the list and the info is not already in the dictionary then add it to the list
                if info not in data_dictionary[search] and info != '':
                    data_dictionary[search].append(info)
                    #check if the empty info is in the dictionary and remove it
                    if '' in data_dictionary[search]:
                        data_dictionary[search].remove('')
            #if the search term is not in the dictionary add it with its info
            else:
                    data_dictionary[search] = [info]
        #if the entry is not long enough to have both the search term and the info term then print a message to the command line so the problem entry can be examined 
        elif data_entry[0].startswith('#'):
            pass
        else:
            print("Problem with entry:")
            print(data_entry)
    #remove the empty entry from the dictionary        
    if '' in data_dictionary:
        del data_dictionary['']
    #close the file
    data_file.close()
    
    return data_dictionary

def build_tsv_array(tsv_file_name):
    """Takes the tsv file and turns it into an array"""
    #open the tsv file
    tsv_file = open(tsv_file_name, 'r')
    
    #start the array 
    tsv_array =  []
    
    #populate the array
    #loop over each line
    for line in tsv_file:
        #turn the line into an array by splitting the lines along the tabs
        array_line = line.split('\t')
        #add the line array to the tsv array
        tsv_array.append(array_line)
        
    #close the file
    tsv_file.close()
    
    return tsv_array

def add_info(search_array, info_dictionary, search_index):
    """adds information from the data dictionary to the array made from the tsv
        Parameters: two tiered array made from a tsv, dictionary with string keys and list values, index of the term to search on in the array/tsv
    """
    #loop over each entry in the array from the tsv file/ array
    #initiate count
    count = 0
    while count < len(search_array):
        #find the next entry
        entry = search_array[count]
        #check to make sure the entry is long enough to include the seach term
        if len(entry) > search_index:
            #identify the searching item in question
            search = entry[search_index].strip(' ')
        else:
            #if the entry is not long enough then give a dumy search term
            search = "None"
        #check that the location is in the dictionary
        if search in info_dictionary:
            #retrieve the desired information from the dictionary
            info = info_dictionary[search]
            #loop over each of the entries in info, popping them out after each one
            while len(info) > 1:
                #loop through the info array and add new line to the array
                #find the index of the current entry and add one to get just below
                index = count + 1
                #form new a line just below the current entry with the current peice of info
                search_array.insert(index, [info.pop(0), '\n'])
                #advance the count of the search array so that the new line is skipped
                count = count + 1
            #with only one entry left add it to the entry in-line    
            entry.insert(0, info[0])
        #if the entry is deemed not a real entry then add a new empty column to the array to keep things orderly
        else:
            entry.insert(0, '')
        #advance the count to the next entry line
        count = count + 1
    
def write_tsv_from_array(two_tier_array, file_name):
    """creates a tsv from a two tiered array
        Parameters: tww tiered array, name for new tsv file
    """
    #create a new file
    new_tsv = open(file_name, 'w')
    
    #loop over each line in the array
    for line in two_tier_array:
        #loop over each entry in the line
        for entry in line:
            #for each entry write it to the new file and add a comma at the end
            if line.index(entry) < len(line)-1:
                new_tsv.write(entry + '\t')
            #for the final entry don't add a comma to the end.
            else:
                new_tsv.write(entry)
        
    #close the file
    new_tsv.close()
    
    return file_name

def add_data_from(array_name, data_file_name, data_search_index, tsv_search_index, data_to_add_index, filter_on = False, filter_index = 32, filter_by = 'OMIM'):
    """Returns a tsv like the given tsv but with new data from a given data file
        parameters: tsv file name that needs data added
            tab delimited file name with the desired information
            index of the search term in the data file
            index of the search term in the tsv
            index of the data in data file
            Optional: if the data dictionary needs to be filtered then:
            filter on (true/false)
            index of the filter term in the data file
            term needed to pass the filter
    """
    #build the dictionary
    data_dict = build_dictionary(data_file_name, data_search_index, data_to_add_index, filter_on, filter_index, filter_by)
    #build the array
    tsv_array = array_name
    #add the infomation from the dictionary to the array
    add_info(tsv_array, data_dict, tsv_search_index)
    
    #return the new tsv file name
    return tsv_array
    
def clean(tsv_file_name, out_put_file_name):
    """takes a tsv file created by the populate function and returns a tsv file that has column headers and does not have extra OMIM numbers"""
    #build the tsv array
    tsv_array = build_tsv_array(tsv_file_name)
    #add the headers 
    tsv_array[0][0] = 'Prevelance: 2016'
    tsv_array[0][1] = 'Disorder: OMIM'
    tsv_array[0][2] = 'OMIM Number'
    tsv_array[0][3] = 'Disorder: Orphanet'
    tsv_array[0][4] = 'Orphanum'
    #initiate a count 
    count = 0
    #loop over entries in the array with the count, end when the count reaches the end of the array
    while count < len(tsv_array):
        #get the entry based on the count
        entry = tsv_array[count]
        #check to make sure the OMIM number is the only information in the entry
        #check if the entry is short enough that it does not have any information after the OMIM number
        #then check to make sure everything befor the OMIM number is blank 
        if len(entry) == 4 and entry[0] == '' and entry[1] == '' and entry[3] == '\n':
            #if the OMIM number is the only info in the entry then remove that entry from the array
            #do not move the count forward becase the the next entry is now at that count
            tsv_array.remove(entry)
        #if the entry is empty then remove it    
        elif len(entry) == 1 and entry[0] == '\n':
            tsv_array.remove(entry)
        #remove alone orphanums the same way as the OMIM    
        elif len(entry) == 5 and entry[0] == '' and entry[1] == '' and entry[2] == '' and entry[3] == '':
            tsv_array.remove(entry)
        else:
            #if the entry has other information besides the OMIM number then move the count forward to the next entry
            count += 1
    #turn the array back into a tsv named the input name        
    new_tsv = write_tsv_from_array(tsv_array, out_put_file_name)
    #return the new tsv
    return new_tsv
    
def populate(tsv_file_name):
    """Takes a tsv file and populates it from OMIM's genemap2.txt and orphanet 
        adds: orphanet number based on the gene symbol
        adds: disease, OMIM number and prevelace based on orphanet number
        adds: OMIM inheritance based on OMIM number
        removes entries with only OMIM numbers to clean up the tsv
    """
    #CHECK THESE NUMBERS AND DATA FILES FIRST IN CASE OF NOT WORKING
    
    #Indecies
    
    #orphanet
    #gene to disease database
    gene_orphanet = 26
    orphanum = 5
    omim_number_orphanet = 33
    disease_orphanet = 6
    omim_validation_orphanet = 32
    #prevelance database
    prevelance_orphanet = 27
    validation_orphanet = 36
    
    #OMIM
    omim_number_omim = 5
    inheritance_omim = 12
    
    #tsv
    gene_tsv = 1
    
    #data files
    #Orphanet cross referencer. Gene to disorder file 
    Orphadata_1 = 'orphanet_data_symbol_to_disorder.txt'
    #Orphanet prevelance. 
    Orphadata_2 = 'orphanet_data_1.txt'
    #OMIM data. genemap2.txt
    OMIM_data = 'genemap2.txt'
    
    #get the Orphanet number from the gene symbol using the orphanet gene to disease reference
    array_1 = build_tsv_array(tsv_file_name)
    array_2 = add_data_from(array_1, Orphadata_1, gene_orphanet, gene_tsv, orphanum)
    #update the tsv indecies
    orphanum_tsv = 0
    #get the disease from the orphanet number using the orphanet gene to disease reference
    array_3 = add_data_from(array_2, Orphadata_1, orphanum, orphanum_tsv, disease_orphanet)
    #update the needed tsv indecies
    orphanum_tsv += 1
    #get the OMIM number from the orphanet number using the orphanet gene to disease reference, filter to make sure only OMIM numbers are retrieved
    array_4 = add_data_from(array_3, Orphadata_1, orphanum, orphanum_tsv, omim_number_orphanet, filter_on = True, filter_index = omim_validation_orphanet, filter_by = 'OMIM')
    #update the needed tsv indicies
    orphanum_tsv += 1
    omim_number_tsv = 0
    #get the inheritance from the OMIM number using the OMIM database
    array_5 = add_data_from(array_4, OMIM_data, omim_number_omim, omim_number_tsv, inheritance_omim)
    #update the needed tsv numbers 
    orphanum_tsv += 1
    #get the prevelance from the orphanet number using the Orphanet database, filter to make sure only validated prevelance data is retrieved
    array_6 = add_data_from(array_5, Orphadata_2, orphanum, orphanum_tsv, prevelance_orphanet, filter_on = True, filter_index = validation_orphanet, filter_by = 'Validated')
    
    temp_tsv_name = tsv_file_name.split('.')[0] + '_temp.tsv'
    
    tsv_from_array = write_tsv_from_array(array_6, temp_tsv_name)
    
    #Create a name for the output tsv by adding 'populated' to the end of the name
    #new_tsv_name = 'savePoint.tsv'
    new_tsv_name = tsv_file_name.split('.')[0] + '_populated.tsv'
    
    #clean the final tsv of solo OMIM numbers and add headers
    clean(tsv_from_array, new_tsv_name)
    
    
def main(tsv_file):
    populate(tsv_file)
        
if __name__ == "__main__":
    args = sys.argv
    main(args[1])
    
    
    
    