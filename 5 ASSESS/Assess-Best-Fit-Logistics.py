################################################################
# -*- coding: utf-8 -*-
################################################################
import sys
import os
import pandas as pd
import networkx as nx
from geopy.distance import vincenty
import sqlite3 as sq
from pandas.io import sql
################################################################

if sys.platform == 'linux':
    Base = os.path.expanduser('~') + '/VKHCG'
else:
    Base = 'C:/VKHCG'

print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')

################################################################
Company = '03-Hillman'
InputDir = '01-Retrieve/01-EDS/01-R'
InputFileName = 'Retrieve_All_Countries.csv'
EDSDir = '02-Assess/01-EDS'
OutputDir = EDSDir + '/02-Python'
OutputFileName = 'Assess_Best_Logistics.gml'
################################################################

sFileDir = Base + '/' + Company + '/' + EDSDir
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

################################################################
sFileDir = Base + '/' + Company + '/' + OutputDir
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

################################################################
sDataBaseDir = Base + '/' + Company + '/02-Assess/SQLite'
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)

################################################################
sDatabaseName = sDataBaseDir + '/Hillman.db'
conn = sq.connect(sDatabaseName)

################################################################
sFileName = Base + '/' + Company + '/' + InputDir + '/' + InputFileName
print('###########')
print('Loading :', sFileName)
Warehouse = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")

################################################################
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
RoutePointsCountry = pd.DataFrame(
    WarehouseGood.groupby(['Country'])[['Latitude', 'Longitude']].mean()
)

print('################')
sTable = 'Assess_RoutePointsCountry'
print('Storing :', sDatabaseName, ' Table:', sTable)
RoutePointsCountry.to_sql(sTable, conn, if_exists="replace")
print('################')

################################################################
RoutePointsPostCode = pd.DataFrame(
    WarehouseGood.groupby(['Country', 'PostCode'])[['Latitude', 'Longitude']].mean()
)

print('################')
sTable = 'Assess_RoutePointsPostCode'
print('Storing :', sDatabaseName, ' Table:', sTable)
RoutePointsPostCode.to_sql(sTable, conn, if_exists="replace")
print('################')

################################################################
RoutePointsPlaceName = pd.DataFrame(
    WarehouseGood.groupby(['Country', 'PostCode', 'PlaceName'])[['Latitude', 'Longitude']].mean()
)

print('################')
sTable = 'Assess_RoutePointsPlaceName'
print('Storing :', sDatabaseName, ' Table:', sTable)
RoutePointsPlaceName.to_sql(sTable, conn, if_exists="replace")
print('################')

################################################################
### Fit Country to Country
################################################################
print('################')
sView = 'Assess_RouteCountries'
print('Creating :', sDatabaseName, ' View:', sView)

sSQL = f"DROP VIEW IF EXISTS {sView};"
sql.execute(sSQL, conn)

sSQL = (
    "CREATE VIEW " + sView + " AS"
    " SELECT DISTINCT"
    "   S.Country AS SourceCountry,"
    "   S.Latitude AS SourceLatitude,"
    "   S.Longitude AS SourceLongitude,"
    "   T.Country AS TargetCountry,"
    "   T.Latitude AS TargetLatitude,"
    "   T.Longitude AS TargetLongitude"
    " FROM"
    "   Assess_RoutePointsCountry AS S,"
    "   Assess_RoutePointsCountry AS T"
    " WHERE S.Country <> T.Country"
    " AND S.Country in ('GB','DE','BE','AU','US','IN')"
    " AND T.Country in ('GB','DE','BE','AU','US','IN');"
)
sql.execute(sSQL, conn)

print('################')
print('Loading :', sDatabaseName, ' Table:', sView)

sSQL = "SELECT * FROM " + sView + ";"
RouteCountries = pd.read_sql_query(sSQL, conn)

RouteCountries['Distance'] = RouteCountries.apply(
    lambda row: round(
        vincenty(
            (row['SourceLatitude'], row['SourceLongitude']),
            (row['TargetLatitude'], row['TargetLongitude'])
        ).miles, 4
    ),
    axis=1
)

