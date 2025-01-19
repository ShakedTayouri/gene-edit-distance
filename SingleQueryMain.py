import sys
import time

from GedRunner import GedRunner
from cutpoints_detection.HypotheticalCutPointsDetector import HypotheticalCutPointsDetector

if __name__ == '__main__':
    start = time.time()

    query = sys.argv[1]
    description = sys.argv[2]
    classification = sys.argv[3]
    result_path = sys.argv[4]

    print("query " + str(query))
    print("description " + str(description))
    print("classification" + str(classification))
    print("result_path " + str(result_path))

    ged_runner = GedRunner(query, description, classification, [HypotheticalCutPointsDetector()])
    ged_runner.run_ged(result_path)
