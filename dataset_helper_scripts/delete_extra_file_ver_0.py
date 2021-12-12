

import os
import sys


def delete(mydir):

    filelist = [ f for f in os.listdir(mydir) if f.endswith(".eye") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))

if __name__ == '__main__':
    mydir = sys.argv[1]
    delete(mydir)