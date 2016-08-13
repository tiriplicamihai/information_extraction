import re

import nltk
import chardet

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
        CHUNK: {<JJ|NN|NNP|CD|VB><\(><CD><\)><VBG|NN><NNS|NN|JJ>} # thirty (30) working|business days
               {<JJ|NN|NNP|CD|VB><\(><CD><\)><NNS|NN|JJ>} # thirty (30) days
               {<CD><NN><NNS|NN>} # thirty business days
               {<CD><NN|NNS>} # 10 days, 1 year
    """

    def __init__(self, filename):
        super(DateExtractor, self).__init__()

        with open(filename, 'r') as f:
            self.text = f.read()

        if 'UTF-16' in chardet.detect(self.text).get('encoding', ''):
            self.text = self.text.decode('utf-16')

        self.parser = nltk.RegexpParser(self.GRAMMAR)

        print 'Date extractor for file %s' % filename

    def extract_dates(self):
        sentences = self._get_sentences()
        tagged_sentences = [nltk.pos_tag(sent) for sent in sentences]

        result = []
        for sentence in tagged_sentences:
            #if any(['15' in w for w, _ in sentence]):
            #    import ipdb; ipdb.set_trace()
            tree = self.parser.parse(sentence)
            time_expressions = self._extract_data_from_tree(tree)

            if time_expressions:
                result.extend(time_expressions)

        return result

    def _extract_data_from_tree(self, tree):
        expressions = []
        for subtree in tree.subtrees():
            if subtree.label() == 'CHUNK':
                expressions.append(' '.join(w for w, _ in subtree.leaves()))

        return expressions

    def _get_sentences(self):
        sentences = nltk.sent_tokenize(self.text)
        # Remove new lines
        sentences = [s.replace('\r\n', ' ') for s in sentences]

        # Collapse whitespaces
        rex = re.compile(r'[ \t]+')
        sentences = [rex.sub(' ', s) for s in sentences]

        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        return sentences