print(RouteCountries.head(5))

################################################################
### Fit Country to Post Code
################################################################
print('################')
sView = 'Assess_RoutePostCode'
print('Creating :', sDatabaseName, ' View:', sView)
sSQL = f"DROP VIEW IF EXISTS {sView};"
sql.execute(sSQL, conn)

sSQL = (
    "CREATE VIEW " + sView + " AS"
    " SELECT DISTINCT"
    "   S.Country AS SourceCountry,"
    "   S.Latitude AS SourceLatitude,"
    "   S.Longitude AS SourceLongitude,"
    "   T.Country AS TargetCountry,"
    "   T.PostCode AS TargetPostCode,"
    "   T.Latitude AS TargetLatitude,"
    "   T.Longitude AS TargetLongitude"
    " FROM"
    "   Assess_RoutePointsCountry AS S,"
    "   Assess_RoutePointsPostCode AS T"
    " WHERE S.Country = T.Country"
    " AND S.Country in ('GB','DE','BE','AU','US','IN')"
    " AND T.Country in ('GB','DE','BE','AU','US','IN');"
)
sql.execute(sSQL, conn)

print('################')
print('Loading :', sDatabaseName, ' Table:', sView)

sSQL = "SELECT * FROM " + sView + ";"
RoutePostCode = pd.read_sql_query(sSQL, conn)

RoutePostCode['Distance'] = RoutePostCode.apply(
    lambda row: round(
        vincenty(
            (row['SourceLatitude'], row['SourceLongitude']),
            (row['TargetLatitude'], row['TargetLongitude'])
        ).miles, 4
    ),
    axis=1
)

print(RoutePostCode.head(5))

################################################################
### Fit Post Code to Place Name
################################################################
print('################')
sView = 'Assess_RoutePlaceName'
print('Creating :', sDatabaseName, ' View:', sView)

sSQL = f"DROP VIEW IF EXISTS {sView};"
sql.execute(sSQL, conn)

sSQL = (
    "CREATE VIEW " + sView + " AS"
    " SELECT DISTINCT"
    "   S.Country AS SourceCountry,"
    "   S.PostCode AS SourcePostCode,"
    "   S.Latitude AS SourceLatitude,"
    "   S.Longitude AS SourceLongitude,"
    "   T.Country AS TargetCountry,"
    "   T.PostCode AS TargetPostCode,"
    "   T.PlaceName AS TargetPlaceName,"
    "   T.Latitude AS TargetLatitude,"
    "   T.Longitude AS TargetLongitude"
    " FROM"
    "   Assess_RoutePointsPostCode AS S,"
    "   Assess_RoutePointsPlaceName AS T"
    " WHERE"
    "   S.Country = T.Country"
    " AND S.PostCode = T.PostCode"
    " AND S.Country in ('GB','DE','BE','AU','US','IN')"
    " AND T.Country in ('GB','DE','BE','AU','US','IN');"
)
sql.execute(sSQL, conn)

print('################')
print('Loading :', sDatabaseName, ' Table:', sView)

sSQL = "SELECT * FROM " + sView + ";"
RoutePlaceName = pd.read_sql_query(sSQL, conn)

RoutePlaceName['Distance'] = RoutePlaceName.apply(
    lambda row: round(
        vincenty(
            (row['SourceLatitude'], row['SourceLongitude']),
            (row['TargetLatitude'], row['TargetLongitude'])
        ).miles, 4
    ),
    axis=1
)

print(RoutePlaceName.head(5))

################################################################
G = nx.Graph()

################################################################
print('Countries:', RouteCountries.shape)
for i in range(RouteCountries.shape[0]):
    sNode0 = 'C-' + RouteCountries['SourceCountry'][i]
    G.add_node(
        sNode0,
        Nodetype='Country',
        Country=RouteCountries['SourceCountry'][i],
        Latitude=round(RouteCountries['SourceLatitude'][i], 4),
        Longitude=round(RouteCountries['SourceLongitude'][i], 4)
    )

    sNode1 = 'C-' + RouteCountries['TargetCountry'][i]
    G.add_node(
        sNode1,
        Nodetype='Country',
        Country=RouteCountries['TargetCountry'][i],
        Latitude=round(RouteCountries['TargetLatitude'][i], 4),
        Longitude=round(RouteCountries['TargetLongitude'][i], 4)
    )

    G.add_edge(sNode0, sNode1, distance=round(RouteCountries['Distance'][i], 3))

