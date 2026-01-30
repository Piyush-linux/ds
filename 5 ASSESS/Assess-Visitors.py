################################################################
import sys
import os
import sqlite3 as sq
import pandas as pd
from pandas.io import sql
################################################################

if sys.platform == 'linux':
    Base = os.path.expanduser('~') + 'VKHCG'
else:
    Base = 'C:/VKHCG'

print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')
################################################################

Company = '02-Krennwallner'
sInputFileName = '01-Retrieve/01-EDS/02-Python/Retrieve_Online_Visitor.csv'
################################################################

sDataBaseDir = Base + '/' + Company + '/02-Assess/SQLite'
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)
################################################################

sDatabaseName = sDataBaseDir + '/krennwallner.db'
conn = sq.connect(sDatabaseName)
################################################################

### Import Country Data
################################################################
sFileName = Base + '/' + Company + '/' + sInputFileName
print('################################')
print('Loading :', sFileName)
print('################################')

VisitorRawData = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    encoding="latin-1",
    skip_blank_lines=True
)

VisitorRawData.drop_duplicates(subset=None, keep='first', inplace=True)
VisitorData = VisitorRawData

print('Loaded Company :', VisitorData.columns.values)
print('################################')
################################################################

print('################')
sTable = 'Assess_Visitor'
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
sView = 'Assess_Visitor_UseIt'
print('Creating :', sDatabaseName, ' View:', sView)

sSQL = "DROP VIEW IF EXISTS " + sView + ";"
sql.execute(sSQL, conn)

sSQL = "CREATE VIEW " + sView + " AS"
sSQL += " SELECT"
sSQL += " A.Country,"
sSQL += " A.Place_Name,"
sSQL += " A.Latitude,"
sSQL += " A.Longitude,"
sSQL += " (A.Last_IP_Number - A.First_IP_Number) AS UsesIt"
sSQL += " FROM"
sSQL += " Assess_Visitor as A"
sSQL += " WHERE"
sSQL += " Country is not null"
sSQL += " AND"
sSQL += " Place_Name is not null;"
sql.execute(sSQL, conn)
#################################################################

print('################')
sView = 'Assess_Total_Visitors_Location'
print('Creating :', sDatabaseName, ' View:', sView)

sSQL = "DROP VIEW IF EXISTS " + sView + ";"
sql.execute(sSQL, conn)

sSQL = "CREATE VIEW " + sView + " AS"
sSQL += " SELECT"
sSQL += " Country,"
sSQL += " Place_Name,"
sSQL += " SUM(UsesIt) AS TotalUsesIt"
sSQL += " FROM"
sSQL += " Assess_Visitor_UseIt"
sSQL += " GROUP BY"
sSQL += " Country,"
sSQL += " Place_Name"
sSQL += " ORDER BY"
sSQL += " TotalUsesIt DESC"
sSQL += " LIMIT 10;"
sql.execute(sSQL, conn)
#################################################################

print('################')
sView = 'Assess_Total_Visitors_GPS'
print('Creating :', sDatabaseName, ' View:', sView)

sSQL = "DROP VIEW IF EXISTS " + sView + ";"
sql.execute(sSQL, conn)

sSQL = "CREATE VIEW " + sView + " AS"
sSQL += " SELECT"
sSQL += " Latitude,"
sSQL += " Longitude,"
sSQL += " SUM(UsesIt) AS TotalUsesIt"
sSQL += " FROM"
sSQL += " Assess_Visitor_UseIt"
sSQL += " GROUP BY"
sSQL += " Latitude,"
sSQL += " Longitude"
sSQL += " ORDER BY"
sSQL += " TotalUsesIt DESC"
sSQL += " LIMIT 10;"
sql.execute(sSQL, conn)
#################################################################

sTables = ['Assess_Total_Visitors_Location', 'Assess_Total_Visitors_GPS']
for sTable in sTables:
    print('################')
    print('Loading :', sDatabaseName, ' Table:', sTable)

    sSQL = " SELECT * FROM " + sTable + ";"
    TopData = pd.read_sql_query(sSQL, conn)

    print('################')
    print(TopData)
    print('################')
    print('################################')
    print('Rows : ', TopData.shape[0])
    print('################################')

################################################################
print('### Done!! ############################################')
################################################################
