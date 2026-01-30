#=============================================================
# Utility Start Movie to HORUS (Part 1)
#=============================================================
import cv2
import os
import shutil
#=============================================================
sInputFileName = 'C:/VKHCG/05-DS/9999-Data/dog.mp4'
sDataBaseDir = 'C:/VKHCG/05-DS/9999-Data/temp'
#=============================================================
# Remove old folder if exists
if os.path.exists(sDataBaseDir):
    shutil.rmtree(sDataBaseDir)
os.makedirs(sDataBaseDir)
print('=====================================================')
print('Start Movie to Frames')
print('=====================================================')
#=============================================================
vidcap = cv2.VideoCapture(sInputFileName)
success, image = vidcap.read()
count = 0

while success:
    sFrame = sDataBaseDir + str('/dog-frame-' + str(format(count, '04d')) + '.jpg')
    cv2.imwrite(sFrame, image)
    print('Extracted: ', sFrame)

    # Check if file was saved properly
    if os.path.getsize(sFrame) == 0:
        count += -1
        os.remove(sFrame)
        print('Removed: ', sFrame)

    if cv2.waitKey(10) == 27:  # Exit if Escape is hit
        break

    success, image = vidcap.read()
    count += 1
#=============================================================
print('=====================================================')
print('Generated :', count, 'Frames')
print('=====================================================')
print('Movie to Frames HORUS - Done')
print('=====================================================')
print('# Utility done')
#=============================================================
