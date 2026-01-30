################################################################
import sys
import os
import sqlite3 as sq
import pandas as pd
################################################################
if sys.platform == 'linux':
    Base = os.path.expanduser('~') + '/VKHCG'
else:
    Base = 'C:/VKHCG'

print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')
################################################################
Company = '04-Clark'
sInputFileName1 = '01-Retrieve/01-EDS/02-Python/Retrieve-Data_female-names.csv'
sInputFileName2 = '01-Retrieve/01-EDS/02-Python/Retrieve-Data_male-names.csv'
sInputFileName3 = '01-Retrieve/01-EDS/02-Python/Retrieve-Data_last-names.csv'
sOutputFileName1 = 'Assess-Staff.csv'
sOutputFileName2 = 'Assess-Customers.csv'
################################################################
sDataBaseDir = Base + '/' + Company + '/02-Assess/SQLite'
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)
################################################################
sDatabaseName = sDataBaseDir + '/clark.db'
conn = sq.connect(sDatabaseName)
################################################################
### Import Female Data
################################################################
sFileName = Base + '/' + Company + '/' + sInputFileName1
print('################################')
print('Loading :', sFileName)
print('################################')
FemaleRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
FemaleRawData.rename(columns={'NameValues': 'FirstName'}, inplace=True)
FemaleRawData.drop_duplicates(subset=None, keep='first', inplace=True)
FemaleData = FemaleRawData.sample(100)
print('################################')
################################################################
print('################')
sTable = 'Assess_FemaleName'
print('Storing :', sDatabaseName, ' Table:', sTable)
FemaleData.to_sql(sTable, conn, if_exists="replace")
print('################')
################################################################
print('################################')
print('Rows : ', FemaleData.shape[0], ' records')
print('################################')
################################################################
### Import Male Data
################################################################
sFileName = Base + '/' + Company + '/' + sInputFileName2
print('################################')
print('Loading :', sFileName)
print('################################')
MaleRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
MaleRawData.rename(columns={'NameValues': 'FirstName'}, inplace=True)
MaleRawData.drop_duplicates(subset=None, keep='first', inplace=True)
MaleData = MaleRawData.sample(100)
print('################################')
################################################################
print('################')
sTable = 'Assess_MaleName'
print('Storing :', sDatabaseName, ' Table:', sTable)
MaleData.to_sql(sTable, conn, if_exists="replace")
print('################')
################################################################
print('################################')
print('Rows : ', MaleData.shape[0], ' records')
print('################################')
################################################################
### Import Surname Data
################################################################
sFileName = Base + '/' + Company + '/' + sInputFileName3
print('################################')
print('Loading :', sFileName)
print('################################')
SurnameRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
SurnameRawData.rename(columns={'NameValues': 'LastName'}, inplace=True)
SurnameRawData.drop_duplicates(subset=None, keep='first', inplace=True)
SurnameData = SurnameRawData.sample(200)
print('################################')
################################################################
print('################')
sTable = 'Assess_Surname'
print('Storing :', sDatabaseName, ' Table:', sTable)
SurnameData.to_sql(sTable, conn, if_exists="replace")
print('################')
################################################################
print('################################')
print('Rows : ', SurnameData.shape[0], ' records')
print('################################')
################################################################
################################################################
print('################')
sTable = 'Assess_FemaleName & Assess_MaleName'
print('Loading :', sDatabaseName, ' Table:', sTable)
sSQL = "select distinct A.FirstName, 'Female' as Gender from Assess_FemaleName as A " \
       "UNION select distinct A.FirstName, 'Male' as Gender from Assess_MaleName as A;"
FirstNameData = pd.read_sql_query(sSQL, conn)
print('################')
################################################################
sTable = 'Assess_FirstName'
print('Storing :', sDatabaseName, ' Table:', sTable)
FirstNameData.to_sql(sTable, conn, if_exists="replace")
print('################')
################################################################
################################################################
print('################')
sTable = 'Assess_FirstName x2 & Assess_Surname'
print('Loading :', sDatabaseName, ' Table:', sTable)

sSQL = "select distinct A.FirstName, B.FirstName AS SecondName, C.LastName, A.Gender " \
       "from Assess_FirstName as A, Assess_FirstName as B, Assess_Surname as C " \
       "WHERE A.Gender = B.Gender AND A.FirstName <> B.FirstName;"

PeopleRawData = pd.read_sql_query(sSQL, conn)
People1Data = PeopleRawData.sample(10000)

sTable = 'Assess_FirstName & Assess_Surname'
print('Loading :', sDatabaseName, ' Table:', sTable)

sSQL = "select distinct A.FirstName, '' AS SecondName, B.LastName, A.Gender " \
       "from Assess_FirstName as A, Assess_Surname as B;"

PeopleRawData = pd.read_sql_query(sSQL, conn)
People2Data = PeopleRawData.sample(10000)

PeopleData = People1Data.append(People2Data)
print(PeopleData)
print('################')
################################################################
sTable = 'Assess_People'
print('Storing :', sDatabaseName, ' Table:', sTable)
PeopleData.to_sql(sTable, conn, if_exists="replace")
print('################')
################################################################
sFileDir = Base + '/' + Company + '/02-Assess/01-EDS/02-Python'
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)
################################################################
sOutputFileName = sTable + '.csv'
sFileName = sFileDir + '/' + sOutputFileName
print('################################')
print('Storing :', sFileName)
print('################################')
PeopleData.to_csv(sFileName, index=False)
print('################################')
################################################################
print('### Done!! ############################################')
################################################################
