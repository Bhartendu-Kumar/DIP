import os
import sys


def main(path):
  
    count = 1

    for root, dirs, files in os.walk(path):
        for i in files:
            os.rename(os.path.join(root, i), os.path.join(root, "changed" + str(count) + ".pgm"))
            count += 1


if __name__ == '__main__':
    path = sys.argv[1]
    main(path)
