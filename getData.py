import numpy as np
import pandas as pd


def read_file():
    excel_file = "2018_ocpf.xlsx"
    data = pd.read_excel(excel_file)
    result = data[['Date', 'Contributor', 'Address', 'Zip', 'Occupation', 'Employer', 'Amount', 'Recipient','Record Type Description']]
    return result
def read_file_2019():
    excel_file = "2019_ocpf.xlsx"
    data = pd.read_excel(excel_file)
    result = data[['Date', 'Contributor', 'Address', 'Zip', 'Occupation', 'Employer', 'Amount', 'Recipient','Record Type Description']]
    return result

def clear_data(data):
    # first delete data if address or contributor are null
    data.dropna(subset = ['Address'], inplace = True)
    data.dropna(subset = ['Contributor'], inplace = True)
    # then change rest NaN to string"not provided"
    data = data.replace(np.NaN, "NOT PROVIDED", regex = True)
    # only pick the ones that has been picked
    candidate_list_2018 = ['Wu, Michelle', 'Essaibi George, Annissa', 'Flaherty Jr., Michael F', 'Garrison, Althea','Edwards, Lydia','Flynn, Edward Michael','Baker, Frank','Campbell, Andrea Joy','Arroyo, Ricardo N.','O\'Malley, Matthew J.','Janey, Kim','Bok, Kenzie','Breadon, Elizabeth A.']
    data = data[data['Recipient'].isin(candidate_list_2018)]
    print(data)
    return data
def check_unique(data):
    unique_contributor_list = list(data['Contributor'].unique())
    return unique_contributor_list
data2018 = read_file()
data2019 = read_file_2019()
data2018 = clear_data(data2018)
data2019 = clear_data(data2019)
data_2018_2019 = pd.concat([data2018,data2019])
unique_contributor_list_2018 = check_unique(data2018)
unique_contributor_list_2019 = check_unique(data2019)
unique_contributor_list = check_unique(data_2018_2019)
print("Number of Unique Donation in 2018:" + str(np.shape(unique_contributor_list_2018)))
print("Number of Unique Donation in 2019:" + str(np.shape(unique_contributor_list_2019)))
print("Number of Unique Donation in 2018 - 2019:" + str(np.shape(unique_contributor_list)))
