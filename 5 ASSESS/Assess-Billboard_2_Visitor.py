################################################################
# -*- coding: utf-8 -*-
################################################################
import networkx as nx
import sys
import os
import sqlite3 as sq
import pandas as pd
from geopy.distance import vincenty
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
sTable = 'Assess_BillboardVisitorData'
sOutputFileName = 'Assess-DE-Billboard-Visitor.gml'
################################################################

sDataBaseDir = Base + '/' + Company + '/02-Assess/SQLite'
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)
################################################################

sDatabaseName = sDataBaseDir + '/krennwallner.db'
conn = sq.connect(sDatabaseName)
################################################################

print('################')
print('Loading :', sDatabaseName, ' Table:', sTable)

sSQL = "select " \
       " A.BillboardCountry," \
       " A.BillboardPlaceName," \
       " ROUND(A.BillboardLatitude,3) AS BillboardLatitude, " \
       " ROUND(A.BillboardLongitude,3) AS BillboardLongitude," \
       " (CASE WHEN A.BillboardLatitude < 0 THEN " \
       "  'S' || ROUND(ABS(A.BillboardLatitude),3) " \
       " ELSE " \
       "  'N' || ROUND(ABS(A.BillboardLatitude),3) END) AS sBillboardLatitude," \
       " (CASE WHEN A.BillboardLongitude < 0 THEN " \
       "  'W' || ROUND(ABS(A.BillboardLongitude),3) " \
       " ELSE " \
       "  'E' || ROUND(ABS(A.BillboardLongitude),3) END) AS sBillboardLongitude," \
       " A.VisitorCountry," \
       " A.VisitorPlaceName," \
       " ROUND(A.VisitorLatitude,3) AS VisitorLatitude, " \
       " ROUND(A.VisitorLongitude,3) AS VisitorLongitude," \
       " (CASE WHEN A.VisitorLatitude < 0 THEN " \
       "  'S' || ROUND(ABS(A.VisitorLatitude),3) " \
       " ELSE " \
       "  'N' || ROUND(ABS(A.VisitorLatitude),3) END) AS sVisitorLatitude," \
       " (CASE WHEN A.VisitorLongitude < 0 THEN " \
       "  'W' || ROUND(ABS(A.VisitorLongitude),3) " \
       " ELSE " \
       "  'E' || ROUND(ABS(A.VisitorLongitude),3) END) AS sVisitorLongitude," \
       " A.VisitorYearRate " \
       " from Assess_BillboardVistorsData AS A;"

BillboardVistorsData = pd.read_sql_query(sSQL, conn)
print('################')
################################################################

BillboardVistorsData['Distance'] = BillboardVistorsData.apply(
    lambda row: round(
        vincenty(
            (row['BillboardLatitude'], row['BillboardLongitude']),
            (row['VisitorLatitude'], row['VisitorLongitude'])
        ).miles,
        4
    ),
    axis=1
)
################################################################

G = nx.Graph()
################################################################

for i in range(BillboardVistorsData.shape[0]):

    sNode0 = 'MediaHub-' + BillboardVistorsData['BillboardCountry'][i]

    sNode1 = 'B-' + BillboardVistorsData['sBillboardLatitude'][i] + '-' + BillboardVistorsData['sBillboardLongitude'][i]
    G.add_node(
        sNode1,
        Nodetype='Billboard',
        Country=BillboardVistorsData['BillboardCountry'][i],
        PlaceName=BillboardVistorsData['BillboardPlaceName'][i],
        Latitude=round(BillboardVistorsData['BillboardLatitude'][i], 3),
        Longitude=round(BillboardVistorsData['BillboardLongitude'][i], 3)
    )

    sNode2 = 'M-' + BillboardVistorsData['sVisitorLatitude'][i] + '-' + BillboardVistorsData['sVisitorLongitude'][i]
    G.add_node(
        sNode2,
        Nodetype='Mobile',
        Country=BillboardVistorsData['VisitorCountry'][i],
        PlaceName=BillboardVistorsData['VisitorPlaceName'][i],
        Latitude=round(BillboardVistorsData['VisitorLatitude'][i], 3),
        Longitude=round(BillboardVistorsData['VisitorLongitude'][i], 3)
    )

    print('Link Media Hub :', sNode0, ' to Billboard : ', sNode1)
    G.add_edge(sNode0, sNode1)

    print('Link Post Code :', sNode1, ' to GPS : ', sNode2)
    G.add_edge(sNode1, sNode2, distance=round(BillboardVistorsData['Distance'][i]))

################################################################
print('################################')
print("Nodes of graph: ", nx.number_of_nodes(G))
print("Edges of graph: ", nx.number_of_edges(G))
print('################################')
################################################################

sFileDir = Base + '/' + Company + '/02-Assess/01-EDS/02-Python'
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)
################################################################

sFileName = sFileDir + '/' + sOutputFileName
print('################################')
print('Storing :', sFileName)
print('################################')

nx.write_gml(G, sFileName)
sFileName = sFileName + '.gz'
nx.write_gml(G, sFileName)
################################################################
print('### Done!! ############################################')
################################################################
