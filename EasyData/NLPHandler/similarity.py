# ====================== 设置数据预料 ============================ #
from gensim.similarities import MatrixSimilarity
from gensim import corpora
from sklearn.metrics.pairwise import cosine_similarity


def bow__vec(bow, vocal_size):
    _list = [0] * vocal_size
    for idx, value in bow:
        _list[idx] = value
    return _list

class SimilarityChecker(object):
    def __init__(self, token_documents, num_sim=50):
        super(SimilarityChecker, self).__init__()
        self.num_sim = num_sim
        self.token_documents = token_documents
        self.setting()

    def setting(self):
        items = self.token_documents
        self.dictionary = corpora.Dictionary(items)
        self.vocal_size = len(self.dictionary.token2id)
        self.corpus = [self.dictionary.doc2bow(text) for text in items]
        # ====================== 相似度矩阵 ============================ #
        self.sim_index = MatrixSimilarity(self.corpus, num_features=len(self.dictionary),
                                      num_best=self.num_sim)

    def find_similars(self, token_query):
        query_bow = self.dictionary.doc2bow(token_query)

        sims = self.sim_index[query_bow]

        sims = sorted(sims, key=lambda item: -item[1])
        res = []
        for doc_i, doc_sim in sims:
            res.append({
                "idx": doc_i,
                "doc": " ".join(self.token_documents[ doc_i ]),
                "doc_sim": doc_sim
            })

        return res


class SimilarityChecker4Math(SimilarityChecker):
    def show_similars(self, query, positions, scores, col_q, col_s):
        positions, scores = self.find_similars(query)
        # ======================================================== #
        problems = self.df[col_q].values[positions]
        solutions = self.df[col_s].values[positions]
        solutions = self.df.values[positions]

        solution_set = set()
        problems_set = set()
        for p, s, score in zip(problems, solutions, scores):
            s = s[:-1] if s[-1] == "|" else s  # 过滤相同的解题公式
            if s not in solution_set:
                # 按题目相似度过滤
                p_bow_vec = bow__vec(self.dictionary.doc2bow(
                    next(self.tokeinzer(p))), self.vocal_size)
                max_sim = max(map(lambda x: cosine_similarity([p_bow_vec],
                                                              [bow__vec(self.dictionary.doc2bow(
                                                                  next(self.tokeinzer(x))), self.vocal_size)]
                                                              )[0][0],
                                  problems_set)
                              ) if len(problems_set) > 0 else 0
                # print(f"current_max_sim: {max_sim}")
                if max_sim < 0.98:
                    solution_set.add(s)
                    problems_set.add(p)
                else:
                    continue  # 按题目相似度过滤
            else:
                continue  # 过滤相同的解题公式

            print(f"({score}) [probelm] {p}")
            print(f"[solution] ==> {s}")
            print("-"*50)

        print(f"**** There are {len(solution_set)} difference probelm")
