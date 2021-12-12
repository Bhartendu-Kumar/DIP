



import os
import sys

#this function replaces dot in the file names with underscore
def renaming():

    path =  sys.argv[1]
    filenames = os.listdir(path)
    print(filenames)

    for filename in filenames:
        print("inside for loop filename: ", filename)
        os.rename(os.path.join(path , filename), os.path.join(path , filename.replace(".", "_")) )




if __name__ == "__main__":
    renaming()