################################################################
print('Post Code:', RoutePostCode.shape)
for i in range(RoutePostCode.shape[0]):
    sNode0 = 'C-' + RoutePostCode['SourceCountry'][i]
    G.add_node(
        sNode0,
        Nodetype='Country',
        Country=RoutePostCode['SourceCountry'][i],
        Latitude=round(RoutePostCode['SourceLatitude'][i], 4),
        Longitude=round(RoutePostCode['SourceLongitude'][i], 4)
    )

    sNode1 = 'P-' + RoutePostCode['TargetPostCode'][i] + '-' + RoutePostCode['TargetCountry'][i]
    G.add_node(
        sNode1,
        Nodetype='PostCode',
        Country=RoutePostCode['TargetCountry'][i],
        PostCode=RoutePostCode['TargetPostCode'][i],
        Latitude=round(RoutePostCode['TargetLatitude'][i], 4),
        Longitude=round(RoutePostCode['TargetLongitude'][i], 4)
    )

    G.add_edge(sNode0, sNode1, distance=round(RoutePostCode['Distance'][i], 3))

################################################################
print('Place Name:', RoutePlaceName.shape)
for i in range(RoutePlaceName.shape[0]):
    sNode0 = 'P-' + RoutePlaceName['TargetPostCode'][i] + '-' + RoutePlaceName['TargetCountry'][i]
    G.add_node(
        sNode0,
        Nodetype='PostCode',
        Country=RoutePlaceName['SourceCountry'][i],
        PostCode=RoutePlaceName['TargetPostCode'][i],
        Latitude=round(RoutePlaceName['SourceLatitude'][i], 4),
        Longitude=round(RoutePlaceName['SourceLongitude'][i], 4)
    )

    sNode1 = (
        'L-' + RoutePlaceName['TargetPlaceName'][i]
        + '-' + RoutePlaceName['TargetPostCode'][i]
        + '-' + RoutePlaceName['TargetCountry'][i]
    )

    G.add_node(
        sNode1,
        Nodetype='PlaceName',
        Country=RoutePlaceName['TargetCountry'][i],
        PostCode=RoutePlaceName['TargetPostCode'][i],
        PlaceName=RoutePlaceName['TargetPlaceName'][i],
        Latitude=round(RoutePlaceName['TargetLatitude'][i], 4),
        Longitude=round(RoutePlaceName['TargetLongitude'][i], 4)
    )

    G.add_edge(sNode0, sNode1, distance=round(RoutePlaceName['Distance'][i], 3))

################################################################
sFileName = sFileDir + '/' + OutputFileName
print('################################')
print('Storing :', sFileName)
print('################################')

nx.write_gml(G, sFileName)
nx.write_gml(G, sFileName + '.gz')

################################################################
print('################################')
print('Path:', nx.shortest_path(G, source='P-SW1-GB', target='P-01001-US', weight='distance'))
print('Path length:', nx.shortest_path_length(G, source='P-SW1-GB', target='P-01001-US', weight='distance'))
print('Path length (1):', nx.shortest_path_length(G, source='P-SW1-GB', target='C-GB', weight='distance'))
print('Path length (2):', nx.shortest_path_length(G, source='C-GB', target='C-US', weight='distance'))
print('Path length (3):', nx.shortest_path_length(G, source='C-US', target='P-01001-US', weight='distance'))
print('################################')

print('Routes from P-SW1-GB < 2: ', nx.single_source_shortest_path(G, source='P-SW1-GB', cutoff=1))
print('Routes from P-01001-US < 2: ', nx.single_source_shortest_path(G, source='P-01001-US', cutoff=1))
print('################################')

################################################################
print('################')
print('Vacuum Database')
sql.execute("VACUUM;", conn)
print('################')

################################################################
print('### Done!! ############################################')
################################################################
