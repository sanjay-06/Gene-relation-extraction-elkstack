from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Tfifd:
    def __init__(self, query, df):
        self.query = query
        self.df = df

    def rank_results(self):
        cos_sim_list = []
        for index, row in self.df.iterrows():
            normalized_mutation = row['NORMALIZED_MUTATION']
            gene = row['GENE']
            disease = row['DISEASE']
            document = normalized_mutation + ' ' + gene + ' ' + disease
            cos_sim = self.cosine_sim(self.query, document)
            cos_sim_list.append(cos_sim)
        rank = np.argsort(cos_sim_list)[::-1]
        ranked_results = self.df.iloc[rank]
        return ranked_results

    def cosine_sim(self, document):
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_query = tfidf_vectorizer.fit_transform([self.query])
        tfidf_document = tfidf_vectorizer.transform([document])
        return cosine_similarity(tfidf_query, tfidf_document)[0][0]