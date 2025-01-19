import configparser
import os

from score_calculator.SequenceAlignment import sequence_alignment


def calculate_score_by_gap_penalty(origin_string, transformed_string):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.dirname(script_dir)
    config_path = os.path.join(project_dir, 'config.ini')

    config = configparser.ConfigParser()
    config.read(config_path)

    rm = int(config['calculation_weights']['rm'])
    pmm = int(config['calculation_weights']['pmm'])
    pgo = int(config['calculation_weights']['pgo'])
    pgx = int(config['calculation_weights']['pgx'])

    matched, mismatched, gaps_opened, gaps_extended = sequence_alignment(origin_string, transformed_string)

    return matched * rm - mismatched * pmm - gaps_opened * pgo - gaps_extended * pgx


def get_gaps_penalty(cut_out_fragments, pgo, pgx):
    gaps_penalty = 0
    for cut_out_fragment in cut_out_fragments:
        gaps_penalty += pgo + pgx * (cut_out_fragment.end - cut_out_fragment.start)

    return gaps_penalty
