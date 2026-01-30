import sys
import os
import pandas as pd
import sqlite3 as sq
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
################################################################
Base = 'C:/VKHCG'
print('################################')
print('Working Base :', Base, ' using ', sys.platform)
print('################################')
################################################################
Company = '01-Vermeulen'
################################################################
sDataBaseDir = Base + '/' + Company + '/04-Transform/SQLite'
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)
################################################################
sDatabaseName = sDataBaseDir + '/Vermeulen.db'
conn1 = sq.connect(sDatabaseName)
################################################################
sDataVaultDir = Base + '/88-DV'
if not os.path.exists(sDataVaultDir):
    os.makedirs(sDataVaultDir)
################################################################
sDatabaseName = sDataVaultDir + '/datavault.db'
conn2 = sq.connect(sDatabaseName)
################################################################
sDataWarehouseDir = Base + '/99-DW'
if not os.path.exists(sDataWarehouseDir):
    os.makedirs(sDataWarehouseDir)
################################################################
sDatabaseName = sDataWarehouseDir + '/datawarehouse.db'
conn3 = sq.connect(sDatabaseName)
################################################################

t = 0
tMax = ((300 - 100) / 10) * ((300 - 30) / 5)

PersonFrame = None

for heightSelect in range(100, 300, 10):
    for weightSelect in range(30, 300, 5):

        height = round(heightSelect / 100, 3)
        weight = int(weightSelect)
        bmi = weight / (height * height)

        if bmi <= 18.5:
            BMI_Result = 1
        elif 18.5 < bmi < 25:
            BMI_Result = 2
        elif 25 < bmi < 30:
            BMI_Result = 3
        elif bmi > 30:
            BMI_Result = 4
        else:
            BMI_Result = 0

        PersonLine = [
            ('PersonID', [str(t)]),
            ('Height', [height]),
            ('Weight', [weight]),
            ('bmi', [bmi]),
            ('Indicator', [BMI_Result])
        ]

        t += 1
        print('Row:', t, 'of', tMax)

        if t == 1:
            PersonFrame = pd.DataFrame.from_items(PersonLine)
        else:
            PersonRow = pd.DataFrame.from_items(PersonLine)
            PersonFrame = PersonFrame.append(PersonRow)

################################################################
DimPerson = PersonFrame
DimPersonIndex = DimPerson.set_index(['PersonID'], inplace=False)
################################################################

# Store in Transform DB
sTable = 'Transform-BMI'
print('\n#################################')
print('Storing :', sDatabaseName, '\n Table:', sTable)
print('\n#################################')
DimPersonIndex.to_sql(sTable, conn1, if_exists="replace")
################################################################

# Store in DV
sTable = 'Person-Satellite-BMI'
print('\n#################################')
print('Storing :', sDatabaseName, '\n Table:', sTable)
print('\n#################################')
DimPersonIndex.to_sql(sTable, conn2, if_exists="replace")
################################################################

# Store in DW
sTable = 'Dim-BMI'
print('\n#################################')
print('Storing :', sDatabaseName, '\n Table:', sTable)
print('\n#################################')
DimPersonIndex.to_sql(sTable, conn3, if_exists="replace")
################################################################

# Plot BMI Curve
fig = plt.figure()

PlotPerson = DimPerson[DimPerson['Indicator'] == 1]
plt.plot(PlotPerson['Height'], PlotPerson['Weight'], ".")

PlotPerson = DimPerson[DimPerson['Indicator'] == 2]
plt.plot(PlotPerson['Height'], PlotPerson['Weight'], "o")

PlotPerson = DimPerson[DimPerson['Indicator'] == 3]
plt.plot(PlotPerson['Height'], PlotPerson['Weight'], "+")

PlotPerson = DimPerson[DimPerson['Indicator'] == 4]
plt.plot(PlotPerson['Height'], PlotPerson['Weight'], "^")

plt.axis('tight')
plt.title("BMI Curve")
plt.xlabel("Height (meters)")
plt.ylabel("Weight (kg)")
plt.plot()

# Load diabetes dataset
diabetes = datasets.load_diabetes()

# Use only one feature
diabetes_X = diabetes.data[:, np.newaxis, 2]

diabetes_X_train = diabetes_X[:-30]
diabetes_X_test = diabetes_X[-50:]

diabetes_y_train = diabetes.target[:-30]
diabetes_y_test = diabetes.target[-50:]

regr = linear_model.LinearRegression()
regr.fit(diabetes_X_train, diabetes_y_train)

diabetes_y_pred = regr.predict(diabetes_X_test)

print('Coefficients: \n', regr.coef_)
print("Mean squared error: %.2f" % mean_squared_error(diabetes_y_test, diabetes_y_pred))
print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

plt.scatter(diabetes_X_test, diabetes_y_test, color='black')
plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())
plt.axis('tight')
plt.title("Diabetes")
plt.xlabel("BMI")
plt.ylabel("Age")
plt.show()
