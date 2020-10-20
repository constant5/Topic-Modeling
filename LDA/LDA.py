# %%

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

import argparse
from scripts.data_processing import data_processing
from glob import glob
import os
import re
from wordcloud import WordCloud
from pprint import pprint
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from eli5.sklearn import InvertableHashingVectorizer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import LatentDirichletAllocation as LDA
from pyLDAvis import sklearn as sklearn_lda
import pickle 
import pyLDAvis
import random

parser = argparse.ArgumentParser(description='LDA Model')

### arguments
parser.add_argument('--data_dir', type=str, default='data', help='directory where data is located')
parser.add_argument('--num_posts', type=int, default=2500000, help='number of posts to load')
parser.add_argument('--word_cloud', type=int, default=0, help='make word cloud plot')
parser.add_argument('--n_features', type=int, default=40000, help='dimension of hash vectors')
parser.add_argument('--topics', type=int, default=10, help='number of topics for LDA model')
parser.add_argument('--hash_vect', type=str, default=None, help='location of vectorizer (ex. models/hash_vect.pk)')
parser.add_argument('--lda_path', type=str, default=None, help='location of lda model (ex. models/lda_model.pk)')
parser.add_argument('--plot_10', type=int, default =0 , help='plot top 10 words from vectorization')
parser.add_argument('--max_iter', type=int, default=10, help='iterations of LDA algorithm')
parser.add_argument('--prepare_vis', type=int, default=0, help='prepare LDAvis')
parser.add_argument('--run_exp', type=str, default=None, help='list(n_topics) to fit LDA')
args = parser.parse_args()


# ### Create post generator
# %%

data_path = os.path.join(args.data_dir, '*.bz2')
bzfile = glob(data_path)
d = data_processing(bzfile, args.num_posts)
print('loading data...', end=' ')
data = [l for l in d]
print('done')

# ### Data processing steps
# %%
# Remove punctuation
print('processing data...', end=' ')
data = [re.sub('[,\\.!?]', '', x) for x in data]
# Convert the titles to lowercase
data = [x.lower() for x in data]
# Remove post with less than 10 words
data = [x for x in data if len(x.split(' '))>10]
print('done')
# display some data
print('first 4 posts:')
pprint(data[:3])
print('\n')

# ### Word Cloud visualization

# %%
if args.word_cloud:
    print('generating word cloud...', end=' ')
    long_string = ','.join(data)
    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
    # Generate a word cloud
    wordcloud.generate(long_string)
    # Save the word cloud image
    wordcloud.to_file(os.path.join('results','wordcloud.png'))
    # Visualize the word cloud
    # wordcloud.to_image()
    print('done')

# %%
### Word freq visualization and count vectorizer

# %%

sns.set_style('whitegrid')
# get_ipython().run_line_magic('matplotlib', 'inline')
# Helper function
def plot_10_most_common_words(count_data, count_vectorizer):
    words = count_vectorizer.get_feature_names()
    total_counts = np.zeros(len(words))
    for t in count_data:
        total_counts+=t.toarray()[0]
    
    count_dict = (zip(words, total_counts))
    count_dict = sorted(count_dict, key=lambda x:x[1], reverse=True)[0:10]
    words = [w[0][0]['name'] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words)) 
    
    ax = plt.figure(2, figsize=(20, 20/1.6180))
    plt.subplot(title='10 most common words on 10,000 sample posts')
    sns.set_context("poster", font_scale=1.25, rc={"lines.linewidth": 2.5})
    sns.barplot(x=x_pos, y=counts, palette='husl')
    plt.xticks(x_pos, words, rotation=90) 
    plt.xlabel('words')
    plt.ylabel('counts')
    plt.savefig(os.path.join('results','top10words.png'), bbox_inches='tight', facecolor='white')
    plt.show()
# Initialise the count vectorizer with the English stop words
# count_vectorizer = CountVectorizer(stop_words='english')
if args.hash_vect:
    print('loading hash vectorizer...', end=' ')
    hash_vectorizer = pickle.load(open(args.hash_vect, 'rb'))
    hash_data = hash_vectorizer.transform(data)
    print('done')
else: 
    print('fitting hash vectorizer...', end=' ')
    hash_vectorizer = HashingVectorizer(stop_words='english',
                                        alternate_sign=False, 
                                        n_features=args.n_features)
    hash_data = hash_vectorizer.fit_transform(data)
    print('done')
    print('saving hash vectorizer ...', end='')
    pickle.dump(hash_vectorizer, open(os.path.join('models','hash_vect.pk'), 'wb'))
    print('done')


ivec = InvertableHashingVectorizer(hash_vectorizer)
sample_size = 10000
X_sample = random.sample(data, k=sample_size)
print('fitting invertable hash vectorizer...', end=' ')
count_sample = ivec.fit_transform(X_sample)
print('done')
# # Fit and transform the processed titles
# count_data = count_vectorizer.fit_transform(data)

# Visualize the 10 most common words
#plot_10_most_common_words(count_data, count_vectorizer)
if args.plot_10:
    print('plotting top 10 in sample')
    plot_10_most_common_words(count_sample, ivec)

# ### LDA model fit

# %%
# Helper function
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i][0]['name']
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        
def lda_experiment(number_topics, hash_data, max_iter):
    print(number_topics)
    print(f'fitting the LDA model with {number_topics} topics')
    lda = LDA(n_components=number_topics,
            learning_method='online',
            max_iter=max_iter, 
            evaluate_every=5,
            batch_size=128**2, 
            verbose=1,
            n_jobs=-1)
    # save model
    lda.fit(hash_data)
    print('saving LDA model ...', end='')
    pickle.dump(lda, open(os.path.join('models',f'lda_model_{number_topics}.pk'), 'wb'))
    print('done')
    return lda

number_topics = args.topics

if not args.run_exp:
    if args.lda_path:
        lda = pickle.load(open(args.lda_path, 'rb'))
    else:
        lda = lda_experiment(args.topics, hash_data, args.max_iter)


    # Print the topics found by the LDA model
    print("Topics found via LDA:")
    number_words = 10
    print(f'Displaying top {number_words} words in LDA topics')
    print_topics(lda, ivec, number_words)




# %%

def prepare_vis(lda, count_sample, ivec,number_topics):
    print('preparing LDAvis...', end=' ')
    LDAvis_data_filepath = os.path.join('results','./ldavis_prepared_'+str(number_topics))
    # # this is a bit time consuming 
    LDAvis_prepared = sklearn_lda.prepare(lda, count_sample, ivec)
    pyLDAvis.save_html(LDAvis_prepared, LDAvis_data_filepath +'.html')
    print('done')

if args.prepare_vis:
    prepare_vis(lda, count_sample, ivec,args.topics)

# %%
def run_experiment(n_topics, max_iter):
    n_topics = [int(n) for n in n_topics.replace('[','').replace(']','').split(',')]
    print(n_topics)
    for n in n_topics:
        # Create and fit the LDA model
        lda = lda_experiment(n, hash_data, max_iter)
        prepare_vis(lda, count_sample, ivec,n)

if args.run_exp:
    run_experiment(args.run_exp, args.max_iter)


