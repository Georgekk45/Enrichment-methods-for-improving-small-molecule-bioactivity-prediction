#! /bin/python2

import pandas
import numpy

number_of_desired_samples = 200
antipsychotics_file = '200.csv'
target_prediction_file = '256.csv'
database_file = 'drugbank-approved-1 .csv'
output_file = 'results.csv'

database = pandas.read_csv(database_file)
antipsychotics_dataframe = pandas.read_csv(antipsychotics_file, header = None, names = ['antipsychotics'])
target_prediction = pandas.read_csv(target_prediction_file)

# create a Series of the approved agents for comparing
approved_antipsychotics = antipsychotics_dataframe.antipsychotics.values

# the length of the randomly created samples will equal the antipsycho dataset
approved_agents_num = len(approved_antipsychotics)

# create a dataframe keeping only the antipsychotics
approved_antipsychotics_dataframe = database.loc[database.ID.isin(approved_antipsychotics)]

# remove the antipsychotic agents from the db file to avoid using antipsycho agents in the random samples
for antipshychotic in approved_antipsychotics:
    database = database.loc[database.ID != antipshychotic]

# create number_of_desired_samples sets of random agents. each sample will have agents
# equal to the number of antiphsychotic agents
sets_list = []
for sample_no in range(number_of_desired_samples):
    sets_list.append(database.sample(approved_agents_num))

# just store one row per set. This row will be the sum of all rows & the resulting row will be a pandas Series
sets_sum_list = []
for random_set in sets_list:
    sets_sum_list.append(random_set.sum())

# do the same for the approved_antipsychotics
approved_antipsychotics_sums = approved_antipsychotics_dataframe.sum()

# finally concatenate the sums into one dataframe. this will be the final dataframe
results = approved_antipsychotics_sums
for set_sum in sets_sum_list:
    results = pandas.concat([results,set_sum], axis=1)
results = results.transpose()
results.index = numpy.arange(len(results))


# do a copy so as not to lose the results original file
comparison_dataframe = results.copy()

# compare each value of each row of the dataframe to the value of the antipsychotic sample. results will be True/False
for comparison_candidate in comparison_dataframe[1:].iterrows():
    comparison_dataframe.loc[comparison_candidate[0]] = (comparison_dataframe.iloc[0] > comparison_dataframe.loc[comparison_candidate[0]])

# if the random sample wins, set the value = 0, else 1
comparison_dataframe = comparison_dataframe.applymap(lambda x: 1 if x else 0)

# for each column get the average value and append it to a list
estimation_score = []
for column in comparison_dataframe:
    if column != 'ID':
        estimation_score.append(comparison_dataframe[column].mean())

# convert the estimation_score list to a pandas dataframe object in order to add it to the results Dataframe
estimation_score.insert(0,numpy.nan)
estimation_score = pandas.DataFrame(estimation_score).transpose()
estimation_score.columns = results.columns
estimation_score.index = ['estimations']
# do the final addition
results = pandas.concat([results,estimation_score])
# export to csv
results.to_csv(output_file)
