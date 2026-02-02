from unittest import TestCase

from ged_flow.GedRunner import match_strings


class TestGedRunner(TestCase):
    def test_basic_match(self):
        main_string = 'sp|A0A088MIT0|BRKP2_PHYNA'
        search_strings = ['sp|A0A088MIT0.1|', 'sp|A8390F4']

        is_match, match_string = match_strings(main_string, search_strings)

        self.assertTrue(is_match)
        self.assertEqual(match_string, 'sp|A0A088MIT0.1|')

    def test_no_match(self):
        main_string = 'sp|A0A088MIT0|BRKP2_PHYNA'
        search_strings = ['sp|A8390F4']

        is_match, _ = match_strings(main_string, search_strings)

        self.assertFalse(is_match)

    def test_partial_match(self):
        main_string = 'sp|A0A088MIT0|BRKP2_PHYNA'
        search_strings = ['sp|A0A088', 'BRKP2']

        is_match, _ = match_strings(main_string, search_strings)

        self.assertFalse(is_match)

    def test_multiple_matches(self):
        main_string = 'sp|A0A088MIT0|BRKP2_PHYNA'
        search_strings = ['sp|A0A088MIT0.1|', 'BRKP2', 'PHYNA']

        is_match, match_string = match_strings(main_string, search_strings)

        self.assertTrue(is_match)
        self.assertEqual(match_string, 'sp|A0A088MIT0.1|')

    def test_empty_main_string(self):
        main_string = ''
        search_strings = ['sp|A0A088MIT0.1|', 'sp|A8390F4']

        is_match, _ = match_strings(main_string, search_strings)

        self.assertFalse(is_match)

    def test_empty_search_strings(self):
        main_string = 'sp|A0A088MIT0|BRKP2_PHYNA'
        search_strings = []

        is_match, _ = match_strings(main_string, search_strings)

        self.assertFalse(is_match)

    def test_empty_both(self):
        main_string = ''
        search_strings = []

        is_match, _ = match_strings(main_string, search_strings)

        self.assertFalse(is_match)
