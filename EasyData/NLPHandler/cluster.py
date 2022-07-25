# from umap import UMAP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt



def set_embedding(text_list, embed_method="tfidf"):
  if embed_method == "tfidf":
    tfidf = TfidfVectorizer(binary=True, max_features=25_000)
    text_embeddings = tfidf.fit_transform(text_list).toarray()
    return text_embeddings  # numpy.ndarray
  elif embed_method == "d2v":
    raise ValueError("Not Implement")
  elif embed_method == "bert":
    raise ValueError("Not Implement")
  else:
    raise ValueError("Not Implement")



# def dim_reduction(text_embeddings):
#   _umap = UMAP()
#   embed_2d = _umap.fit_transform(text_embeddings)  # numpy.ndarray
#   return embed_2d
def dim_reduction(text_embeddings):
    pass

def set_cluster(df, col, embed_method="tfidf", N_TOPIC=6, text_embeddings=None):
    # ======================== 编码 ========================== #
    if text_embeddings is None:
      text_embeddings = set_embedding( df[col].values )
    # ======================== 降维 ========================== #
    embed_2d = dim_reduction(text_embeddings)
    # ====================== 聚类 ============================ #
    kmeans = KMeans(n_clusters= N_TOPIC)
    kmeans.fit(embed_2d)

    df[f'cluster_{embed_method}'] = kmeans.labels_.tolist()
    df[f'embed_2d_{embed_method}'] = embed_2d.tolist()

    print("check the number of each topic : ")
    print(df[f'cluster_{embed_method}'].value_counts())
    return df


def show_cluster(embed_2d, cluster, save_path="cluster.jpg"):
    # centers = kmeans.cluster_centers_
    cluster_num = len(set(cluster))
    plt.figure(figsize=(10,10))
    plt.scatter(embed_2d[:,0], embed_2d[:,1], s=1, c=cluster)
    plt.title(f'Show {cluster_num} clusters', size=16)

    plt.savefig(save_path)
    plt.show()