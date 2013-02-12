from collections import defaultdict
from itertools import imap, ifilter
from operator import itemgetter

from korpus.utils import tokenizer, idf, tf, cosine_similarity


class Corpus(object):

    def __init__(self, docs,
                 preprocessor=lambda x: x,
                 tokenizer=tokenizer):
        self.tokenizer = tokenizer
        self.preprocessor = preprocessor
        term_vectors = {}
        inverse_term_vectors = defaultdict(set)
        for pk, value in docs:
            tokens = self.tokenizer(self.preprocessor(value))
            term_vectors[pk] = tf(tokens)
            map(lambda ngram: inverse_term_vectors[ngram].add(pk),
                tokens.iterkeys())

        self.idf_dict = idf(inverse_term_vectors)
        self.term_vectors = term_vectors
        self.inverse_term_vectors = inverse_term_vectors

    def query(self, text, min_score=0.8, subset=None):
        tokens = self.tokenizer(self.preprocessor(text))
        terms = tf(tokens)
        similar_docs = set()
        for term in terms.iterkeys():
            map(similar_docs.add, self.inverse_term_vectors[term])
        if subset is not None:
            similar_docs = similar_docs.intersection(subset)

        similar_docs_length = len(similar_docs)

        def score_yielder(similar_doc):
            score = cosine_similarity(terms,
                                      self.term_vectors[similar_doc],
                                      self.idf_dict)
            if score > min_score:
                return similar_doc, score, similar_docs_length

        return sorted(ifilter(None, imap(score_yielder, similar_docs)),
                      key=itemgetter(1), reverse=True)


def similarity_dict(term_vectors, inverse_term_vectors, idf_dict):
    similarity = defaultdict(int)
    for doc, terms in term_vectors.iteritems():
        similar_docs = set()
        for term in terms.iterkeys():
            similar_docs = similar_docs.union(inverse_term_vectors[term])
        for similar_doc in similar_docs:
            if doc < similar_doc:
                similarity[(doc, similar_doc)] = cosine_similarity(
                    terms, term_vectors[similar_doc], idf_dict)
    return similarity
