# Module for opening reddit bz2 files on talon

import json
import bz2 

class bz2reader():

    def __init__(self, fname, max_lines=-1):
        self.fname = fname
        self.file_object = bz2.open(self.fname, 'rb')
        self.max_lines = max_lines

    def read_lines(self):
        ''' reads bz2 file line by line and yields dicts'''
        i = 0
        while True:
            data = self.file_object.readline()
            if not data or i >= self.max_lines:
                self.file_object.close()
                break
            i += 1
            yield json.loads(data.decode())
    
    def select_keys(self, keys=[]):
        ''' yield lines with only specified keys'''
        for data in self.read_lines():
            processed = {}
            for k in keys:
                processed[k] = data[k]
            yield processed
    
    def __del__(self):
        if self.file_object:
            self.file_object.close()

    




