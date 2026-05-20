import unittest

from score_calculator.ScoreByAdjustedAlignment import calculate_score_by_adjusted_alignment, \
    get_sorted_cut_out_fragments
from utils.CutOutFragments import CutOutFragment


class TestSequenceAlignment(unittest.TestCase):
    def test_sort_cut_out_fragments_cut_points(self):
        cut_out_fragments = [CutOutFragment(1, 10), CutOutFragment(10, 15), CutOutFragment(15, 100)]

        self.assertEqual(get_sorted_cut_out_fragments(cut_out_fragments),
                         [CutOutFragment(10, 15), CutOutFragment(1, 10), CutOutFragment(15, 100)])

    def test_k_is_greater_than_number_of_cut_points(self):
        cut_out_fragments = [CutOutFragment(1, 10), CutOutFragment(10, 15), CutOutFragment(15, 100)]
        sorted_cut_out_fragments = get_sorted_cut_out_fragments(cut_out_fragments)
        longest_cut_out_fragment = sorted_cut_out_fragments.pop()

        self.assertEqual(longest_cut_out_fragment, CutOutFragment(15, 100))
        self.assertEqual(sorted_cut_out_fragments,
                         [CutOutFragment(10, 15), CutOutFragment(1, 10)])

    def test_single_hsp_prm_better_than_gaps(self):
        gap_ranges = [CutOutFragment(1946, 2008)]  # 62

        prm = 12

        adjusted_score = 100 + pow(0.98, 1) * (- prm)

        self.assertEqual(adjusted_score, calculate_score_by_adjusted_alignment(gap_ranges, 100))

    def test_single_hsp_gaps_better_than_prm(self):
        gap_ranges = [CutOutFragment(1947, 1950)]

        pgo = 5
        pgx = 2

        score = 100 - pgo - 3 * pgx

        self.assertEqual(calculate_score_by_adjusted_alignment(gap_ranges, 100), score)

    def test_multiple_hsp_gaps_better_than_prm(self):
        gap_ranges = [CutOutFragment(5, 6), CutOutFragment(100, 103), CutOutFragment(200, 202)]

        pgo = 5
        pgx = 2

        score = 100 - 3 * pgo - (3 + 2 + 1) * pgx

        self.assertEqual(calculate_score_by_adjusted_alignment(gap_ranges, 100), score)

    def test_multiple_hsp_two_gap_better_than_prm(self):
        gap_ranges = [CutOutFragment(5, 6), CutOutFragment(100, 103), CutOutFragment(200, 300)]

        pgo = 5
        pgx = 2
        prm = 12

        gaps_penalty = 2 * pgo + (3 + 1) * pgx + prm
        score = 100 + pow(0.98, 1) * - gaps_penalty

        self.assertEqual(calculate_score_by_adjusted_alignment(gap_ranges, 100), score)

    def test_multiple_hsp_one_gap_better_than_prm(self):
        gap_ranges = [CutOutFragment(5, 7), CutOutFragment(100, 120), CutOutFragment(200, 300)]

        pgo = 5
        pgx = 2
        prm = 12

        gaps_penalty = 1 * pgo + 2 * pgx + 2 * prm
        score = 100 + pow(0.98, 2) * - gaps_penalty

        self.assertEqual(score, calculate_score_by_adjusted_alignment(gap_ranges, 100))
