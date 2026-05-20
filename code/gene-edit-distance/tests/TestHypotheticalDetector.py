from unittest import TestCase

from cutpoints_detection.HypotheticalCutPointsDetector import HypotheticalCutPointsDetector
from utils.Hsp import Hsp


class TestHypotheticalCutPointsDetector(TestCase):
    def test_detect_two_cut_points(self):
        cut_points = HypotheticalCutPointsDetector().detect_query_cut_points(
            [Hsp(1, 4, 2, 6, 100), Hsp(6, 8, 0, 3, 20)], 'a' * 10)
        self.assertEqual(cut_points, [4, 6])

    def test_check_edges_detect_three_cut_points(self):
        cut_points = HypotheticalCutPointsDetector().detect_query_cut_points(
            [Hsp(0, 4, 2, 6, 100), Hsp(6, 8, 0, 3, 20), Hsp(10, 14, 0, 3, 20)], 'a' * 15)
        self.assertEqual([4, 6, 8, 10], cut_points)

    def test_detect_multiple_cut_points(self):
        cut_points = HypotheticalCutPointsDetector().detect_query_cut_points(
            [Hsp(1, 4, 2, 6, 100), Hsp(6, 8, 0, 3, 20), Hsp(10, 15, 0, 3, 20), Hsp(20, 22, 0, 3, 20)], 'a' * 30)
        self.assertEqual([4, 6, 8, 10, 15, 20], cut_points)

    def test_detect_single_cut_points(self):
        cut_points = HypotheticalCutPointsDetector().detect_query_cut_points([Hsp(1, 4, 2, 6, 100)],
                                                                             'a' * 6)
        self.assertEqual(cut_points, [])
