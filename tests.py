from unittest import TestCase

from date_extractor import DateExtractor


class TestDateExtractor(TestCase):

    def setUp(self):
        super(TestDateExtractor, self).setUp()

        self.extractor = DateExtractor()

    def test_numerical_date_extraction_plural(self):
        """Assert that expressions like '24 hours' are correctly detected. """
        expressions = [
            ('I am leaving in 24 hours.', ['24 hours']),
            ('I am leaving in 24 days.', ['24 days']),
            ('I am leaving in 24 weeks.', ['24 weeks']),
            ('I am leaving in 24 months.', ['24 months']),
            ('I am leaving in 24 years.', ['24 years']),
        ]

        self._verify_time_expressions(expressions)

    def test_numerical_date_extraction_singular(self):
        """Assert that expressions like '1 hour' are correctly detected. """
        expressions = [
            ('I am leaving in 1 hour.', ['1 hour']),
            ('I am leaving in 1 day.', ['1 day']),
            ('I am leaving in 1 week.', ['1 week']),
            ('I am leaving in 1 month.', ['1 month']),
            ('I am leaving in 1 year.', ['1 year']),
        ]

        self._verify_time_expressions(expressions)

    def test_text_date_extraction_singular(self):
        """Assert that expressions like 'twenty-four (24) hours' are correctly detected. """
        expressions = [
            ('I am leaving in twenty-four (24) hours.', ['twenty-four (24) hours']),
            ('I am leaving in twenty-four (24) days.', ['twenty-four (24) days']),
            ('I am leaving in twenty-four (24) weeks.', ['twenty-four (24) weeks']),
            ('I am leaving in twenty-four (24) months.', ['twenty-four (24) months']),
            ('I am leaving in twenty-four (24) years.', ['twenty-four (24) years']),
        ]

        self._verify_time_expressions(expressions)

    def test_day_type_date_extraction_singular(self):
        """Assert that expressions like 'ten (10) working days' are correctly detected. """
        expressions = [
            ('I am leaving in ten (10) working days.', ['ten (10) working days']),
            ('I am leaving in ten (10) business days.', ['ten (10) business days']),
            ('I am leaving in ten (10) calendar days.', ['ten (10) calendar days']),
        ]

        self._verify_time_expressions(expressions)

    def test_multiple_time_exressions_same_text(self):
        """Assert that if a text contains more than one time expression then all of them are
        extracted.
        """
        expressions = [
            ('I am leaving in ten (10) working days. I will leave in 10 hours or maybe 2 months.',
             ['ten (10) working days', '10 hours', '2 months']),
        ]

        self._verify_time_expressions(expressions)

    def test_false_positives_wrong_time_unit(self):
        """Assert that expressions that don't end in a time unit are not returned. """
        expressions = [
            ('I will buy 10 apples in 3 days.', ['3 days']),
        ]

        self._verify_time_expressions(expressions)

    def test_false_positives_age_expressiosn(self):
        """Assert that age expressions are not returned. """
        expressions = [
            ('I will be 18 years old in 3 days.', ['3 days']),
            ('I will be 18 years of age in 3 days.', ['3 days']),
        ]

        self._verify_time_expressions(expressions)

    def test_to_left_extension(self):
        """Assert that left extensions of numerals works as expected. """
        expressions = [
            ('I am leaving in twenty four (24) days.', ['twenty four (24) days']),
        ]

        self._verify_time_expressions(expressions)

    def _verify_time_expressions(self, expressions):
        for text, expected_expressions in expressions:
            self.assertEqual(self.extractor.extract_dates(text), expected_expressions,
                             'Time expression not correctly was extracted for %s' % text)
