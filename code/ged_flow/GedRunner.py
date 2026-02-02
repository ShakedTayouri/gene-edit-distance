# ged_runner.py
import os
import time
import csv
import re
from functools import reduce

from SubsetGenerator import generate_subsets
from cutpoints_detection.AbstractCutPointsDetector import BaseCutPointsDetector
from hit_collector.HitCollector import collect_hits
from score_calculator.ScoreByAdjustedAlignment import calculate_score_by_adjusted_alignment

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

GED_TOXIN_THRESHOLD = float(config["ged_results"]["ged_toxin_threshold"])


def match_strings(main_string, search_strings):
    pattern = r'\|[A-Z0-9]+'
    matches_main = set(re.findall(pattern, main_string))

    for search_string in search_strings:
        matches_search = set(re.findall(pattern, search_string))
        if matches_main & matches_search:
            return True, search_string

    return False, ''


class GedRunner:
    def __init__(self, base_query, description, cut_points_detectors, blast_runner):
        self.start_time = time.time()
        self.base_query = base_query
        self.description = description
        self.blast_runner = blast_runner

        self.cut_points_detectors = []
        for detector in cut_points_detectors:
            self.cut_points_detectors.append(detector)

        self.maximum_active_cut_points = 3  # or pass via config

    def get_time_running(self):
        return str(time.time() - self.start_time)

    def run_ged(self):
        blast_query_results = self.blast_runner.run_blast(self.base_query)
        hits_data = collect_hits(blast_query_results)

        best_subset_score = 0
        best_subset = None

        for hit in hits_data:
            max_score, hsp_with_max_score = hit.get_best_hsps_normalize_score()
            if best_subset_score < max_score:
                best_subset_score = max_score
                best_subset = hsp_with_max_score

            if len(hit.hsps) == 1:
                continue

            query_cut_points = self.get_hsps_by_detectors(hit.hsps, self.base_query)
            if len(query_cut_points) < 2:
                continue

            subsets = generate_subsets(
                self.base_query,
                query_cut_points,
                self.maximum_active_cut_points
            )

            for subset in subsets:
                blast_subset_results = self.blast_runner.run_blast(subset.merge_query)
                subset_hits_data = collect_hits(blast_subset_results)

                subset_hit_ids = [h.id for h in subset_hits_data]
                is_match, match_hit_id = match_strings(hit.id, subset_hit_ids)

                if not is_match:
                    continue

                match_hit = next(
                    h for h in subset_hits_data if h.id == match_hit_id
                )

                score, coverage = match_hit.get_best_hsps_score_and_percent_coverage()
                adjusted_score = (
                    calculate_score_by_adjusted_alignment(
                        subset.cut_out_fragments, score
                    ) * coverage
                )

                if adjusted_score > best_subset_score:
                    best_subset_score = adjusted_score
                    best_subset = subset.query

        return best_subset, best_subset_score

    def get_hsps_by_detectors(self, hsps, query):
        cut_points = []
        for detector in self.cut_points_detectors:
            cut_points.extend(detector.detect_query_cut_points(hsps, query))
        return sorted(cut_points)

    def save_ged_result(self, final_result_path, best_subset, best_subset_score, base_query=None, description=None):
        if base_query is None:
            base_query = [self.base_query]
        if description is None:
            description = [self.description]

        toxin_flag = 1 if best_subset_score > GED_TOXIN_THRESHOLD else 0
        
        file_exists = os.path.isfile(final_result_path)
        with open(final_result_path, 'a+', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    "Description",
                    "Query",
                    "Query with gaps between optimal HSPs",
                    "GED score",
                    "Toxin Flag",
                    "Running Time (seconds)"
                ])

            writer.writerow([
                self.description,
                self.base_query,
                best_subset,
                best_subset_score,
                toxin_flag,
                self.get_time_running()
            ])
