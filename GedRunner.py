import configparser
import os
import re
import tempfile
import time
from functools import reduce

from Bio import SearchIO
from Bio.Blast.Applications import NcbiblastnCommandline, NcbiblastxCommandline

from SubsetGenerator import generate_subsets
from cutpoints_detection.AbstractCutPointsDetector import BaseCutPointsDetector
from hit_collector.HitCollector import collect_hits
from io_utils.FastaWriter import FastaWriter
from score_calculator.ScoreByAdjustedAlignment import calculate_score_by_adjusted_alignment

BLAST_XML_FORMAT = 5


def match_strings(main_string, search_strings):
    print(main_string)
    print(search_strings)

    pattern = r'\|[A-Z0-9]+'

    # Find all occurrences of the pattern in the main_string
    matches_main = set(re.findall(pattern, main_string))

    for search_string in search_strings:
        # Find all occurrences of the pattern in the search_string
        matches_search = set(re.findall(pattern, search_string))

        # Check if any of the matches from main_string are in search_string
        if matches_main & matches_search:
            return True, search_string

    return False, ''


class GedRunner:
    """
    This class will perform GED flow for a query.
    Perform on a query BLAST, get HSP per hit.
    For each hit, calculate the hsps likelihood to merge to toxin.
    """

    def __init__(self, base_query, description, cut_points_detectors: list):
        self.start_time = time.time()
        self.base_query = base_query
        self.description = description
        self.cut_points_detectors = []

        print("Query: " + str(self.base_query))
        print("Description: " + str(self.description))

        for cut_points_detector in cut_points_detectors:
            assert issubclass(type(cut_points_detector), BaseCutPointsDetector), \
                "This cut point detector isn't a subclass of BaseCutPointsDetector."
            self.cut_points_detectors.append(cut_points_detector)

        # Creating temp files.
        self.temp_query_path = tempfile.mktemp(prefix="temp_query_")
        self.temp_subject_path = tempfile.mktemp(prefix="temp_subject_")
        self.temp_result_path = tempfile.mktemp(prefix="temp_result_")

        # Read the configs from the config.ini file.
        self.config = configparser.ConfigParser()
        self.config.read(os.path.dirname(__file__) + '/config.ini')

        self.maximum_active_cut_points = int(self.config['running_parameters']['maximum_active_cut_points'])

        # Create the blastn cline object.
        self.blastn = NcbiblastnCommandline(query=self.temp_query_path,
                                            out=self.temp_result_path,
                                            outfmt=BLAST_XML_FORMAT,
                                            db=self.config['blast_parameters']['db'],
                                            cmd=self.config['blast_paths']['blastn_path'],
                                            evalue=self.config['blast_parameters']['evalue'],
                                            task='blastn-short')

        # Create the blastx against subject data cline object.
        self.blastx_2sequences = NcbiblastxCommandline(query=self.temp_query_path,
                                                       subject=self.temp_subject_path,
                                                       out=self.temp_result_path,
                                                       outfmt=BLAST_XML_FORMAT,
                                                       cmd=self.config['blast_paths']['blastx_path'])

    def __del__(self):
        # Deletes the temp files.
        os.remove(self.temp_query_path)
        os.remove(self.temp_result_path)
        if os.path.exists(self.temp_subject_path):
            os.remove(self.temp_subject_path)

    def get_time_running(self) -> str:
        # Get the time passed from the starting.
        return str(time.time() - self.start_time)

    def run_blast(self, query) -> list:
        """
        Perform blast (Basic Local Alignment Search Tool).
        :param: The query for blast.
        :return: List of hits points.
        """
        # Write the query in to the temp file.
        FastaWriter(self.temp_query_path).save_queries(query)

        # Run the blast command.
        self.blastn()

        with open(self.temp_result_path) as result_file:
            return SearchIO.read(result_file, "blast-xml")

    def run_blast_against_subject(self, query, hit) -> list:
        """
        Perform blast (Basic Local Alignment Search Tool).
        :param: The query and the subject for blast.
        :return: List of hits points.
        """
        # Write the query and the subject in to the temp files.
        FastaWriter(self.temp_query_path).save_queries(query)
        FastaWriter(self.temp_subject_path).save_queries(hit)

        self.blastx_2sequences()

        with open(self.temp_result_path) as result_file:
            return SearchIO.read(result_file, "blast-xml")

    def run_ged(self, final_result_path: str):
        blast_query_results = self.run_blast(self.base_query)
        hits_data = collect_hits(blast_query_results)

        if not hits_data:
            print("Not match find in BLAST at all")

        best_subset_score = 0
        for hit in hits_data:
            print("hit: " + str(hit))
            max_score = hit.get_best_hsps_normalize_score()
            # max_score = hit.get_best_hsps_score()
            print(max_score)
            if best_subset_score < max_score:
                best_subset_score = max_score

            print("hsps amount: ", len(hit.hsps))
            print(hit.hsps)

            # If there is only one HSP, there is no action that can be taken.
            if len(hit.hsps) == 1:
                print("Only one HSP")
                continue

            query_cut_points = self.get_hsps_by_detectors(hit.hsps, self.base_query)
            print("Cut points " + str(query_cut_points))

            if len(query_cut_points) < 2:  # In case the cut points in the edges
                continue

            subsets = generate_subsets(self.base_query, query_cut_points, self.maximum_active_cut_points)
            print("Number of subsets", len(subsets))

            subset_to_score = []
            for subset in subsets:
                print(subset)
                print(subset.query)

                blast_subset_results = self.run_blast(subset.merge_query)
                subset_hits_data = collect_hits(blast_subset_results)
                print(subset_hits_data)

                subset_hits_ids = [subset_hit.id for subset_hit in subset_hits_data]
                is_match, match_hit_id = match_strings(hit.id, subset_hits_ids)

                if not is_match:
                    print("Not Find the hit")
                    continue

                match_hit = next((subset_hit for subset_hit in subset_hits_data if subset_hit.id == match_hit_id), None)
                merge_query_score, merge_query_percent_coverage = match_hit.get_best_hsps_score_and_percent_coverage()

                adjusted_score = calculate_score_by_adjusted_alignment(subset.cut_out_fragments,
                                                                       merge_query_score) * merge_query_percent_coverage
                subset_to_score.append((subset.query, adjusted_score))

            print(subset_to_score)

            for subset, score_sum in subset_to_score:
                if best_subset_score < score_sum:
                    best_subset_score = score_sum

        # Write the final result in to the out file.
        with open(final_result_path, 'a+') as file:
            file.write(str(self.base_query) + "|" +
                       str(self.description).replace("|", "!") + "|" +
                       str(best_subset_score) + "|" +
                       str(self.get_time_running()) + "\n")

        print("Query: " + str(self.base_query) + "\n" +
              "Fasta Description: " + self.description + "\n" +
              "Best subset score: " + str(best_subset_score) + "\n" +
              "Time running: " + self.get_time_running() + "\n")

    def get_hsps_by_detectors(self, hsps, query):
        query_cut_points = []

        for cut_point_detector in self.cut_points_detectors:
            query_cut_points.append(cut_point_detector.detect_query_cut_points(hsps, query))

        query_cut_points = reduce(list.__add__, query_cut_points)  # Flat map the list of lists
        query_cut_points.sort()

        return query_cut_points
