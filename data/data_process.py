import xlrd
from pymongo import MongoClient

client = MongoClient()
db = client.cs504

# age group
#  18-24
#  25-34
#  35-49
#  50-64
#  65+


# Helper functions
def convert_age_to_group(age):
    if isinstance(age, int) or isinstance(age, float):
        if 18 <= age <= 24:
            return "18-24"
        elif 25 <= age <= 34:
            return "25-34"
        elif 35 <= age <= 49:
            return "35-49"
        elif 50 <= age <= 64:
            return "50-64"
        elif age >= 65:
            return "65+"
        else:
            print(age)
            raise Exception("Incorrect Age")
    elif isinstance(age, str):
        if age == "18 to 24":
            return "18-24"
        elif age == "25 to 34":
            return "25-34"
        elif age == "35 to 49":
            return "35-49"
        elif age == "50 to 64":
            return "50-64"
        elif age == "65+":
            return "65+"
        else:
            print(age)
            raise Exception("Incorrect Age")
    else:
        raise Exception("Incorrect Age")

def convert_gender_to_group(gender):
    if gender == "M":
        return "Male"
    elif gender == "F":
        return "Female"
    else:
        raise Exception("Incorrect gender")


def get_ward_id(name):
    return int(name.split(" ")[1][1:])

#%%

# Process VAN File
stat_for_van_file = {}
for i in range(1, 23):
    stat_for_van_file[i] = {
        'Age': {
            '18-24': 0,
            '25-34': 0,
            '35-49': 0,
            '50-64': 0,
            '65+': 0
        },
        'Gender': {
            'Male': 0,
            'Female': 0
        }
    }

# col-F(5) sex, col-N(13) Age, col-Q(16) precinct (Boston W14 P14)
data = xlrd.open_workbook("VAN File - All Wards SPARK USE.xlsx")
table = data.sheets()[0]

for row in range(1, table.nrows):
    wid = get_ward_id(table.cell(row, 16).value)
    age_group = convert_age_to_group(table.cell(row, 13).value)

    gender_field = table.cell(row, 5).value
    if gender_field == "U":
        continue
    gender_group = convert_gender_to_group(gender_field)

    stat_for_van_file[wid]["Age"][age_group] += 1
    stat_for_van_file[wid]["Gender"][gender_group] += 1

print(stat_for_van_file)

#%%

# Process reg files
stat_for_eligible = {}
stat_for_registered = {}
for i in range(1, 23):
    stat_for_eligible[i] = {
        'Age': {
            '18-24': 0,
            '25-34': 0,
            '35-49': 0,
            '50-64': 0,
            '65+': 0
        },
        'Gender': {
            'Male': 0,
            'Female': 0
        }
    }

    stat_for_registered[i] = {
        'Age': {
            '18-24': 0,
            '25-34': 0,
            '35-49': 0,
            '50-64': 0,
            '65+': 0
        },
        'Gender': {
            'Male': 0,
            'Female': 0
        }
    }

# row N-R S(Unknown)
data = xlrd.open_workbook("registered_voters_xtabs.xlsx")
table = data.sheets()[3]

for row in range(180, 435):
    for col in range(13, 18):
        age_group = convert_age_to_group(table.cell(2, col).value)
        wid = get_ward_id(table.cell(row, 0).value)

        stat_for_eligible[wid]["Age"][age_group] += int(table.cell(row, col).value)
        stat_for_registered[wid]["Age"][age_group] += int(table.cell(row, col).value)

print(stat_for_registered)

#%%

# Process non-reg files

# row N-R S(Unknown)
data = xlrd.open_workbook("non_registered_xtabs.xlsx")
table = data.sheets()[3]

for row in range(180, 435):
    for col in range(13, 18):
        age_group = convert_age_to_group(table.cell(2, col).value)
        wid = get_ward_id(table.cell(row, 0).value)

        stat_for_eligible[wid]["Age"][age_group] += int(table.cell(row, col).value)

print(stat_for_eligible)

#%%

# process election files
stat_for_election = {}

# row 2, 5, 8, 11, 14
data = xlrd.open_workbook("Historical Votes Cast by Boston Ward.xlsx")
table = data.sheets()[0]

for row in range(1, 14, 3):
    year = int(table.cell(row, 0).value.split(" ")[0])
    ward_election = {}
    for col in range(1, 44, 2):
        wid = int(table.cell(0, col).value)

        ward_election[wid] = {
            "1st": {
                "Name": table.cell(row, col+1).value,
                "Votes": table.cell(row, col).value
            },
            "2nd": {
                "Name": table.cell(row+1, col+1).value,
                "Votes": table.cell(row+1, col).value
            }
        }

    stat_for_election[year] = ward_election

print(stat_for_election)

#%%

# Agg date by year

result = []
for ward_id in range(1, 23):
    result.append({
        "Ward": ward_id,
        "Voter": {
            "Eligible": stat_for_eligible[ward_id],
            "Registered": stat_for_registered[ward_id],
            "Voted": stat_for_van_file[ward_id]
        },
        "Election": stat_for_election[2017][ward_id]
    })

ward_data = db.ward_data
ward_data.insert_many(result)
