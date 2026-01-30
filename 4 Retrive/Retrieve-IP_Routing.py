################################################################
# -*- coding: utf-8 -*-
################################################################
import sys
import os
import pandas as pd
from math import radians, cos, sin, asin, sqrt
################################################################
def haversine(lon1, lat1, lon2, lat2, stype):
    """Calculate the great circle distance between two points on Earth."""
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    # Choose radius
    r = 6371 if stype == 'km' else 3956  # km or miles
    return round(c * r, 3)
################################################################
Base = 'C:/VKHCG'
################################################################
sFileName = Base + '/01-Vermeulen/00-RawData/IP_DATA_CORE.csv'
print('Loading:', sFileName)
IP_DATA_ALL = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],
    encoding="latin-1"
)
################################################################
sFileDir = Base + '/01-Vermeulen/01-Retrieve/01-EDS/02-Python'
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)
################################################################
# ✅ Fix: Use .copy() to avoid SettingWithCopyWarning
IP_DATA = IP_DATA_ALL.drop_duplicates(subset=None, keep='first', inplace=False).copy()
IP_DATA.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

IP_DATA1 = IP_DATA.copy()
IP_DATA1.insert(0, 'K', 1)
IP_DATA2 = IP_DATA1.copy()
print(IP_DATA1.shape)
################################################################
# Cross join to compute all pairwise distances
IP_CROSS = pd.merge(right=IP_DATA1, left=IP_DATA2, on='K')
IP_CROSS.drop('K', axis=1, inplace=True)
# Rename columns for clarity
IP_CROSS.rename(columns={
    'Longitude_x': 'Longitude_from',
    'Longitude_y': 'Longitude_to',
    'Latitude_x': 'Latitude_from',
    'Latitude_y': 'Latitude_to',
    'Place_Name_x': 'Place_Name_from',
    'Place_Name_y': 'Place_Name_to',
    'Country_x': 'Country_from',
    'Country_y': 'Country_to'
}, inplace=True)
################################################################
# Calculate distances in kilometers and miles
################################################################
IP_CROSS['DistanceBetweenKilometers'] = IP_CROSS.apply(
    lambda row: haversine(
        row['Longitude_from'],
        row['Latitude_from'],
        row['Longitude_to'],
        row['Latitude_to'],
        'km'
    ), axis=1
)
IP_CROSS['DistanceBetweenMiles'] = IP_CROSS.apply(
    lambda row: haversine(
        row['Longitude_from'],
        row['Latitude_from'],
        row['Longitude_to'],
        row['Latitude_to'],
        'miles'
    ), axis=1
)
################################################################
print(IP_CROSS.shape)
sFileName2 = sFileDir + '/Retrieve_IP_Routing.csv'
IP_CROSS.to_csv(sFileName2, index=False, encoding="latin-1")
################################################################
print('### Done!! ############################################')
################################################################
