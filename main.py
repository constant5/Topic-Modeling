from Reddit_Scraper.RedditScraper import redditscraper
from LDA.LDA_Infer import lda_infer
import numpy as np
import pickle


RS = redditscraper()
LDA = lda_infer('LDA\\models\\hash_vect.pk', 'LDA\\models\\lda_model_2.pk')

sports  = RS.Get_Reddit_Comments('sports', 10)
politics  = RS.Get_Reddit_Comments('politics', 10)

data = [post for post in sports['title']] + [post for post in politics['title']]
print(data)

hashed = LDA.hash_vectorize(data)
predicted = LDA.lda_predict(hashed)
topics = [np.where(r==r.max())[0][0] for r in predicted]

for p,t in zip(data, topics):
    print(t, ' : ', p )