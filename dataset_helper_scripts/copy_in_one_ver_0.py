import os
import shutil
import sys

def copy(path, dest):
    name = 0
    for root, dirs, files in os.walk(path):  # replace the . with your starting directory
       for file in files:


          path_file = os.path.join(root,file)

          shutil.copy2(path_file,dest) # change you destination dir
          #rename the file at destination
          # os.rename(os.path.join(dest , file), os.path.join(dest,''.join([str(name), '.pgm']) ))
          # name += 1



if __name__ == '__main__':
    path = sys.argv[1]
    dest = sys.argv[2]
    copy(path, dest)