import configparser
import os

from score_calculator.ScoreByGapPenalty import get_gaps_penalty


def get_sorted_cut_out_fragments(cut_out_fragments):
    """
        Args:
            cut_out_fragments: A list of CutOutFragments, where each CutOutFragments contains two elements: the start and end points.

        Returns:
            A sorted tuple by longest cut points in the given list.
        """
    return sorted(cut_out_fragments, key=lambda x: x.end - x.start)


def calculate_score_by_adjusted_alignment(cut_out_fragments, merge_query_score):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.dirname(script_dir)
    config_path = os.path.join(project_dir, 'config.ini')

    config = configparser.ConfigParser()
    config.read(config_path)

    penalty_gap_opening = int(config['calculation_weights']['pgo'])
    penalty_gap_extension = int(config['calculation_weights']['pgx'])
    penalty_removal = int(config['calculation_weights']['prm'])
    gap_removal_probability = float(config['calculation_weights']['grp'])

    # Calculate initial gaps' penalty, all the gaps calculated
    gaps_penalty = get_gaps_penalty(cut_out_fragments, penalty_gap_opening,
                                    penalty_gap_extension)
    max_score = merge_query_score - gaps_penalty
    print("Score with gaps: " + str(max_score))

    sorted_cut_out_fragments = get_sorted_cut_out_fragments(cut_out_fragments)
    print("Sorted cut out fragments: " + str(sorted_cut_out_fragments))

    # Every run take the longest gap and cut it instead of the gap
    for gaps_to_be_removed in range(1, len(sorted_cut_out_fragments) + 1):
        gaps_penalty = gaps_penalty - penalty_gap_opening - penalty_gap_extension * len(
            sorted_cut_out_fragments.pop()) + penalty_removal

        adjusted_alignment_score = merge_query_score + pow(gap_removal_probability, gaps_to_be_removed) * - gaps_penalty
        max_score = max(max_score, adjusted_alignment_score)
        print("Max score: " + str(max_score))

    return max_score
