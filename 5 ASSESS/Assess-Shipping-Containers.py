################################################################
# -*- coding: utf-8 -*-
################################################################
import sys
import os
import pandas as pd
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
InputDir = '01-Retrieve/01-EDS/02-Python'
InputFileName1 = 'Retrieve_Product.csv'
InputFileName2 = 'Retrieve_Box.csv'
InputFileName3 = 'Retrieve_Container.csv'
EDSDir = '02-Assess/01-EDS'
OutputDir = EDSDir + '/02-Python'
OutputFileName = 'Assess_Shipping_Containers.csv'
################################################################

sFileDir = Base + '/' + Company + '/' + EDSDir
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

sFileDir = Base + '/' + Company + '/' + OutputDir
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

sDataBaseDir = Base + '/' + Company + '/02-Assess/SQLite'
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)

sDatabaseName = sDataBaseDir + '/hillman.db'
conn = sq.connect(sDatabaseName)

################################################################
### Import Product Data
################################################################
sFileName = Base + '/' + Company + '/' + InputDir + '/' + InputFileName1
print('###########')
print('Loading :', sFileName)

ProductRawData = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    encoding="latin-1"
)
ProductRawData.drop_duplicates(subset=None, keep='first', inplace=True)
ProductRawData.index.name = 'IDNumber'
ProductData = ProductRawData[ProductRawData.Length <= 0.5].head(10)

print('Loaded Product :', ProductData.columns.values)
print('################################')

print('################')
sTable = 'Assess_Product'
print('Storing :', sDatabaseName, ' Table:', sTable)
ProductData.to_sql(sTable, conn, if_exists="replace")
print('################')

print(ProductData.head())
print('################################')
print('Rows : ', ProductData.shape[0])
print('################################')

################################################################
### Import Box Data
################################################################
sFileName = Base + '/' + Company + '/' + InputDir + '/' + InputFileName2
print('###########')
print('Loading :', sFileName)

BoxRawData = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    encoding="latin-1"
)
BoxRawData.drop_duplicates(subset=None, keep='first', inplace=True)
BoxRawData.index.name = 'IDNumber'
BoxData = BoxRawData[BoxRawData.Length <= 1].head(1000)

print('Loaded Product :', BoxData.columns.values)
print('################################')

print('################')
sTable = 'Assess_Box'
print('Storing :', sDatabaseName, ' Table:', sTable)
BoxData.to_sql(sTable, conn, if_exists="replace")
print('################')

print(BoxData.head())
print('################################')
print('Rows : ', BoxData.shape[0])
print('################################')

################################################################
### Import Container Data
################################################################
sFileName = Base + '/' + Company + '/' + InputDir + '/' + InputFileName3
print('###########')
print('Loading :', sFileName)

ContainerRawData = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    encoding="latin-1"
)
ContainerRawData.drop_duplicates(subset=None, keep='first', inplace=True)
ContainerRawData.index.name = 'IDNumber'
ContainerData = ContainerRawData[ContainerRawData.Length <= 2].head(10)

print('Loaded Product :', ContainerData.columns.values)
print('################################')

print('################')
sTable = 'Assess_Container'
print('Storing :', sDatabaseName, ' Table:', sTable)
ContainerData.to_sql(sTable, conn, if_exists="replace")
print('################')

print(ContainerData.head())
print('################################')
print('Rows : ', ContainerData.shape[0])
print('################################')

################################################################
### Fit Product in Box
################################################################
print('################')
sView = 'Assess_Product_in_Box'
print('Creating :', sDatabaseName, ' View:', sView)

sSQL = "DROP VIEW IF EXISTS " + sView + ";"
sql.execute(sSQL, conn)

