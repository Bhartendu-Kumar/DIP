

import cv2
import glob, os, errno

# Replace mydir with the directory you want
mydir = r'folder_src'
dstpath = r'folder_dest' # Destination Folder

#check if directory exist, if not create it
try:
    os.makedirs(dstpath)
except OSError as e:
    if e.errno == errno.EEXIST:
        raise
for fil in glob.glob("*.jpg"):
    image = cv2.imread(fil)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to greyscale
    cv2.imwrite(os.path.join(dstpath,fil),gray_image) # write to location with same name

