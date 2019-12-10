import numpy as np
import pandas as pd


def read_file_2018():
    excel_file = "2018_ocpf_all.xlsx"
    data = pd.read_excel(excel_file)
    result = data[['Date', 'Contributor', 'Address','City','State', 'Zip', 'Occupation', 'Employer', 'Amount', 'Recipient','Record Type Description']]
    return result
def read_file_2019():
    excel_file = "2019_ocpf_all.xlsx"
    data = pd.read_excel(excel_file)
    result = data[['Date', 'Contributor', 'Address','City','State', 'Zip', 'Occupation', 'Employer', 'Amount', 'Recipient','Record Type Description']]
    return result
def read_file_2016():
    csv_file = '2016_ocpf.csv'
    data = pd.read_csv(csv_file)
    result = data[['Date', 'Contributor', 'Address', 'Zip', 'Occupation', 'Employer', 'Amount', 'Recipient','Record Type Description']]
    return result
def read_file_2017():
    csv_file = '2017_ocpf.csv'
    data = pd.read_csv(csv_file)
    result = data[['Date', 'Contributor', 'Address', 'Zip', 'Occupation', 'Employer', 'Amount', 'Recipient','Record Type Description']]
    return result

def clear_data_2016(data):
    # first delete data if address or contributor are null
    data.dropna(subset = ['Address'], inplace = True)
    data.dropna(subset = ['Contributor'], inplace = True)
    # then change rest NaN to string"not provided"
    data = data.replace(np.NaN, "NOT PROVIDED", regex = True)
    print(np.dtype(data['Amount']))
    candidate_list_2016 = ['Essaibi George, Annissa','Flaherty Jr., Michael F.','Pressley, Ayanna','Wu, Michelle','Edwards, Lydia','Flynn, Edward Michael','Baker, Frank','Campbell, Andrea Joy','McCarthy, Timothy Patrick','O\'Malley, Matthew J.','Janey, Kim','Zakim, Joshua','Ciommo, Mark']
    data = data[data['Recipient'].isin(candidate_list_2016)]
    print(data)
    return data
def clear_data(data):
    # first delete data if address or contributor are null
    data.dropna(subset = ['Address'], inplace = True)
    data.dropna(subset = ['Contributor'], inplace = True)
    # then change rest NaN to string"not provided"
    data = data.replace(np.NaN, "NOT PROVIDED", regex = True)
    print(np.dtype(data['Amount']))
    candidate_list_2018 = ['Wu, Michelle', 'Essaibi George, Annissa', 'Flaherty Jr., Michael F.', 'Garrison, Althea','Edwards, Lydia','Flynn, Edward Michael','Baker, Frank','Campbell, Andrea Joy','Arroyo, Ricardo N.','O\'Malley, Matthew J.','Janey, Kim','Bok, Priscilla MacKenzie','Breadon, Elizabeth A.']
    data = data[data['Recipient'].isin(candidate_list_2018)]
    print(data)
    return data
def check_unique(data):
    data = data.drop_duplicates(['Contributor'])
    return data
def print_unique_contributor(data2016,data2017,data2018, data2019, data_total_2016,data_total_2018):
    unique_contributor_list_2016 = check_unique(data2016)
    unique_contributor_list_2017 = check_unique(data2017)
    unique_contributor_list_2018 = check_unique(data2018)
    unique_contributor_list_2019 = check_unique(data2019)
    unique_contributor_list_first = check_unique(data_total_2016)
    unique_contributor_list_second = check_unique(data_total_2018)
    print("Number of Unique Donation in 2016:" + str(len(unique_contributor_list_2016)))
    print("Number of Unique Donation in 2017:" + str(len(unique_contributor_list_2017)))
    print("Number of Unique Donation in 2016 - 2017:" + str(len(unique_contributor_list_first)))
    print("")
    print("Number of Unique Donation in 2018:" + str(len(unique_contributor_list_2018)))
    print("Number of Unique Donation in 2019:" + str(len(unique_contributor_list_2019)))
    print("Number of Unique Donation in 2018 - 2019:" + str(len(unique_contributor_list_second)))
def check_contribution_category(data,year):
    less25 = data[data['Amount'] < 25]
    less99great25 = data[(data['Amount'] >= 25) & (data['Amount'] < 100)]
    less249great100 = data[(data['Amount'] >= 100) & (data['Amount'] < 250)]
    less499great250 = data[(data['Amount'] >= 250) & (data['Amount'] < 499)]
    less1000great500 = data[(data['Amount'] >= 500) & (data['Amount'] < 1000)]
    print("***************************************************************")
    print("*****************" + year + "*************************")
    print("# less than 25$:" + str(len(less25)))
    print("# less than 99$ and greater than 25$:" + str(len(less99great25)))
    print("# less than 249$ and greater than 99$:" + str(len(less249great100)))
    print("# less than 499$ and greater than 249$:" + str(len(less499great250)))
    print("# less than 500$ and greater than 1000$:" + str(len(less1000great500)))

def print_check_contribution_category(data2016,data2017,data2018, data2019, data_total_2016,data_total_2018):
    check_contribution_category(data2016," year of 2016 ")
    check_contribution_category(data2017," year of 2017 ")
    check_contribution_category(data_total_2016," year of 2016 - 2017 ")
    check_contribution_category(data2018," year of 2018 ")
    check_contribution_category(data2019, " year of 2019 ")
    check_contribution_category(data_total_2018, " year of 2018 - 2019 ")
data2016 = read_file_2016()
data2017 = read_file_2017()
data2018 = read_file_2018()
data2019 = read_file_2019()
data2016 = clear_data_2016(data2016)
data2017 = clear_data_2016(data2017)
data2018 = clear_data(data2018)
data2019 = clear_data(data2019)
data_total_2016 = pd.concat([data2016,data2017])
export_excel = data_total_2016.to_excel (r'2016-2017data.xlsx', index = None, header=True) #Don't forget to add '.xlsx' at the end of the path
data_total_2018 = pd.concat([data2018,data2019])
export_excel1 = data_total_2018.to_excel (r'2018-2019data.xlsx', index = None, header=True) #Don't forget to add '.xlsx' at the end of the path


print(np.shape(data2018))
print_unique_contributor(data2016,data2017,data2018, data2019, data_total_2016,data_total_2018)
print_check_contribution_category(data2016,data2017,data2018, data2019, data_total_2016,data_total_2018)
