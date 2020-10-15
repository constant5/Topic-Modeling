# script for data processing pipeline

from BZ2Reader import bz2reader
from glob import glob
import os 

# get list of b22 file in data folder
DATA_FOLDER = 'data'
bz2files = glob(os.path.join(DATA_FOLDER,'*.bz2'))

# for all bz2 files get a subset of attributes

def data_processing(bz2files, max_lines=-1):
    for bz2file in  bz2files:
        bzr = bz2reader(bz2file, max_lines)
        for data in bzr.select_keys(['subreddit','author','body','created_utc']):
            print(data)
            # insert rest of pipeline here

def test():
    data_processing(bz2files, 5)

if __name__=="__main__":
    test()