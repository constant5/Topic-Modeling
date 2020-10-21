import pickle
import re

class lda_infer():

    def __init__(self, hash_vect, lda_path):
        self.hv = pickle.load(open(hash_vect, 'rb'))
        self.lda = pickle.load(open(lda_path, 'rb'))

    def data_process(self, data):
        data = [re.sub('[,\\.!?]', '', x) for x in data]
        # Convert the titles to lowercase
        data = [x.lower() for x in data]
        # Remove post with less than 10 words
        data = [x for x in data if len(x.split(' '))>10]
        return data

    def hash_vectorize(self, data):
        return self.hv.transform(data)

    def lda_transform(self, hash_data):
        return self.lda.transform(hash_data)

    def infer(self, data):
        data = self.data_process(data)
        data_vec = self.hash_vectorize(data)
        return data, self.lda_transform(data_vec)
