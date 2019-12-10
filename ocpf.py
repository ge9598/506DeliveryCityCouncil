import pandas as pd
import re
import numpy as np
import Levenshtein
#data= pd.read_excel('2018_ocpf.xlsx')
def read_file(filename):
    excel_file = filename
    data = pd.read_excel(excel_file)
    result = data[['Date', 'Contributor', 'Address', 'Zip', 'Occupation', 'Employer', 'Amount','Recipient','Record Type Description']]
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
    #print(data)
    return data

def getunions():
    PACS=pd.read_excel('boston city council with organization date.xlsx')
    PACSname=PACS['Name, Address'].tolist()
    names=[]
    for item in PACSname:
        sps=item.split('\n')
        name=sps[0]
        if name[-1]=='.':
          names.append(name[0:-1])
        else:
            names.append(name)
    return names
def donation_from_PACS(year,data,time_inc=0):
    ALLPACS=getPACS(year)
    unions = ['Massachusetts Teachers Association', 'Service Employees International Union',
              '1199 SEIU United Healthcare Workers East',
              'American Federation of State, County & Municipal Employees (Council 93)',
              'Massachusetts Nurses Association', "Massachusetts & Northern New England Laborers' District Council",
              "International Brotherhood of Teamsters", "AFT Massachusetts",
              "United Food and Commercial Workers (UFCW) Union", "International Brotherhood of Electrical Workers",
              "United Government Security Officers of America International Union",
              "Professional Fire Fighters of Massachusetts", "New England Regional Council of Carpenters",
              "Unite Here, Local 26", "National Association of Letter Carriers",
              "International Association of Machinists and Aerospace Workers",
              "International Union of Painters & Allied Trades District Council #35", "United Auto Workers Local 2322",
              "Utility Workers of America, Local 369", "Ironworkers Local #7"]
    UnionPACS = []
    NotUnionPACS = []
    index = []
    res = []
    for i in range(len(ALLPACS)):
        sim = []
        for j in range(len(unions)):
            sim.append(Levenshtein.distance(ALLPACS[i], unions[j]))
        if min(sim) <= 11:
            index.append(sim.index(min(sim)))
        else:
            index.append(-1)
    for i in range(len(ALLPACS)):
        a = []
        if index[i] != -1:
            UnionPACS.append(ALLPACS[i])
            a.append(ALLPACS[i])
            a.append(unions[index[i]])
            res.append(a)
    print(ALLPACS)
    print(unions)
    for i in ALLPACS:
        if i not in UnionPACS:
            NotUnionPACS.append(i)
    print("notunion: "+str(NotUnionPACS))
    pacdata=data[data['Contributor'].isin(NotUnionPACS)]
    return pacdata
def donation_from_unionPACS(year,data,time_inc=0):
    ALLPACS=getPACS(year)
    unions = ['Massachusetts Teachers Association', 'Service Employees International Union',
              '1199 SEIU United Healthcare Workers East',
              'American Federation of State, County & Municipal Employees (Council 93)',
              'Massachusetts Nurses Association', "Massachusetts & Northern New England Laborers' District Council",
              "International Brotherhood of Teamsters", "AFT Massachusetts",
              "United Food and Commercial Workers (UFCW) Union", "International Brotherhood of Electrical Workers",
              "United Government Security Officers of America International Union",
              "Professional Fire Fighters of Massachusetts", "New England Regional Council of Carpenters",
              "Unite Here, Local 26", "National Association of Letter Carriers",
              "International Association of Machinists and Aerospace Workers",
              "International Union of Painters & Allied Trades District Council #35", "United Auto Workers Local 2322",
              "Utility Workers of America, Local 369", "Ironworkers Local #7"]
    UnionPACS = []
    UnionPACS2 = []
    NotUnionPACS=[]
    index=[]
    res=[]
    for i in range(len(ALLPACS)):
        sim = []
        for j in range(len(unions)):
            sim.append(Levenshtein.distance(ALLPACS[i],unions[j]))
        if min(sim)<=11:
            index.append(sim.index(min(sim)))
        else:
            index.append(-1)
    for i in range(len(ALLPACS)):
        a=[]
        if index[i]!=-1:
            UnionPACS.append(ALLPACS[i])
            UnionPACS2.append(unions[index[i]])
            a.append(ALLPACS[i])
            a.append(unions[index[i]])
            res.append(a)
    #print(ALLPACS)
    #print(unions)
    #print(index)
    #print(res)
    print("union: "+str(UnionPACS))
    pacdata=pd.concat([data[data['Contributor'].isin(UnionPACS)],data[data['Contributor'].isin(UnionPACS2)]])
    return pacdata