sSQL = "CREATE VIEW " + sView + " AS" \
       " SELECT" \
       " P.UnitNumber AS ProductNumber," \
       " B.UnitNumber AS BoxNumber," \
       " (B.Thickness * 1000) AS PackSafeCode," \
       " (B.BoxVolume - P.ProductVolume) AS PackFoamVolume," \
       " ((B.Length*10) * (B.Width*10) * (B.Height*10)) * 167 AS Air_Dimensional_Weight," \
       " ((B.Length*10) * (B.Width*10) * (B.Height*10)) * 333 AS Road_Dimensional_Weight," \
       " ((B.Length*10) * (B.Width*10) * (B.Height*10)) * 1000 AS Sea_Dimensional_Weight," \
       " P.Length AS Product_Length," \
       " P.Width AS Product_Width," \
       " P.Height AS Product_Height," \
       " P.ProductVolume AS Product_cm_Volume," \
       " ((P.Length*10) * (P.Width*10) * (P.Height*10)) AS Product_ccm_Volume," \
       " (B.Thickness * 0.95) AS Minimum_Pack_Foam," \
       " (B.Thickness * 1.05) AS Maximum_Pack_Foam," \
       " B.Length - (B.Thickness * 1.10) AS Minimum_Product_Box_Length," \
       " B.Length - (B.Thickness * 0.95) AS Maximum_Product_Box_Length," \
       " B.Width - (B.Thickness * 1.10) AS Minimum_Product_Box_Width," \
       " B.Width - (B.Thickness * 0.95) AS Maximum_Product_Box_Width," \
       " B.Height - (B.Thickness * 1.10) AS Minimum_Product_Box_Height," \
       " B.Height - (B.Thickness * 0.95) AS Maximum_Product_Box_Height," \
       " B.Length AS Box_Length," \
       " B.Width AS Box_Width," \
       " B.Height AS Box_Height," \
       " B.BoxVolume AS Box_cm_Volume," \
       " ((B.Length*10) * (B.Width*10) * (B.Height*10)) AS Box_ccm_Volume," \
       " (2 * B.Length * B.Width) + (2 * B.Length * B.Height) + (2 * B.Width * B.Height) AS Box_sqm_Area," \
       " ((B.Length*10) * (B.Width*10) * (B.Height*10)) *  3.5 AS Box_A_Max_Kg_Weight," \
       " ((B.Length*10) * (B.Width*10) * (B.Height*10)) *  7.7 AS Box_B_Max_Kg_Weight," \
       " ((B.Length*10) * (B.Width*10) * (B.Height*10)) * 10.0 AS Box_C_Max_Kg_Weight" \
       " FROM Assess_Product as P, Assess_Box as B" \
       " WHERE" \
       " P.Length >= (B.Length - (B.Thickness * 1.10)) AND" \
       " P.Width >= (B.Width - (B.Thickness * 1.10)) AND" \
       " P.Height >= (B.Height - (B.Thickness * 1.10)) AND" \
       " P.Length <= (B.Length - (B.Thickness * 0.95)) AND" \
       " P.Width <= (B.Width - (B.Thickness * 0.95)) AND" \
       " P.Height <= (B.Height - (B.Thickness * 0.95)) AND" \
       " (B.Height - B.Thickness) >= 0 AND" \
       " (B.Width - B.Thickness) >= 0 AND" \
       " (B.Height - B.Thickness) >= 0 AND" \
       " B.BoxVolume >= P.ProductVolume;"

sql.execute(sSQL, conn)

################################################################
### Fit Box in Pallet
################################################################
t = 0
for l in range(2, 8):
    for w in range(2, 8):
        for h in range(4):
            t += 1
            PalletLine = [
                ('IDNumber', [t]),
                ('ShipType', ['Pallet']),
                ('UnitNumber', ('L-' + format(t, "06d"))),
                ('Box_per_Length', (format(2 ** l, "4d"))),
                ('Box_per_Width', (format(2 ** w, "4d"))),
                ('Box_per_Height', (format(2 ** h, "4d")))
            ]

            if t == 1:
                PalletFrame = pd.DataFrame.from_items(PalletLine)
            else:
                PalletRow = pd.DataFrame.from_items(PalletLine)
                PalletFrame = PalletFrame.append(PalletRow)

PalletFrame.set_index(['IDNumber'], inplace=True)

print('################################')
print('Rows : ', PalletFrame.shape[0])
print('################################')

################################################################
### Fit Box on Pallet
################################################################
print('################')
sView = 'Assess_Box_on_Pallet'
print('Creating :', sDatabaseName, ' View:', sView)

sSQL = "DROP VIEW IF EXISTS " + sView + ";"
sql.execute(sSQL, conn)

sSQL = "CREATE VIEW " + sView + " AS" \
       " SELECT DISTINCT" \
       " P.UnitNumber AS PalletNumber," \
       " B.UnitNumber AS BoxNumber," \
       " round(B.Length*P.Box_per_Length,3) AS Pallet_Length," \
       " round(B.Width*P.Box_per_Width,3) AS Pallet_Width," \
       " round(B.Height*P.Box_per_Height,3) AS Pallet_Height," \
       " P.Box_per_Length * P.Box_per_Width * P.Box_per_Height AS Pallet_Boxes" \
       " FROM Assess_Box as B, Assess_Pallet as P" \
       " WHERE" \
       " round(B.Length*P.Box_per_Length,3) <= 20 AND" \
       " round(B.Width*P.Box_per_Width,3) <= 9 AND" \
       " round(B.Height*P.Box_per_Height,3) <= 5;"

