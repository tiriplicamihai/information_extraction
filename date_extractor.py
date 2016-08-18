import re

import chardet
import nltk
from nltk.stem.porter import PorterStemmer
from num2words import num2words

from constants import ALLOWED_STEMS, AGE_EXPRESSIONS, YEAR_STEM
from helpers import join_sentence


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
        DATE: {<JJ|NN|NNP|CD|VB><\(><CD><\)><VBG|NN><NNS|NN|JJ>} # thirty (30) working|business days
              {<JJ|NN|NNP|CD|VB><\(><CD><\)><NNS|NN|JJ>} # thirty (30) days
              {<CD><NN><NNS|NN>} # thirty business days
              {<CD><NN|NNS|JJ>} # 10 days, 1 year
    """

    def __init__(self, filename):
        super(DateExtractor, self).__init__()

        with open(filename, 'r') as f:
            self.text = f.read()

        if 'UTF-16' in chardet.detect(self.text).get('encoding', ''):
            self.text = self.text.decode('utf-16')

        self.parser = nltk.RegexpParser(self.GRAMMAR)
        self.stemmer = PorterStemmer()

        print 'Date extractor for file %s' % filename

    def extract_dates(self):
        sentences = self._get_sentences()
        tagged_sentences = [nltk.pos_tag(sent) for sent in sentences]

        result = []
        for sentence in tagged_sentences:
            tree = self.parser.parse(sentence)

            for expression in self._extract_data_from_tree(tree):
                if not expression or self._is_false_positive(expression, sentence):
                    continue

                expression = self._extend_to_left(expression, sentence)
                result.append(expression)

        return result

    def _extend_to_left(self, expression, tagged_sentence):
        """Try to complete the first numeral. It's a helaing method for the next scenario:
        seventy two (72) days.
        """
        num_text = self._extract_number_from_expression(expression)
        if not num_text:
            return expression

        if expression.startswith(num_text):
            # Expression is correctly formatted
            return expression

        # If the text would have contained '-' the expression would have been correct.
        num_words = num_text.split('-')

        if not expression.startswith(num_words[-1]):
            print 'Expression %s does not start with the expected word %s' % (expression,
                                                                              num_words[-1])
            return expression

        sentence = join_sentence([t[0] for t in tagged_sentence])

        # Last word is in the expression, the other words we expect to find in the subsentence.
        # The fact that there can be more such expressions in a sentence was considered but we
        # should not do anything special for them because agreements have a pseudo structure which
        # leads to consistency in terms of formats.
        idx = sentence.find(expression)

        subsentence = sentence[:idx].strip().split()
        subsentence.reverse()

        num_words = num_words[:-1]
        num_words.reverse()

        idx = 0
        wc = len(num_words)
        while idx < wc and num_words[idx] == subsentence[idx]:
            expression = '%s %s' % (num_words[idx], expression)
            idx += 1

        return expression

    def _extract_number_from_expression(self, expression):
        number_search = re.search('\(([0-9]+)\)', expression)
        if not number_search:
            return None

        try:
            number = int(number_search.groups()[0])
        except:
            print "Could not extract number from expression: %s" % expression
            return None

        return num2words(number)

    def _extract_data_from_tree(self, tree):
        expressions = []
        for subtree in tree.subtrees():
            if not subtree.label() == 'DATE':
                continue

            expressions.append(join_sentence([t[0] for t in subtree.leaves()]))

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

    def _is_false_positive(self, expression, tagged_sentence):
        # The last token should be either time unit or 'period'
        time_unit = expression.split()[-1]

        stem = self.stemmer.stem_word(time_unit)
        if stem not in ALLOWED_STEMS:
            return True

        if stem == YEAR_STEM:
            # Check if the sentence represents an age expression (it is followed by "of age"
            # or "old").
            sentence = join_sentence([t[0] for t in tagged_sentence])
            idx = sentence.find(expression) + len(expression)
            subsentence = sentence[idx:].strip()
            # Note: This check may fail if in the same sentence there are both age expressions and
            # date expressions in years. This should not be a problem since no reviewed document
            # has this case (it also doesn't make sense in the pseudo-structure of agreements).
            if any(subsentence.startswith(expr) for expr in AGE_EXPRESSIONS):
                return True

        return False
