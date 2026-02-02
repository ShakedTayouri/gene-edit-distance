from typing import List

from ged_flow.utils.Hsp import Hsp


class Hit:
    def __init__(self, id, length, hsps):
        self.id: str = id
        self.length: int = length
        self.hsps: List[Hsp] = hsps

    def get_best_hsps_score(self):
        return max(hsp.bitscore for hsp in self.hsps)

    def get_best_hsps_normalize_score(self):
        best_hsp = max(
            self.hsps,
            key=lambda hsp: hsp.bitscore * ((hsp.target_end_index - hsp.target_start_index) / self.length)
        )
        best_score = best_hsp.bitscore * ((best_hsp.target_end_index - best_hsp.target_start_index) / self.length)
        
        return best_score, best_hsp


    def get_best_hsps_score_and_percent_coverage(self):
        max_score = 0
        max_score_percent_coverage = 0

        for hsp in self.hsps:
            if hsp.bitscore > max_score:
                max_score = hsp.bitscore
                max_score_percent_coverage = (hsp.target_end_index - hsp.target_start_index) / self.length

        print("max_score: ", max_score)
        print("max_score_percent_coverage: ", max_score_percent_coverage)
        return max_score, max_score_percent_coverage

    def __repr__(self):
        return f'Hit(id={self.id}, length={self.length}, hsps={self.hsps})'
