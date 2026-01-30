################################################################
import sys
import os
import sqlite3 as sq
import pandas as pd
################################################################

if sys.platform == 'linux': 
    Base = os.path.expanduser('~') + 'VKHCG'
else:
    Base = 'C:/VKHCG'

print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')
################################################################

sInputFileName1 = '01-Retrieve/01-EDS/02-Python/Retrieve_DE_Billboard_Locations.csv'
sInputFileName2 = '01-Retrieve/01-EDS/02-Python/Retrieve_Online_Visitor.csv'
sOutputFileName = 'Assess-DE-Billboard-Visitor.csv'
Company = '02-Krennwallner'
################################################################

sDataBaseDir = Base + '/' + Company + '/02-Assess/SQLite'
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)
################################################################

sDatabaseName = sDataBaseDir + '/krennwallner.db'
conn = sq.connect(sDatabaseName)
################################################################
### Import Billboard Data
################################################################

sFileName = Base + '/' + Company + '/' + sInputFileName1
print('################################')
print('Loading :', sFileName)
print('################################')

BillboardRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
BillboardRawData.drop_duplicates(subset=None, keep='first', inplace=True)
BillboardData = BillboardRawData

print('Loaded Company :', BillboardData.columns.values)
print('################################')
################################################################

print('################')
sTable = 'Assess_BillboardData'
print('Storing :', sDatabaseName, ' Table:', sTable)
BillboardData.to_sql(sTable, conn, if_exists="replace")
print('################')
################################################################

print(BillboardData.head())
print('################################')
print('Rows : ', BillboardData.shape[0])
print('################################')
################################################################
### Import Visitor Data
################################################################

sFileName = Base + '/' + Company + '/' + sInputFileName2
print('################################')
print('Loading :', sFileName)
print('################################')

VisitorRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
VisitorRawData.drop_duplicates(subset=None, keep='first', inplace=True)
VisitorData = VisitorRawData[VisitorRawData.Country == 'DE']

print('Loaded Company :', VisitorData.columns.values)
print('################################')
################################################################

print('################')
sTable = 'Assess_VisitorData'
print('Storing :', sDatabaseName, ' Table:', sTable)
VisitorData.to_sql(sTable, conn, if_exists="replace")
print('################')
################################################################

print(VisitorData.head())
print('################################')
print('Rows : ', VisitorData.shape[0])
print('################################')
################################################################

print('################')
sTable = 'Assess_BillboardVisitorData'
print('Loading :', sDatabaseName, ' Table:', sTable)

sSQL = "select distinct" \
       " A.Country AS BillboardCountry," \
       " A.Place_Name AS BillboardPlaceName," \
       " A.Latitude AS BillboardLatitude," \
       " A.Longitude AS BillboardLongitude," \
       " B.Country AS VisitorCountry," \
       " B.Place_Name AS VisitorPlaceName," \
       " B.Latitude AS VisitorLatitude," \
       " B.Longitude AS VisitorLongitude," \
       " (B.Last_IP_Number - B.First_IP_Number) * 365.25 * 24 * 12 AS VisitorYearRate" \
       " from Assess_BillboardData as A" \
       " JOIN Assess_VisitorData as B" \
       " ON A.Country = B.Country AND A.Place_Name = B.Place_Name;"

BillboardVistorsData = pd.read_sql_query(sSQL, conn)

print('################')
################################################################

print('################')
sTable = 'Assess_BillboardVistorsData'
print('Storing :', sDatabaseName, ' Table:', sTable)
BillboardVistorsData.to_sql(sTable, conn, if_exists="replace")
print('################')
################################################################

print(BillboardVistorsData.head())
print('################################')
print('Rows : ', BillboardVistorsData.shape[0])
print('################################')
################################################################

sFileDir = Base + '/' + Company + '/02-Assess/01-EDS/02-Python'
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)
################################################################

print('################################')
print('Storing :', sFileName)
print('################################')

sFileName = sFileDir + '/' + sOutputFileName
BillboardVistorsData.to_csv(sFileName, index=False)

print('################################')
################################################################
print('### Done!! ############################################')
################################################################
