from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import jieba

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


  