import os
import sys

from GedRunner import GedRunner
from cutpoints_detection.HypotheticalCutPointsDetector import HypotheticalCutPointsDetector
from io_utils.FastaReader import FastaReader

if __name__ == '__main__':
    order_address = sys.argv[1]
    result_path = sys.argv[2]

    print(order_address)
    fasta_reader = FastaReader(order_address)
    for query, description in fasta_reader.load_queries():
        query = str(query)
        ged_runner = GedRunner(query, description, [HypotheticalCutPointsDetector()])
        ged_runner.run_ged(result_path)
    os.remove(order_address)
