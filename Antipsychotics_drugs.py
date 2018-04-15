#! /bin/python2

drugbank_file_path = 'drugbank.xml'
category_to_search = 'Antipsychotic Agents'
path_of_file_to_write = 'id_list.txt'
id_list = []
# first read the file
with open (drugbank_file_path) as inputfile:
    # each line is an element of the 'data' list
    data = inputfile.readlines()

# now parse the read file for the drugs we need
for index, element in enumerate(data):
    # new drugs always start with '<drug ', 
    # also make sure that the next element is the id one
    # we need this since there are some <drugbank-id primary="true">DBSALTXXXXXXX</drugbank-id>
    # lines that need to be avoided
    if '<drug ' in element and '<drugbank-id primary="true">' in data[index+1]:
        # now get the id (it is the immediate next element, but do a customary check for it)
        drug_id = data[index+1].lstrip('<drugbank-id primary="true">').rstrip('</drugbank-id>\n')

    if  category_to_search in element and '<category>' in data[index+1]:
        id_list.append(drug_id)
    # if we match the category, save the id
    #elif category_to_search in element: #
    #    id_list.append(drug_id)


# finally write the list to file
with open(path_of_file_to_write, 'w') as file_to_write:
    for drug_id in id_list:
      file_to_write.write("%s\n" % drug_id)

