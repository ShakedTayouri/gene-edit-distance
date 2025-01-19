from unittest import TestCase

from utils.CutOutFragments import CutOutFragment
from utils.Subset import find_cut_out_fragments


class Subset(TestCase):
    def test_find_cut_out_fragments_single_gaps(self):
        self.assertEqual(find_cut_out_fragments("AAA----BBBB"),
                         [CutOutFragment(3, 7)])

    def test_find_cut_out_fragments_multiple_gaps(self):
        self.assertEqual(find_cut_out_fragments("AAA----BBBB----CCCC-----"),
                         [CutOutFragment(3, 7), CutOutFragment(11, 15), CutOutFragment(19, 24)])
