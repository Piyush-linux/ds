#################### Assess-Network-Routing-Customer.py ######################
import sys
import os
import pandas as pd
################################################################
pd.options.mode.chained_assignment = None
################################################################
Base = 'C:/VKHCG'
print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')
################################################################
sInputFileName = Base + '/01-Vermeulen/02-Assess/01-EDS/02-Python/Assess-Network-RoutingCustomer.csv'
################################################################
sOutputFileName = 'Assess-Network-Routing-Customer.gml'
Company = '01-Vermeulen'
################################################################
### Import Customer Network Routing Data
################################################################
sFileName = sInputFileName
print('################################')
print('Loading :', sFileName)
print('################################')
CustomerData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
print('Loaded Columns:', CustomerData.columns.values)
print('################################')
print(CustomerData.head())
print('################################')
print('### Done!! #####################')
print('################################')
################################################################
