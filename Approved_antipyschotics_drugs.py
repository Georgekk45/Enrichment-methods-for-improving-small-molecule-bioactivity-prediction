#! /bin/python2
import random

drugbank_file_path = 'drugbank-approved.csv'
category_to_search = 'Antipsychotic Agents'
path_of_file_to_write = 'matched_id_list.csv'
matched_id_list = []
other_id_list = []
drug_id = False
with open (drugbank_file_path) as inputfile:
    data = inputfile.readlines()

for index, element in enumerate(data):
    if '<drug ' in element and '<drugbank-approved-id primary="true">' in data[index+1]:
        if drug_id and drug_id not in matched_id_list: other_id_list.append(drug_id)
        drug_id = data[index+1].lstrip('<drugbank-approved-id primary="true">').rstrip('</drugbank-approved-id>\n')
    elif category_to_search in element:
        matched_id_list.append(drug_id)

# finally write the list to file
with open(path_of_file_to_write, 'w') as file_to_write:
    for drug_id in matched_id_list:
        file_to_write.write("%s\n" % drug_id)

sets = []
while (len(other_id_list) > 38):
    new_set = []
    for drug_id in range (38):
        choose = random.randint(0,len(other_id_list))
        new_set.append(other_id_list.pop(choose-1))
    sets.append(new_set)

with open(path_of_file_to_write, 'w') as file_to_write:
    for set_index, drug_set in enumerate(sets):
        for drug_id in drug_set:
            file_to_write.write("%s\n" % drug_id)
        file_to_write.write('===== set %s \n' % str(set_index+1))
