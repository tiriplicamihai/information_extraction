import re

import nltk


class DateExtractor(object):
    """Module for extracting date expressions from text.
    Examples of recognized dates:
        - 10 days
        - ten days
        - 11/10/2106
        - 12 months
        - one year.
    """

    GRAMMAR = r"""
        CHUNK: {<NN><\(><CD><\)><NNS|NN>}
    """

    def __init__(self, filename):
        super(DateExtractor, self).__init__()

        with open(filename, 'r') as f:
            self.text = f.read()

        self.text = self.text.decode('utf-16')

        self.parser = nltk.RegexpParser(self.GRAMMAR)

        print 'Date extractor for file %s' % filename

    def extract_dates(self):
        sentences = self._get_sentences()
        tagged_sentences = [nltk.pos_tag(sent) for sent in sentences]

        s = [(u'thirty', 'NN'), (u'(', '('), (u'30', 'CD'), (u')', ')'), (u'days', 'NNS')]

        tree = self.parser.parse(s)

        time_expression = self._extract_data_from_tree(tree)
        return []

    def _extract_data_from_tree(self, tree):
        for subtree in tree.subtrees():
            if subtree.label() == 'CHUNK':
                return ' '.join(w for w, _ in subtree.leaves())

        return ''

    def _get_sentences(self):
        sentences = nltk.sent_tokenize(self.text)
        # Remove new lines
        sentences = [s.replace('\r\n', ' ') for s in sentences]

        # Collapse whitespaces
        rex = re.compile(r'[ \t]+')
        sentences = [rex.sub(' ', s) for s in sentences]

        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        return sentences
