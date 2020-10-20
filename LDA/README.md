These files are based on 

https://towardsdatascience.com/end-to-end-topic-modeling-in-python-latent-dirichlet-allocation-lda-35ce4ed6b3e0


* Note you need to put your data file in data/

* Note you must add:

    if isinstance(vectorizer, eli5.sklearn.unhashing.InvertableHashingVectorizer):
        return w[0]['name'] if isinstance(w, list) else str(w) for w in vectorizer.get_feature_names() ]

to line 23 in for it to work with the hash vectorizer the your_env/lib/python3.6/site-packages/pyLDAvis/sklearn.py

For initial training of both the vectorizer and the LDA model

python LDA.py --data_dir data --num_post 1000000 --n_features 40000 --topics 10







