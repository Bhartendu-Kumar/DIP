import sys

import cv2

import os ,glob

from os import listdir ,makedirs , walk

from os.path import isfile ,join

from PIL import Image

def convert_v1():
    path = 'folder_src' # Source Folder
    dstpath = 'folder_dest' # Destination Folder
    try:
        makedirs(dstpath)
    except:
        print ("Directory already exist, images will be written in same folder")
    # Folder won't used


    files = list(filter(lambda f: isfile(join(path ,f)), listdir(path)))

    for image in files:
        print("inside files")
        print(image)
        try:
            img = cv2.imread(os.path.join(path ,image))
            gray = cv2.cvtColor(img ,cv2.COLOR_BGR2GRAY)
            dstPath = join(dstpath ,image)

            # convert from openCV2 to PIL. Notice the COLOR_BGR2RGB which means that
            # the color is converted from BGR to RGB
            color_coverted = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(color_coverted).convert('L')
            pil_image.save(dstPath)

            # cv2.imwrite("yale/one.png" ,gray)
        except:
            print ("{} is not converted".format(image))
            print("in side except")
            print(image)
    for fil in glob.glob("*.jpg"):
        print("inside glob")
        print()
        image = cv2.imread(fil)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to greyscale
        cv2.imwrite(os.path.join(dstpath ,fil) ,gray_image)
        # try:
        #     image = cv2.imread(fil)
        #     gray_image = cv2.cvtColor(os.path.join(path ,image), cv2.COLOR_BGR2GRAY) # convert to greyscale
        #     cv2.imwrite(os.path.join(dstpath ,fil) ,gray_image)
        # except:
        #     print('{} is not converted'.format(fil))

def convert_v2():
    path = sys.argv[1]  # Source Folder
    dstpath = sys.argv[2]  # Destination Folder

    try:
        makedirs(dstpath)
    except:
        print("Directory already exist, images will be written in same folder")
    # Folder won't used

    files = list(filter(lambda f: isfile(join(path, f)), listdir(path)))

    # print("files are {}".format(files))

    for image in files:

        # try:
        # for gif
        cap = cv2.VideoCapture(os.path.join(path, image))
        ret, img = cap.read()
        cap.release()

        # img = cv2.imread(os.path.join(path, image))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # convert from openCV2 to PIL. Notice the COLOR_BGR2RGB which means that
        # the color is converted from BGR to RGB
        color_coverted = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(color_coverted).convert('L')
        dstPath = join(dstpath, image)
        pil_image.save(dstPath+".png")



        #
        # cv2.imwrite(dstPath, gray)
        # except:
        #     print("{} is not converted".format(image))

    # for fil in glob.glob("*.jpg"):
    #
    #     try:
    #         image = cv2.imread(fil)
    #         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to greyscale
    #         cv2.imwrite(os.path.join(dstpath ,fil) ,gray_image)
    #     except:
    #         print('{} is not converted'.format(fil))
    #


if __name__ == '__main__':
    convert_v2()