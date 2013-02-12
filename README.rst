======
korpus
======

Korpus is a tf-idf algorithm implementation , simply helps you create a corpus
of documents which you can query it to find similiar documents for a given
input. So, what is tf-idf?

Wiki definition (http://en.wikipedia.org/wiki/Tf-idf):

    Tf–idf, term frequency–inverse document frequency, is a numerical statistic
    which reflects how important a word is to a document in a collection or
    corpus.
    
    It is often used as a weighting factor in information retrieval and text
    mining. The tf-idf value increases proportionally to the number of times a
    word appears in the document, but is offset by the frequency of the word in
    the corpus, which helps to control for the fact that some words are
    generally more common than others.

Basically, korpus is your best friend, while you are trying to approach what
the actual input meant to be using your pre-indexed document base. This is the
approach what Lucene (the most popular java full text search engine) uses in
backyard (http://lucene.apache.org/core/old_versioned_docs/versions/2_9_0/api/all/org/apache/lucene/search/Similarity.html)

Quickstart
----------

Let's take a look the example below. Currently a document defined as a 
``(id, content)`` tuple and we are going to create a corpus with a bunch of
idioms using these document tuples. Once the corpus created, under the hood,
our idioms are automatically indexed and weighted which is meant to be ready
for querying::

    >>> from korpus.corpus import Corpus

    >>> common_idioms = [
        (1, 'Piece of cake'),
        (2, 'Costs an arm and a leg'),
        (3, 'Break a leg'),
        (4, 'Hit the books'),
        (5, 'Let the cat out of the bag'),
        (6, 'Hit the nail on the head'),
        (7, 'When pigs fly'),
        (8, 'You can’t judge a book by its cover'),
        (9, 'Bite off more than you can chew '),
        (10, 'Scratch someone’s back'),
    ]

    >>> corpus = Corpus(common_idioms)
    >>> resutls = corpus.query('Hit the nail', min_score=0.2)
    [(6, 0.6134307406647964, 4), (4, 0.2928327297980855, 4)]

We tried to find similiar idioms by our input ``Hit the nail`` with a minimum
similarity score of ``0.2``. The returned list of objects contains the
information about matched items in corresponding corpus. In this case there two
matched items of ids ``6`` and ``4`` with similarity scores
``0.6134307406647964`` and ``0.2928327297980855`` beside the total match count
of ``4``

This means there are 4 matched results. Two of them are above the ``min_score``
threshold those are::

    * Hit the nail on the head (0.613)
    * Hit the books (0.292)

Documentation
-------------

Coming soon...


Contributors
------------

* Mumin Ozturk (`@mumino <http://github.com/mumino>`_)
* Kadir Pekel (`@kadirpekel <http://github.com/kadirpekel>`_)

License
-------
Copyright (c) 2013 Metglobal LLC.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the 'Software'), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
