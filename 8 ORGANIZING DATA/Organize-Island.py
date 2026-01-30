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

# Open Warehouse + Datamart
sDatabaseName = sDataWarehouseDir + '/datawarehouse.db'
conn1 = sq.connect(sDatabaseName)

sDatabaseName = sDataWarehouseDir + '/datamart.db'
conn2 = sq.connect(sDatabaseName)
################################################################

print('################')
sTable = 'Dim-BMI'
print('Loading from Warehouse :', sTable)

sSQL = "SELECT * FROM [Dim-BMI];"
PersonFrame0 = pd.read_sql_query(sSQL, conn1)
################################################################

print('################')
print('Filtering Data...')

sSQL = """
SELECT 
       Height,
       Weight,
       Indicator
  FROM [Dim-BMI]
 WHERE Indicator > 2
 ORDER BY Height, Weight;
"""
PersonFrame1 = pd.read_sql_query(sSQL, conn1)
################################################################

# Create vertical-style table indexed by Indicator
DimPerson = PersonFrame1
DimPersonIndex = DimPerson.set_index(['Indicator'], inplace=False)
################################################################

sTable = 'Dim-BMI-Vertical'
print('\n#################################')
print('Storing into Datamart:', sTable)
print('#################################')

DimPersonIndex.to_sql(sTable, conn2, if_exists="replace")
################################################################

print('################################')
print('Loading Back from Datamart:', sTable)
print('################################')

sSQL = "SELECT * FROM [Dim-BMI-Vertical];"
PersonFrame2 = pd.read_sql_query(sSQL, conn2)
################################################################

# Summary Output
print('################################')
print('Full Data Set (Rows):', PersonFrame0.shape[0])
print('Full Data Set (Columns):', PersonFrame0.shape[1])
print('################################')

print('Vertical Data Set (Rows):', PersonFrame2.shape[0])
print('Vertical Data Set (Columns):', PersonFrame2.shape[1])
print('################################')
################################################################
