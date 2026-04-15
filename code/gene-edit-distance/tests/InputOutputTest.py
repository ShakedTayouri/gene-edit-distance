import unittest

from Bio.Seq import Seq

from io_utils.CsvWriter import CsvWriter
from io_utils.FastaReader import FastaReader


class IoTest(unittest.TestCase):
    def test_loadQueries(self):
        queries_input = 'C:\\Users\\shake\\PycharmProjects\\ged\\data\\order.fasta'
        sequence = [(Seq(
            'GGCACCGCGTGCAGCTGCGGCAACAGCAAAGGCATTTATTGGTTTTATCGCCCGAGCTGCCCGACCGATCGCGGCTATACCGGCAGCTGCCGCTATTTTCTGGGCACCTGCTGCACCCCGGCGGAT'),
            ' OSA2 3SX1_OPHHA P83302 Neurotoxin Oh9-1 OS=Ophiophagus hannah OX=8665 PE=1 SV=1')]

        fasta_reader = FastaReader(queries_input)
        self.assertEqual(sequence, fasta_reader.load_queries())

    def test_text_to_exel(self):
        exel_address = \
            'C:\\Users\\shake\\PycharmProjects\\basic-gene-edit-distance\\data\\Benchmark.xlsx'
        csv_writer = CsvWriter(exel_address)

        text_address = \
            "C:\\Users\\shake\\PycharmProjects\\basic-gene-edit-distance\\data\\output_01-01-24.txt"
        csv_writer.save_classification_from_text(text_address)
