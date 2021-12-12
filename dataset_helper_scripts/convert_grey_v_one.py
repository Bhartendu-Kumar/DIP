

#importing libraries
import cv2

import os ,glob

from os import listdir ,makedirs , walk

from os.path import isfile ,join
import sys

def convert_this_directory(path , dstpath):

    # print("in directory {}".format(path))
    # print("dest directory {}".format(dstpath))

    try:
        makedirs(dstpath)
    except:
        print("Directory already exist, images will be written in same folder")
    # Folder won't used

    files = list(filter(lambda f: isfile(join(path, f)), listdir(path)))

    # print("files are {}".format(files))
    name = 0

    for image in files:

        try:
            img = cv2.imread(os.path.join(path, image))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            dstPath = join(dstpath, image)
            cv2.imwrite(dstPath, gray)
        except:
            print("{} is not converted".format(image))

    # for fil in glob.glob("*.jpg"):
    #
    #     try:
    #         image = cv2.imread(fil)
    #         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to greyscale
    #         cv2.imwrite(os.path.join(dstpath ,fil) ,gray_image)
    #     except:
    #         print('{} is not converted'.format(fil))
    #

#this converts all subfolders in a directory recursively
def convert_all_subdirectories(path , dstpath):
    #
    # print("in directory {}".format(path))
    sub_directories =  list(filter(lambda f: os.path.isdir(join(path ,f)), listdir(path)))

    # print("sub directories are {}".format(sub_directories))

    #converting images in this directory
    convert_this_directory(path , dstpath)
    #now iterating over subdirectories
    for sub_directory in sub_directories:
        #converting images in subdirectories
        convert_all_subdirectories(os.path.join(path , sub_directory) , os.path.join(dstpath , sub_directory))


def convert_to_grey():
    #getting command line arguments
    path = sys.argv[1]
    dstpath = sys.argv[2]



    if os.path.isdir(path):
        convert_all_subdirectories(path , dstpath)
    else:
        print("Path is not a directory")


if __name__ == '__main__':

    convert_to_grey()
