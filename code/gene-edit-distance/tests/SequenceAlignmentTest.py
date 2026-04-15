import unittest

from score_calculator.SequenceAlignment import sequence_alignment


class TestSequenceAlignment(unittest.TestCase):

    def test_basic_alignment(self):
        s1 = "ATTGACCTGA"
        s2 = "AT---CCTGA"
        match, mismatch, gaps_opened, gaps_extended = sequence_alignment(s1, s2)
        self.assertEqual(match, 7)
        self.assertEqual(mismatch, 0)
        self.assertEqual(gaps_opened, 1)
        self.assertEqual(gaps_extended, 2)

    def test_no_match(self):
        s1 = "AGTACG"
        s2 = "TGCATA"
        match, mismatch, gaps_opened, gaps_extended = sequence_alignment(s1, s2)
        self.assertEqual(match, 2)
        self.assertEqual(mismatch, 4)
        self.assertEqual(gaps_opened, 0)
        self.assertEqual(gaps_extended, 0)

    def test_equal_sequences(self):
        s1 = "ACGT"
        s2 = "ACGT"
        match, mismatch, gaps_opened, gaps_extended = sequence_alignment(s1, s2)
        self.assertEqual(match, 4)
        self.assertEqual(mismatch, 0)
        self.assertEqual(gaps_opened, 0)
        self.assertEqual(gaps_extended, 0)

    def test_one_gap_opened(self):
        s1 = "AGTACG"
        s2 = "AG--CG"
        match, mismatch, gaps_opened, gaps_extended = sequence_alignment(s1, s2)
        self.assertEqual(match, 4)
        self.assertEqual(mismatch, 0)
        self.assertEqual(gaps_opened, 1)
        self.assertEqual(gaps_extended, 1)
