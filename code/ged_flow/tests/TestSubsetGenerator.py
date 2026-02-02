import unittest

from ged_flow.SubsetGenerator import generate_subsets
from ged_flow.utils.Subset import Subset


class SubsetGeneratorTests(unittest.TestCase):
    def test_solve_when_has_one_cut_points(self):
        query = "AppleOrangeBanana"
        cut_points = [5, 11]
        subsets = [Subset("Apple------Banana", cut_points)]

        self.assertEqual(subsets, generate_subsets(query, cut_points, 3))

    def test_solve_when_has_two_cut_points(self):
        query = "AppleOrangeBananaCherryKiwi"
        cut_points = [5, 11, 17, 23]
        subsets = [Subset("AppleOrangeBanana------Kiwi", [17, 23]),
                   Subset("Apple------BananaCherryKiwi", [5, 11]),
                   Subset("Apple------Banana------Kiwi", [5, 11, 17, 23]),
                   Subset("Apple------------CherryKiwi", [5, 17]),
                   Subset("AppleOrange------CherryKiwi", [11, 17]),
                   Subset("AppleOrange------------Kiwi", [11, 23]),
                   Subset("Apple------------------Kiwi", [5, 23]),
                   ]

        self.assertEqual(sorted(subsets), sorted(generate_subsets(query, cut_points, 5)))

    def test_solve_when_has_three_cut_points(self):
        query = "AppleOrangeBananaCherryKiwiMangoLemon"
        cut_points = [5, 11, 17, 23, 27, 32]
        subsets = [
            Subset("Apple---------------------------Lemon", [5, 32]),
            Subset("Apple----------------------MangoLemon", [5, 27]),
            Subset("Apple------------------Kiwi-----Lemon", [5, 23, 27, 32]),
            Subset("Apple------------------KiwiMangoLemon", [5, 23]),
            Subset("Apple------------Cherry---------Lemon", [5, 17, 23, 32]),
            Subset("Apple------------Cherry----MangoLemon", [5, 17, 23, 27]),
            Subset("Apple------------CherryKiwi-----Lemon", [5, 17, 27, 32]),
            Subset("Apple------------CherryKiwiMangoLemon", [5, 17]),
            Subset("Apple------Banana---------------Lemon", [5, 11, 17, 32]),
            Subset("Apple------Banana----------MangoLemon", [5, 11, 17, 27]),
            Subset("Apple------Banana------Kiwi-----Lemon", [5, 11, 17, 23, 27, 32]),
            Subset("Apple------Banana------KiwiMangoLemon", [5, 11, 17, 23]),
            Subset("Apple------BananaCherry---------Lemon", [5, 11, 23, 32]),
            Subset("Apple------BananaCherry----MangoLemon", [5, 11, 23, 27]),
            Subset("Apple------BananaCherryKiwi-----Lemon", [5, 11, 27, 32]),
            Subset("Apple------BananaCherryKiwiMangoLemon", [5, 11]),
            Subset("AppleOrange---------------------Lemon", [11, 32]),
            Subset("AppleOrange----------------MangoLemon", [11, 27]),
            Subset("AppleOrange------------Kiwi-----Lemon", [11, 23, 27, 32]),
            Subset("AppleOrange------------KiwiMangoLemon", [11, 23]),
            Subset("AppleOrange------Cherry---------Lemon", [11, 17, 23, 32]),
            Subset("AppleOrange------Cherry----MangoLemon", [11, 17, 23, 27]),
            Subset("AppleOrange------CherryKiwi-----Lemon", [11, 17, 27, 32]),
            Subset("AppleOrange------CherryKiwiMangoLemon", [11, 17]),
            Subset("AppleOrangeBanana---------------Lemon", [17, 32]),
            Subset("AppleOrangeBanana----------MangoLemon", [17, 27]),
            Subset("AppleOrangeBanana------Kiwi-----Lemon", [17, 23, 27, 32]),
            Subset("AppleOrangeBanana------KiwiMangoLemon", [17, 23]),
            Subset("AppleOrangeBananaCherry---------Lemon", [23, 32]),
            Subset("AppleOrangeBananaCherry----MangoLemon", [23, 27]),
            Subset("AppleOrangeBananaCherryKiwi-----Lemon", [27, 32])]

        self.assertEqual(sorted(subsets), sorted(generate_subsets(query, cut_points, 7)))

    def test_limit_two_cut_points(self):
        query = "AppleOrangeBananaCherryKiwiMangoLemon"
        cut_points = [5, 11, 17, 23, 27, 32]
        subsets = [
            Subset("Apple---------------------------Lemon", [5, 32]),
            Subset("Apple----------------------MangoLemon", [5, 27]),
            Subset("Apple------------------KiwiMangoLemon", [5, 23]),
            Subset("Apple------------CherryKiwiMangoLemon", [5, 17]),
            Subset("Apple------BananaCherryKiwiMangoLemon", [5, 11]),
            Subset("AppleOrange---------------------Lemon", [11, 32]),
            Subset("AppleOrange----------------MangoLemon", [11, 27]),
            Subset("AppleOrange------------KiwiMangoLemon", [11, 23]),
            Subset("AppleOrange------CherryKiwiMangoLemon", [11, 17]),
            Subset("AppleOrangeBanana---------------Lemon", [17, 32]),
            Subset("AppleOrangeBanana----------MangoLemon", [17, 27]),
            Subset("AppleOrangeBanana------KiwiMangoLemon", [17, 23]),
            Subset("AppleOrangeBananaCherry---------Lemon", [23, 32]),
            Subset("AppleOrangeBananaCherry----MangoLemon", [23, 27]),
            Subset("AppleOrangeBananaCherryKiwi-----Lemon", [27, 32])]

        self.assertEqual(sorted(subsets), sorted(generate_subsets(query, cut_points, 2)))

    def test_limit_the_generation_when_has_six_cut_points(self):
        query = "AppleOrangeBananaCherryKiwiMangoLemonApricot"
        cut_points = [5, 11, 17, 23, 27, 32, 37]
        subsets = [Subset("Apple--------------------------------Apricot", [5, 37]),
                   Subset("Apple---------------------------LemonApricot", [5, 32]),
                   Subset("Apple----------------------Mango-----Apricot", [5, 27, 32, 37]),
                   Subset("Apple----------------------MangoLemonApricot", [5, 27]),
                   Subset("Apple------------------Kiwi----------Apricot", [5, 23, 27, 37]),
                   Subset("Apple------------------Kiwi-----LemonApricot", [5, 23, 27, 32]),
                   Subset("Apple------------------KiwiMango-----Apricot", [5, 23, 32, 37]),
                   Subset("Apple------------------KiwiMangoLemonApricot", [5, 23]),
                   Subset("Apple------------Cherry--------------Apricot", [5, 17, 23, 37]),
                   Subset("Apple------------Cherry---------LemonApricot", [5, 17, 23, 32]),
                   Subset("Apple------------Cherry----MangoLemonApricot", [5, 17, 23, 27]),
                   Subset("Apple------------CherryKiwi----------Apricot", [5, 17, 27, 37]),
                   Subset("Apple------------CherryKiwi-----LemonApricot", [5, 17, 27, 32]),
                   Subset("Apple------------CherryKiwiMango-----Apricot", [5, 17, 32, 37]),
                   Subset("Apple------------CherryKiwiMangoLemonApricot", [5, 17]),
                   Subset("Apple------Banana--------------------Apricot", [5, 11, 17, 37]),
                   Subset("Apple------Banana---------------LemonApricot", [5, 11, 17, 32]),
                   Subset("Apple------Banana----------MangoLemonApricot", [5, 11, 17, 27]),
                   Subset("Apple------Banana------KiwiMangoLemonApricot", [5, 11, 17, 23]),
                   Subset("Apple------BananaCherry--------------Apricot", [5, 11, 23, 37]),
                   Subset("Apple------BananaCherry---------LemonApricot", [5, 11, 23, 32]),
                   Subset("Apple------BananaCherry----MangoLemonApricot", [5, 11, 23, 27]),
                   Subset("Apple------BananaCherryKiwi----------Apricot", [5, 11, 27, 37]),
                   Subset("Apple------BananaCherryKiwi-----LemonApricot", [5, 11, 27, 32]),
                   Subset("Apple------BananaCherryKiwiMango-----Apricot", [5, 11, 32, 37]),
                   Subset("Apple------BananaCherryKiwiMangoLemonApricot", [5, 11]),
                   Subset("AppleOrange--------------------------Apricot", [11, 37]),
                   Subset("AppleOrange---------------------LemonApricot", [11, 32]),
                   Subset("AppleOrange----------------Mango-----Apricot", [11, 27, 32, 37]),
                   Subset("AppleOrange----------------MangoLemonApricot", [11, 27]),
                   Subset("AppleOrange------------Kiwi----------Apricot", [11, 23, 27, 37]),
                   Subset("AppleOrange------------Kiwi-----LemonApricot", [11, 23, 27, 32]),
                   Subset("AppleOrange------------KiwiMango-----Apricot", [11, 23, 32, 37]),
                   Subset("AppleOrange------------KiwiMangoLemonApricot", [11, 23]),
                   Subset("AppleOrange------Cherry--------------Apricot", [11, 17, 23, 37]),
                   Subset("AppleOrange------Cherry---------LemonApricot", [11, 17, 23, 32]),
                   Subset("AppleOrange------Cherry----MangoLemonApricot", [11, 17, 23, 27]),
                   Subset("AppleOrange------CherryKiwi----------Apricot", [11, 17, 27, 37]),
                   Subset("AppleOrange------CherryKiwi-----LemonApricot", [11, 17, 27, 32]),
                   Subset("AppleOrange------CherryKiwiMango-----Apricot", [11, 17, 32, 37]),
                   Subset("AppleOrange------CherryKiwiMangoLemonApricot", [11, 17]),
                   Subset("AppleOrangeBanana--------------------Apricot", [17, 37]),
                   Subset("AppleOrangeBanana---------------LemonApricot", [17, 32]),
                   Subset("AppleOrangeBanana----------Mango-----Apricot", [17, 27, 32, 37]),
                   Subset("AppleOrangeBanana----------MangoLemonApricot", [17, 27]),
                   Subset("AppleOrangeBanana------Kiwi----------Apricot", [17, 23, 27, 37]),
                   Subset("AppleOrangeBanana------Kiwi-----LemonApricot", [17, 23, 27, 32]),
                   Subset("AppleOrangeBanana------KiwiMango-----Apricot", [17, 23, 32, 37]),
                   Subset("AppleOrangeBanana------KiwiMangoLemonApricot", [17, 23]),
                   Subset("AppleOrangeBananaCherry--------------Apricot", [23, 37]),
                   Subset("AppleOrangeBananaCherry---------LemonApricot", [23, 32]),
                   Subset("AppleOrangeBananaCherry----Mango-----Apricot", [23, 27, 32, 37]),
                   Subset("AppleOrangeBananaCherry----MangoLemonApricot", [23, 27]),
                   Subset("AppleOrangeBananaCherryKiwi----------Apricot", [27, 37]),
                   Subset("AppleOrangeBananaCherryKiwi-----LemonApricot", [27, 32]),
                   Subset("AppleOrangeBananaCherryKiwiMango-----Apricot", [32, 37])]

        self.assertEqual(sorted(subsets), sorted(generate_subsets(query, cut_points, 4)))

    def test_limit_the_generation_of_multiple_cut_points(self):
        query = "AGCCTGGTGCGGATGCGGCGGGAGGGCGAGGAGGACCTGACCCTGGAGGAGAAGGCCGAGCTGTGCAGCGAGCTGGAGCTGCAGCAGAAGTACGTGGACATCGGCAGCAACATCATCGGCGACCTGAGCAGCCTGCCCATCGTGGGCAAGATCGTGGGCACCATCGCCGCCGCCGCCATGGCCGTGACCCACGTGGCCAGCGGCCGGCTGGACATCGAGCAGACCCTGGGCGGCTGCAGCGACGTGCCCTTCGACCAGATCAAGGAGATCCTGGAGGAGCGGTTCAACGAGATCGACCGGAAGCTGGAGAGCCACAGCGCCGCCCTGGAGGAGATCACCAAGCTGGTGGAGAAGAGCATCAGCGCCGTGGAGAAGACCCGGAAGCAGATGAACAAGCGGTTCGACGAGGTGATGCGGAGCATCCAGGACGCCAAGGTGAGCCCCCTGGTGAGCAAGATCAACAACTTCGCCCGGTACTTCGACACCGAGAAGGAGCGGATCCGGGGCCTGAAGCTGAGCGACTACATCCTGAAGCTGGAGGAGCCCAACGGCATCCTGCTGCACTTCAAGGAGAGCCGGACCCCCCGGGACGACAGCCTGCAGGCCCCCCTGTTCAGCATCATCCAGGAGCGGTACGCCGTGCCCAAGAGCATCGACGACGAGCTGGCCTTCAAGGTGCTGTACGCCCTGCTGTACGGCACCCAGACCTACGTGAGCGTGATGTTCTTCCTGCTGGAGCAGTACAGCTTCCTGGCCAACCACTACTACGAGAAGGGCGACCTGGAGAAGTACGACGAGTACTTCAACAGCCTGAACAACGTGTTCCTGGACTTCAAGAGCAGCCTGGTGGGCACCGGCACCAGCAACAACGAGGGCCTGCTGGACCGGGTGCTGCAGGTGCTGGTGACCGTGAAGAACAGCGAGTTCCTGGGCCTGGAGAAGAACGGCGTGAACGAGATGCTGAACGAGAAGATCAACCTGTTCAACAAGATCAAGGTGGAGATCGAGGGCAAGCAGCGGATGACCCTGAGCGAGACCCCCGAGAACTTCGCCCAGATCAGCTTCGACAAGGACATCACCACCCCCATCGGCGACTGGCGGGACGGCCGGGAGGTGCGGTACGCCGTGCAGTACGCCAGCGAGACCCTGTTCAGCAAGATCAGCCACTGGAGCGACCCCGTGGGCGTGCGGGAGAAGGCCTGCCCCACCCTGCGGATGCCCGTGGACCAGACCCGGCGGAACATCCTGGTGTTCCGGAAGTTCGACAGCAGCAAGCCCCAGCTGGTGGGCGAGATCACCCCCTACCAGAGCAACTTCATCGACATCGACCGGGACCTGTACAACACCGCCAACAACCCCGACAGCGCCGTGGGCTTCAAGGAGTTCACCAAGCTGAACTACGACGGCGCCAACATCCGGGCCACCTTCGAGCAGGGCCGGACCGTGTTCCACGCCGCCGCCAAGAGCGGCAACAGCCGGATCATGATCGGCCTGACCTTCCTGGTGAAGAGCAACGAGCTGAACCAGCCCGACAAGAAGGGCTACACCCCCATCCACGTGGCCGCCGACAGCGGCAACGCCGGCATCGTGAACCTGCTGATCCAGCGGGGCGTGAGCATCAACAGCAAGACCTACAACTTCCTGCAGACCCCCCTGCACCTGGCCGCCCAGCGGGGCTTCGTGACCACCTTCCAGCGGCTGATGGAGAGCCCCGAGATCAACATCAACGAGCGGGACAAGGACGGCTTCACCCCCCTGCACTACGCCGTGCGGGGCGGCGAGCGGATCCTGGAGGCCTTCATCAACCAGATCCGGATCGACCTGAACGCCAAGAGCAACAAGGGCCTGACCCCCTTCCACCTGGCCATCATCAAGGACGACTGGCCCGTGGCCAGCACCCTGCTGGGCAGCAAGAAGGTGGACGTGAACGCCGTGGACGAGAACAACATGACCGCCCTGCACTACGCCGCCATCCTGGGCTACCTGGAGACCACCAAGCAGCTGATCAACCTGAAGGAGATCAACGCCGACGTGGTGAGCAGCCCCGGCCTGCTGAGCGCCCTGCACTACGCCATCCTGTACAAGCACGACGACGTGGCCAGCTTCCTGCTGCGGAGCAGCAACGTGAACGTGAACCTGAAGGCCCTGGGCGGCATCACCCCCCTGCACCTGGCCGTGATCCAGGGCCGGACCCAGATCCTGAGCCTGATGTTCGACATCGGCGTGAACATCGAGCAGCAGACCGACGAGAAGTACACCCCCCTGCACCTGGCCGCCATGAGCAAGTACCCCGAGCTGATCCAGATCCTGCTGGACCAGGGCAGCAACTTCGAGGCCAAGACCAACAGCGGCGCCACCCCCCTGCACCTGGCCACCTTCAAGGGCAAGAGCAAGGCCGCCCTGATCCTGCTGAACAACGAGGTGAACTGGCGGGACACCGACGAGAACGGCCAGATGCCCATCCACGGCGCCGCCATGAACGGCCTGCTGGACGTGGCCCAGGCCATCATCAGCATCGACGCCACCGTGCTGGACATCAAGGACAAGAACAGCGACACCCCCCTGAACCTGGCCGCCCAGAAGAGCCACATCGACGTGATCAAGTACTTCATCGACCAGGGCGCCGACATCAACACCCGGAACAAGACCGGCCACGCCCCCCTGCTGGCCTTCAGCAAGAAGGGCAACCTGGACATGGTGAAGTACCTGTTCGACAAGAACGCCAACGTGTACATCGCCGACAACGACGGCATCAACTTCTTCTACTACGCCGTGCGGAACGGCCACCTGAACATCGTGAAGTACGCCATGAGCGAGAAGGACAAGTTCGAGTGGAGCAACATCGACAACAACCGGCGGGACGAGTGCCCCAAGGAGGAGTGCGCCATCAGCCACTTCGCCGTGTGCGACGCCGTGCAGTTCGACAAGATCGAGATCGTGAAGTACTTCGTGACCACCCTGGGCAACTTCGCCATCTGCGGCCCCCTGCACCAGGCCGCCCGGTACGGCCACCTGGACATCGAGAAGTACCTGGTGGAGGAGGAGGACCTGAACGTGGACGGCAGCAAGCCCGACACCCCCCTGTGCTACGCCAGCGAGAACGGCCACCTGGCCGTGGTGCAGTACCTGGTGAGCAACGGCGCCAAGGTGAACCACGACTGCGGCAACGGCATGACCGCCATCGACAAGGCCATCACCAAGAACCACCTGCAGGTGGTGCAGTTCCTGGCCGCCAACGGCGTGGACTTCCGGCGGAAGAACAAGCTGGGCGCCACCCCCTTCCTGACCGCCGTGAGCGAGAACGCCTTCGACATCGCCGAGTACCTGATCCGGGAGAACCGGCAGGACATCGACATCAACGAGCAGAACGTGGACAAGGAGACCGCCCTGCACCTGGCCGTGTACTACAAGAACCTGCAGATGATCAAGCTGCTGGTGAAGTACGGCATCGACATGACCATCCGGAACGCCTACGACAAGACCGCCCTGGACATCGCCACCGACCTGAAGAACAGCAACATCGTGGAGTACCTGAAGACCAAGAGCGGCAAGTTCCGGCGGGAGTACAAGAGCAGCTACGGCGAGCACAGCCTGCTGCAGACCAACAAGATCAGCAGCTTCATCGACGGCAAGAACATCGAGCACGACCACCCCCAGTTCATCAACGCCGACAACGAGAGCAGCCAGCTGTTCAGCGACACCGCCAGCAACATCGACGTGATCGGCCCCCTGCTGCTGATCGACGTGCTGATCCGGTACTTCAGCAAGCAGGGCTACATCAGCAAGGAGAGCGACAGCGCCAGCGACGGCATCACCCAGGCCGCCGCCCTGAGCATCACCGAGAAGTTCGAGGACGTGCTGAACAGCCTGCACAACGAGAGCGCCAAGGAGCAGGTGGACCTGGCCGAGGTGCACGGCAAGGTGTACGCCGCCCTGAAGAGCGGCCGGAACAGCCAGATCCACCCCATCCTGTGCAGCAGCCTGAAGAGCATCAGCACCCTGAAGCCCGAGGACATGGAGAAGCTGGGCAGCGTGATCATGAACAGCCACAGC"
        cut_points = [150, 210, 512, 571, 601, 652, 833, 888, 1118, 1158, 1331, 1380, 1697, 1734, 1876, 1929, 2093,
                      2142, 2544, 2574, 2604, 2643, 2775, 2805, 3069, 3438, 3479, 3510]

        self.assertEqual(397593, len(generate_subsets(query, cut_points, 6)))

    def test_overlap_hsps(self):
        query = "AppleOrangeApple"
        cut_points = [0, 5, 11, 16]

        subsets = [
            Subset("AppleOrange-----", [11, 16]),
            Subset("-----OrangeApple", [0, 5])
        ]

        self.assertTrue(all(elem in generate_subsets(query, cut_points, 3) for elem in subsets))
