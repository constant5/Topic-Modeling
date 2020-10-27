import sklearn
from joblib import load
import numpy as np
import os
import pickle
import re


hv = pickle.load(open('./hash_vect.pk', 'rb'))

#Return loaded model
def load_model(modelpath):
    print(modelpath)
#     clf = load(os.path.join(modelpath,'model.joblib'))
    lda = pickle.load(open(os.path.join(modelpath,'lda_model_8.pk'), 'rb'))
    print("loaded")
    return lda

def data_process(data):
    data = [re.sub('[,\\.!?]', '', x) for x in data]
    # Convert the titles to lowercase
    data = [x.lower() for x in data]
    # Remove post with less than 10 words
    data = [x for x in data if len(x.split(' '))>10]
    return hv.transform(data)

# return prediction based on loaded model (from the step above) and an input payload
def predict(model, payload):
    try:
        # locally, payload may come in as a list
        if type(payload)==str:
#             payload = data_process(payload)
#             payload = hash_vectorize(payload)
            out = str(model.transform(data_process([payload]))[0])
        # in remote / container based deployment, payload comes in as a stream of bytes
        else:
#             payload = data_process(paylod.decode())
#             payload = hash_vectorize(payload)
            out = str(model.transform(data_process([payload.decode()]))[0])
    except Exception as e:  
        out = [type(payload),str(e)] #useful for debugging!
    
    return out
