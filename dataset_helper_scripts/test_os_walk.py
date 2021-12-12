import cv2

import os ,glob

from os import listdir ,makedirs , walk

from os.path import isfile ,join
path = 'folder_src' # Source Folder
dstpath = 'folder_dest' # Destination Folder

def test_os_walk_0():
    print(os.walk('folder_src'))

    for (dirpath, dirnames, filenames) in walk(path):

        print('dirpath: ',dirpath)
        print('dirnames: ',dirnames)
        print('filenames: ',filenames)
        print('\n')

def test_walk():
    print(next(os.walk('.'))[1])
    print("sub d")
    for subd in next(os.walk('.'))[1]:
        print(subd)

def test_os_walk_1():
    sub_d  = list(filter(lambda f: os.path.isdir(join(path ,f)), listdir(path)))
    print(sub_d)

if __name__ == '__main__':
    test_os_walk_1()