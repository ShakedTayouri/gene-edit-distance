import os
import argparse
import logging
from typing import List, Tuple

from GedRunner import GedRunner
from cutpoints_detection.HypotheticalCutPointsDetector import HypotheticalCutPointsDetector
from io_utils.FastaReader import FastaReader
from HSPsReordering import HSPsReordering
from BlastRunner import BlastRunner

SequenceRecord = Tuple[str, str]
PENALTY_REMOVAL = 1


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GED pipeline runner")

    parser.add_argument("order_address", help="Input FASTA file")
    parser.add_argument("result_path", help="Output directory")

    parser.add_argument(
        "--reorder",
        action="store_true",
        help="Enable HSP-based reordering"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        help="Batch size (required when --reorder is used)"
    )

    args = parser.parse_args()

    if args.reorder and args.batch_size is None:
        parser.error("--batch-size is required when --reorder is enabled")

    if args.batch_size is not None and args.batch_size <= 0:
        parser.error("--batch-size must be a positive integer")

    return args


def load_records(fasta_path: str) -> List[SequenceRecord]:
    reader = FastaReader(fasta_path)
    records = reader.load_queries()

    if not records:
        raise ValueError("No sequences found in FASTA file")

    return [(str(seq), str(desc)) for seq, desc in records]


def run_without_reorder(
        records: List[SequenceRecord],
        result_path: str,
        blast_runner
) -> None:
    logging.info("Running GED without reordering")

    for query, description in records:
        runner = GedRunner(
            query,
            description,
            [HypotheticalCutPointsDetector()],
            blast_runner
        )

        subset, score = runner.run_ged()
        runner.save_ged_result(result_path, subset, score)


def run_with_reorder(
        records: List[SequenceRecord],
        batch_size: int,
        result_path: str,
        blast_runner
) -> None:
    logging.info("Running GED with reordering (batch_size=%d)", batch_size)

    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        queries = [q for q, _ in batch]
        descriptions = [d for _, d in batch]

        best_score = float("-inf")
        best_subset = None
        best_runner = None

        reordering_runner = HSPsReordering(queries, blast_runner)
        reordered_queries = reordering_runner.run_reorder_query()

        for reordered_query, hsp_count in reordered_queries:
            runner = GedRunner(
                reordered_query,
                "> Reorder query",
                [HypotheticalCutPointsDetector()],
                blast_runner
            )

            subset, score = runner.run_ged()
            score -= PENALTY_REMOVAL * hsp_count

            if score > best_score:
                best_score = score
                best_subset = subset
                best_runner = runner

        if best_runner is None:
            logging.warning("No valid GED result for batch starting at %d", i)
            continue

        best_runner.save_ged_result(
            result_path,
            best_subset,
            best_score,
            queries,
            descriptions
        )


def main() -> None:
    setup_logging()
    args = parse_args()

    logging.info("Loading FASTA file: %s", args.order_address)
    records = load_records(args.order_address)
    blast_runner = BlastRunner(config_path="config.ini")

    if args.reorder:
        run_with_reorder(
            records=records,
            batch_size=args.batch_size,
            result_path=args.result_path,
            blast_runner=blast_runner
        )
    else:
        run_without_reorder(
            records=records,
            result_path=args.result_path,
            blast_runner=blast_runner
        )


if __name__ == "__main__":
    main()
