from collections import defaultdict
from itertools import imap, ifilter, chain
from operator import itemgetter
import math


def ngrams(token, MIN_N=2, MAX_N=6):
    '''Generates n-grams between MIN_N and MAX_N from given sequence.

    :param token: sequence that n-grams is generated from
    :type token: list or str
    :param MIN_N: min n-gram size
    :type MIN_N: int
    :param MAX_N: max n-gram size
    :type MAX_N: int
    :returns: sequence of n-grams
    :rtype: generator
    '''
    n_tokens = len(token)
    for i in range(n_tokens):
        for j in range(i + MIN_N, min(n_tokens, i + MAX_N) + 1):
            yield token[i:j]


def tokenizer(doc, MIN_N=3, MAX_N=5):
    '''Builds Term Vector for doc. Term vector contains n-grams + words
    splitted by dash(-)

    :param doc: document
    :type doc: str
    :param MIN_N: min n-gram
    :type MIN_N: int
    :param MAX_N: max n-gram
    :type MAX_N: int
    :returns: Term Vector of doc
    :rtype: defaultdict(int)
    '''
    n_dict = defaultdict(int)
    for x in chain(ngrams(doc, MIN_N, MAX_N), doc.split('-')):
        n_dict[x] += 1
    return n_dict


def tf(term_vector):
    '''Calculates term frequency vector. Term frequency vector is a kind of
    term vector. It is weighted version of tokenizer.

    Term Frequency is calculated by following equation per term:
    tf of term x = x's number of time seen in doc / total_term_quantity

    :returns: Weighted term vector of doc
    rtype: defaultdict(int)
    '''
    total_term_quantity = sum(term_vector.itervalues()) * 1.0
    tf_dict = defaultdict(int)
    for term, quantity in term_vector.iteritems():
        tf_dict[term] = quantity / total_term_quantity

    return tf_dict


def cardinality(bitset):
    '''The cardinality of a set is a measure of the "number of elements of
     the set". In python, len(set) is cardinality. But we use int as set.
     Our cardinality is number of 1 bits in int.

     >>> cardinality(0) # 0b0 as set()
     0
     >>> cardinality(1) # 0b1 as set([1])
     1
     >>> cardinality(2) # 0b10 as set([2])
     1
     >>> cardinality(3) # 0b11 as set([1,2])
     2
     >>> cardinality(5) # 0b101 as set([[1,3])
     2
     >>> cardinality(13) # 0b1101 as set([1, 3, 4])
     3

    :param bitset: int whose bytes are set
    :type word: int
    '''
    binary = 1
    cardinality = 0
    while(bitset >= binary):
        cardinality += 1 if bool(bitset & binary) else 0
        binary <<= 1

    return cardinality


def idf(inverse_term_vectors):
    '''The inverse document frequency is a measure of whether the term is
    common or rare across all documents. It is obtained by dividing the total
    number of documents by the number of documents containing the term, and
    then taking the logarithm of that quotient.
    '''

    bitset = 0
    for docs in inverse_term_vectors.itervalues():
        for doc in docs:
            bitset |= 1 << (doc - 1)
    total_num_docs = cardinality(bitset)
    idf_dict = defaultdict(int)
    for term, docs in inverse_term_vectors.iteritems():
        idf_dict[term] = math.log(total_num_docs / len(docs))
    return idf_dict


def cosine_similarity(doc1, doc2, weighting_factor):
    '''Calculates cosine similarity between two docs.
    Documents should be term vector or term frequency vector(suggested).

    :param doc1: first term vector or term frequency vector.
    :type doc1: defaultdict(float) or similar. it musn't throw KeyError
    :param doc2: second term vector
    :type doc2: defaultdict(float) or similar. it musn't throw KeyError
    :param weighting_factor: Weight of terms.
    :type weighting_factor: defaultdict(float) or similar. it musn't throw
                            KeyError
    '''
    intersection = set(doc1.iterkeys()) & set(doc2.iterkeys())

    doc1sum = sum(math.pow(value, 2) * math.pow(weighting_factor[key], 2)
                  for key, value in doc1.iteritems())
    doc2sum = sum(math.pow(value, 2) * math.pow(weighting_factor[key], 2)
                  for key, value in doc2.iteritems())
    upper = sum(doc1[key] * doc2[key] * math.pow(weighting_factor[key], 2)
                for key in intersection)
    return math.sqrt((upper * upper) / (doc1sum * doc2sum))


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