sql.execute(sSQL, conn)

################################################################
sTables = ['Assess_Product_in_Box', 'Assess_Box_on_Pallet']
for sTable in sTables:
    print('################')
    print('Loading :', sDatabaseName, ' Table:', sTable)

    sSQL = " SELECT * FROM " + sTable + ";"
    SnapShotData = pd.read_sql_query(sSQL, conn)

    print('################')
    sTableOut = sTable + '_SnapShot'
    print('Storing :', sDatabaseName, ' Table:', sTableOut)
    SnapShotData.to_sql(sTableOut, conn, if_exists="replace")
    print('################')

################################################################
### Fit Pallet in Container
################################################################
sTables = ['Length', 'Width', 'Height']

for sTable in sTables:
    sView = 'Assess_Pallet_in_Container_' + sTable
    print('Creating :', sDatabaseName, ' View:', sView)

    sSQL = "DROP VIEW IF EXISTS " + sView + ";"
    sql.execute(sSQL, conn)

    sSQL = "CREATE VIEW " + sView + " AS" \
           " SELECT DISTINCT" \
           " C.UnitNumber AS ContainerNumber," \
           " P.PalletNumber," \
           " P.BoxNumber," \
           " round(C." + sTable + "/P.Pallet_" + sTable + ",0) AS Pallet_per_" + sTable + "," \
           " round(C." + sTable + "/P.Pallet_" + sTable + ",0) * P.Pallet_Boxes AS Pallet_" + sTable + "_Boxes," \
           " P.Pallet_Boxes" \
           " FROM Assess_Container as C," \
           " Assess_Box_on_Pallet_SnapShot as P" \
           " WHERE" \
           " round(C.Length/P.Pallet_Length,0) > 0 AND" \
           " round(C.Width/P.Pallet_Width,0) > 0 AND" \
           " round(C.Height/P.Pallet_Height,0) > 0;"

    sql.execute(sSQL, conn)

    print('################')
    print('Loading :', sDatabaseName, ' Table:', sView)

    sSQL = " SELECT * FROM " + sView + ";"
    SnapShotData = pd.read_sql_query(sSQL, conn)

    print('################')
    sTableOut = sView + '_SnapShot'
    print('Storing :', sDatabaseName, ' Table:', sTableOut)

    SnapShotData.to_sql(sTableOut, conn, if_exists="replace")
    print('################')

################################################################
print('################')
sView = 'Assess_Pallet_in_Container'
print('Creating :', sDatabaseName, ' View:', sView)

sSQL = "DROP VIEW IF EXISTS " + sView + ";"
sql.execute(sSQL, conn)

sSQL = "CREATE VIEW " + sView + " AS" \
       " SELECT" \
       " CL.ContainerNumber," \
       " CL.PalletNumber," \
       " CL.BoxNumber," \
       " CL.Pallet_Boxes AS Boxes_per_Pallet," \
       " CL.Pallet_per_Length," \
       " CW.Pallet_per_Width," \
       " CH.Pallet_per_Height," \
       " CL.Pallet_Length_Boxes * CW.Pallet_Width_Boxes * CH.Pallet_Height_Boxes AS Container_Boxes" \
       " FROM Assess_Pallet_in_Container_Length_SnapShot as CL" \
       " JOIN Assess_Pallet_in_Container_Width_SnapShot as CW" \
       " ON CL.ContainerNumber = CW.ContainerNumber" \
       " AND CL.PalletNumber = CW.PalletNumber" \
       " AND CL.BoxNumber = CW.BoxNumber" \
       " JOIN Assess_Pallet_in_Container_Height_SnapShot as CH" \
       " ON CL.ContainerNumber = CH.ContainerNumber" \
       " AND CL.PalletNumber = CH.PalletNumber" \
       " AND CL.BoxNumber = CH.BoxNumber;"

sql.execute(sSQL, conn)

################################################################
sTables = ['Assess_Product_in_Box', 'Assess_Pallet_in_Container']

for sTable in sTables:
    print('################')
    print('Loading :', sDatabaseName, ' Table:', sTable)

    sSQL = " SELECT * FROM " + sTable + ";"
    PackData = pd.read_sql_query(sSQL, conn)

    print('################')
    print(PackData)
    print('################')
    print('################################')
    print('Rows : ', PackData.shape[0])
    print('################################')

    sFileName = sFileDir + '/' + sTable + '.csv'
    print(sFileName)
    PackData.to_csv(sFileName, index=False)

################################################################
print('### Done!! ############################################')
################################################################
