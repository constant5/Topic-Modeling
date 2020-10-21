import pickle 

class lda_infer():

    def __init__(self, hash_vect, lda_path):
        self.hv = pickle.load(open(hash_vect, 'rb'))
        self.lda = pickle.load(open(lda_path, 'rb'))

    def hash_vectorize(self, data):
        return self.hv.transform(data)

    def lda_predict(self, hash_data):
        return self.lda.transform(hash_data)