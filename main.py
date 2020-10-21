from Reddit_Scraper.RedditScraper import redditscraper
from LDA.LDA_Infer import lda_infer
import numpy as np
import pickle


RS = redditscraper()
LDA = lda_infer('LDA\\models\\hash_vect.pk', 'LDA\\models\\lda_model_2.pk')

sports  = RS.Get_Reddit_Comments('sports', 20)

politics  = RS.Get_Reddit_Comments('politics', 20)

sports = [post for post in sports['title']]
politics = [post for post in politics['title']]

clean_sports, pred_sports = LDA.infer(sports)
clean_politics, pred_poly = LDA.infer(politics)

s_topics = [np.where(r==r.max())[0][0] for r in pred_sports]
p_topics = [np.where(r==r.max())[0][0] for r in pred_poly]

for post, pred in zip(clean_sports, s_topics):
    print('r/sports' ,'-', pred, ' : ', post)
for post, pred in zip(clean_politics, p_topics):
    print('r/politics' ,'-', pred, ' : ', post)