from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import jieba
import re
import string
from gensim.models import TfidfModel
from gensim.corpora import Dictionary


def get_tfdif_keywords(text_list, top_num=10):
  _tfidf = TfidfVectorizer(stop_words=None, binary=True, max_features=25_000) # stop_words='english'
  text_embeddings = _tfidf.fit_transform( text_list ).toarray()
  print("shape of text_embeddings",text_embeddings.shape)
  print("len of features",len(_tfidf.get_feature_names()))
  mm = np.mean( text_embeddings, axis=0 )
  ii = np.argsort(mm)[-top_num:][::-1].tolist()
  top_words = [(_tfidf.get_feature_names()[i], mm[i]) for i in ii]
  print(f"{top_num} top words: \n",*top_words[:10], " ...")
  return top_words


def get_keyword(text):
    topk = min(3,len(text))
    keyword = [word for word in jieba.analyse.textrank(text, topK = topk)]
    return keyword


class gensimTfidf(object):
    def __init__(self, items):
        
        self.dct = Dictionary(items)  # fit dictionary
        
        # self.dct.filter_tokens(bad_ids=[self.dct.token2id['ema']])

        self.corpus = [self.dct.doc2bow(item) for item in items]  # convert corpus to BoW format
        self.model = TfidfModel(self.corpus)  # fit model

    def get_item_top(self, item, top_k=10, filter_key=None):
        bow_item  = self.dct.doc2bow(item)
        tfidf_pairs = self.model[bow_item]  # apply model to the first corpus document
        
        tfidf_pairs = sorted(tfidf_pairs, key=lambda x: x[1], reverse=True)

        top_k = min(top_k, len(bow_item) )

        keywords = [self.dct.get(k) for k,v in tfidf_pairs]
        if filter_key is not None:
            keywords =  [k for k in keywords if not filter_key(k)]
        
        keywords = keywords[:top_k]
        return keywords

    def get_corpus_top(self, top_k=10):
        return self.dct.filter_n_most_frequent(top_k)


def filter_num(str):
    if str in string.punctuation:
        return True
    pattern = re.compile(r"\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?")
    return re.match(pattern, str)


  