def getPACS(year):
    f=open(str(year)+".txt",encoding='utf-16')
    line=f.readlines()
    names=[]
    for i in range(1,len(line)):
        words=line[i].split('\t')
        names.append(words[1])
    return names

def getlobbyists(data):
    lobbists=pd.read_csv("lobbyist.csv")
    result=lobbists[["NAMEFIRST","NAMELAST"]]
    #print(result)
    names=[]
    for index,row in result.iterrows():
        if (str(row["NAMELAST"])== 'nan'):
            names.append(str(row["NAMEFIRST"]))
        elif (str(row["NAMEFIRST"]) == 'nan'):
            names.append(str(row["NAMELAST"]))
        else:
            names.append(str(row["NAMELAST"])+', '+str(row["NAMEFIRST"]))

    data['IsLobbyist'] = False
    rows = data[['Contributor']]
    contributors=[]
    for index, row in rows.iterrows():
        contributors.append(row['Contributor'])
    #print(contributors)
    for i in range(len(contributors)):
        for kwds in names:
            if kwds in contributors[i]:
                data.loc[i,'IsLobbyist']=True
    return data

def keywords_PACS(data,time_inc=0):
    PACkwds=['PAC','Political Action Committee','Action Comm','Pol Action Comm']
    data['IsPAC']=0
    rows=data[['Contributor']]
    contributors=[]
    for index, row in rows.iterrows():
        contributors.append(row['Contributor'])
    #print(contributors)
    for i in range(len(contributors)):
        for kwds in PACkwds:
            if kwds in contributors[i] or contributors[i] in kwds:
                data.loc[i,'IsPAC']=1
    return data
def keywords_UnionPACS(data,time_inc=0):
    unionkwds='Local [0-9]'
    #data['IsPAC']=0
    rows=data[['Contributor']]
    contributors=[]
    for index, row in rows.iterrows():
        contributors.append(row['Contributor'])
    #print(contributors)
    for i in range(len(contributors)):
            if re.search(unionkwds,contributors[i]) or ("Union" in contributors[i]) or ("Labor" in contributors[i]):
                data.loc[i,'IsPAC']=2
    return data
def self_donation(data):
    rows=data[['Contributor','Recipient']]
    data['self']=False
    for index,row in rows.iterrows():
        cont=row['Contributor']
        reci=row['Recipient']
        if Levenshtein.distance(cont,reci)<=4:
            print(cont,reci)

        if cont==reci:

            data.loc[index,'self']=True
    return data
data20167=read_file('2016-2017data.xlsx')
'''
clean_data2018=clear_data(data20167)
print(clean_data2018)
#print(getPACS(2018))
print(donation_from_PACS(2016,clean_data2018))
print(donation_from_unionPACS(2016,clean_data2018))
print(donation_from_PACS(2017,clean_data2018))
print(donation_from_unionPACS(2017,clean_data2018))
'''
data20189=read_file('2018-2019data.xlsx')

clean_data2019=clear_data(data20189)
print(clean_data2019)
print(getPACS(2018))
print(donation_from_PACS(2019,clean_data2019))
print(donation_from_unionPACS(2019,clean_data2019))

newdtpac=keywords_PACS(data20189)
print(newdtpac)
newdtunion=keywords_UnionPACS(newdtpac)
newdtlobbyist=getlobbyists(newdtunion)
print(newdtlobbyist[newdtlobbyist['IsPAC']!=0])

print(newdtlobbyist[newdtlobbyist['IsLobbyist']==True])
newdtself=self_donation(newdtlobbyist)
print(newdtself)
#print(data20167[data20167['Contributor'].isin(getlobbyists())])
#print(data20189[data20189['Contributor'].isin(getlobbyists())])
#newdtself.to_excel("20189data.xlsx")