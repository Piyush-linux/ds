################################################################
# -*- coding: utf-8 -*-
################################################################
import sys
import os
import pandas as pd
import sqlite3 as sq
################################################################

# Set Base Directory
if sys.platform == 'linux':
    Base = os.path.expanduser('~') + '/VKHCG'
else:
    Base = 'C:/VKHCG'

print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')
################################################################

Company = '01-Vermeulen'
################################################################

# Ensure Data Warehouse Directory Exists
sDataWarehouseDir = Base + '/99-DW'
if not os.path.exists(sDataWarehouseDir):
    os.makedirs(sDataWarehouseDir)
################################################################

# Open Warehouse Database
sDatabaseName = sDataWarehouseDir + '/datawarehouse.db'
conn1 = sq.connect(sDatabaseName)

# Open DataMart Database
sDatabaseName = sDataWarehouseDir + '/datamart.db'
conn2 = sq.connect(sDatabaseName)
################################################################

print('################')
sTable = 'Dim-BMI'
print('Loading :', sDatabaseName, ' Table:', sTable)

sSQL = "SELECT * FROM [Dim-BMI];"
PersonFrame0 = pd.read_sql_query(sSQL, conn1)
################################################################

print('################')
sTable = 'Dim-BMI'
print('Loading :', sDatabaseName, ' Table:', sTable)

sSQL = """
SELECT 
       Height,
       Weight,
       Indicator,
       CASE Indicator
           WHEN 1 THEN 'Pip'
           WHEN 2 THEN 'Norman'
           WHEN 3 THEN 'Grant'
           ELSE 'Sam'
       END AS Name
  FROM [Dim-BMI]
 WHERE Indicator > 2
 ORDER BY Height, Weight;
"""
PersonFrame1 = pd.read_sql_query(sSQL, conn1)
################################################################

# Create Secure Dimension Table
DimPerson = PersonFrame1
DimPersonIndex = DimPerson.set_index(['Indicator'], inplace=False)
################################################################

sTable = 'Dim-BMI-Secure'
print('\n#################################')
print('Storing :', sDatabaseName, '\n Table:', sTable)
print('#################################')

DimPersonIndex.to_sql(sTable, conn2, if_exists="replace")
################################################################

print('################################')
sTable = 'Dim-BMI-Secure'
print('Loading :', sDatabaseName, ' Table:', sTable)
print('################################')

sSQL = "SELECT * FROM [Dim-BMI-Secure] WHERE Name = 'Sam';"
PersonFrame2 = pd.read_sql_query(sSQL, conn2)
################################################################

print('################################')
print('Full Data Set (Rows):', PersonFrame0.shape[0])
print('Full Data Set (Columns):', PersonFrame0.shape[1])
print('################################')

print('Filtered Secure Data (Rows):', PersonFrame2.shape[0])
print('Filtered Secure Data (Columns):', PersonFrame2.shape[1])
print('Only Sam Data:')
print(PersonFrame2.head())
print('################################')
################################################################
