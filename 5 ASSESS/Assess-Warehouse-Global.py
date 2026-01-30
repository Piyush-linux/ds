################################################################
# -*- coding: utf-8 -*-
################################################################
import sys
import os
import pandas as pd
################################################################

# Set Base directory depending on OS
if sys.platform == 'linux':
    Base = os.path.expanduser('~') + 'VKHCG'
else:
    Base = 'C:/VKHCG'

################################################################
print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')
################################################################

Company = '03-Hillman'
InputDir = '01-Retrieve/01-EDS/01-R'
InputFileName = 'Retrieve_All_Countries.csv'

EDSDir = '02-Assess/01-EDS'
OutputDir = EDSDir + '/02-Python'
OutputFileName = 'Assess_All_Warehouse.csv'

################################################################
# Ensure EDS directory exists
sFileDir = Base + '/' + Company + '/' + EDSDir
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

################################################################
# Ensure Output directory exists
sFileDir = Base + '/' + Company + '/' + OutputDir
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

################################################################
# Load input file
sFileName = Base + '/' + Company + '/' + InputDir + '/' + InputFileName
print('###########')
print('Loading :', sFileName)

Warehouse = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")

################################################################
# Rename columns
sColumns = {
    'X1': 'Country',
    'X2': 'PostCode',
    'X3': 'PlaceName',
    'X4': 'AreaName',
    'X5': 'AreaCode',
    'X10': 'Latitude',
    'X11': 'Longitude'
}

Warehouse.rename(columns=sColumns, inplace=True)
WarehouseGood = Warehouse

################################################################
# Save processed file
sFileName = sFileDir + '/' + OutputFileName
WarehouseGood.to_csv(sFileName, index=False)

#################################################################
print('### Done!! ############################################')
#################################################################
