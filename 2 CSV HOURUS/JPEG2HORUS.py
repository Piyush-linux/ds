# Utility Start Picture to HORUS =================================
# Standard Tools
#=============================================================
import imageio.v2 as imageio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Input Agreement ============================================
sInputFileName = 'C:/VKHCG/05-DS/9999-Data/Angus.jpg'

# Read the image (replace imread from scipy with imageio.imread)
InputData = imageio.imread(sInputFileName)

print('Input Data Values ===================================')
print('X: ', InputData.shape[0])
print('Y: ', InputData.shape[1])
print('Channels (RGB or RGBA): ', InputData.shape[2])
print('=====================================================')

# Processing Rules ===========================================
ProcessRawData = InputData.flatten()
y = InputData.shape[2] + 2
x = int(ProcessRawData.shape[0] / y)

ProcessData = pd.DataFrame(np.reshape(ProcessRawData, (x, y)))

if InputData.shape[2] == 4:
    sColumns = ['XAxis','YAxis','Red', 'Green', 'Blue','Alpha']
else:
    sColumns = ['XAxis','YAxis','Red', 'Green', 'Blue']

ProcessData.columns = sColumns
ProcessData.index.names = ['ID']


print('Rows: ', ProcessData.shape[0])
print('Columns :', ProcessData.shape[1])
print('=====================================================')
print('Process Data Values =================================')
print('=====================================================')

plt.imshow(InputData)
plt.show()
print('=====================================================')

# Output Agreement ===========================================
OutputData = ProcessData
print('Storing File')
sOutputFileName = 'C:/VKHCG/05-DS/9999-Data/HORUS-Picture.csv'
OutputData.to_csv(sOutputFileName, index=False)

print('=====================================================')
print('Picture to HORUS - Done')
print('=====================================================')
