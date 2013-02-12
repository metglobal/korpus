import unittest
import math
from collections import defaultdict
from mock import patch, call

from korpus.utils import (ngrams, tokenizer, tf, cardinality, idf,
                          cosine_similarity)


class TestUtils(unittest.TestCase):

    def test_ngrams(self):
        s = "1234567 abcd"
        tokens = ngrams(s, MIN_N=1, MAX_N=1)
        self.assertListEqual(sorted(s), sorted(tokens))

        self.assertListEqual([s, ], list(ngrams(s, MIN_N=len(s),
                                                MAX_N=len(s)))
                             )

        self.assertListEqual([s, ], list(ngrams(s, MIN_N=len(s),
                                                MAX_N=len(s) + 1))
                             )

        self.assertListEqual([], list(ngrams(s, MIN_N=len(s) + 1,
                                             MAX_N=len(s) + 1))
                             )

        tokens = ngrams(s, MIN_N=len(s) - 1, MAX_N=len(s))
        self.assertListEqual(sorted([s[:len(s) - 1], s, s[1:len(s)]]),
                             sorted(tokens))

    def test_tokenizer(self):
        with patch('korpus.utils.ngrams') as ngrams_mock:

            s = 'tested-string-is-this-and-this-goes-on'
            ngrams_calls = []

            def  ngrams_mock_side_effect(token, MIN_N=2, MAX_N=6):
                ngrams_calls.append(call(token, MIN_N, MAX_N))
                return []

            ngrams_mock.side_effect = ngrams_mock_side_effect
            ret = tokenizer(s, 3, 5)
            expected = defaultdict(int)
            for x in s.split('-'):
                expected[x] += 1
            self.assertDictEqual(ret, expected)
            self.assertEqual(len(ngrams_calls), 1)
            self.assertEqual(ngrams_calls[0], call(s, 3, 5))

            return_value = ['a', 'b', 'c', 'd']
            ngrams_calls = []

            def  ngrams_mock_side_effect2(token, MIN_N=2, MAX_N=6):
                ngrams_calls.append(call(token, MIN_N, MAX_N))
                return return_value

            ngrams_mock.side_effect = ngrams_mock_side_effect2
            ret = tokenizer(s, 2, 4)
            for x in return_value:
                expected[x] += 1

            self.assertDictEqual(ret, expected)
            self.assertEqual(len(ngrams_calls), 1)
            self.assertEqual(ngrams_calls[0], call(s, 2, 4))

    def test_tf(self):
        d = {"a": 10, "b": 10, "c": 60, "d": 20}
        ret = tf(d)
        expected = defaultdict(int,
                               {'a': 0.1, 'c': 0.6, 'b': 0.1, 'd': 0.2})
        self.assertDictEqual(ret, expected)

    def test_cardinality(self):
        self.assertEqual(cardinality(0), 0)
        self.assertEqual(cardinality(1), 1)
        self.assertEqual(cardinality(2), 1)
        self.assertEqual(cardinality(3), 2)
        self.assertEqual(cardinality(4), 1)
        self.assertEqual(cardinality(5), 2)
        self.assertEqual(cardinality(13), 3)

    def test_idf(self):
        inverse_term_vector = {'a': [1, 2],
                               'b': [2, 3, 4, 5, 6],
                               'c': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                     13, 14, 15, 16, 17, 18, 19, 20]}
        ret = idf(inverse_term_vector)
        expected = defaultdict(int, c=0, b=math.log(4), a=math.log(10))
        self.assertDictEqual(ret, expected)

    def test_cosine_similarity(self):
        idf_dict = defaultdict(lambda: 1)
        d1 = {"a": 10, "b": 10, "c": 10, "d": 10}

        ret = cosine_similarity(d1, d1, idf_dict)
        self.assertEqual(ret, 1)

        d2 = {"e": 10}
        ret = cosine_similarity(d1, d2, idf_dict)
        self.assertEqual(ret, 0)

        d1 = {"a": 6, "b": 8}
        d2 = {"a": 3, "e": 4}
        ret = cosine_similarity(d1, d2, idf_dict)
        self.assertEqual(ret, 0.36)

        d1 = {"a": 6, "b": 4}
        d2 = {"a": 3, "e": 4}
        idf_dict = defaultdict(lambda: 1, b=2)
        ret = cosine_similarity(d1, d2, idf_dict)
        self.assertEqual(ret, 0.36)

    def test_index(self):
        pass
