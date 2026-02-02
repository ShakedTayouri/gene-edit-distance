from Bio.Seq import reverse_complement

from hit_collector.HitCollector import collect_hits
from ged_flow.utils.TargetHspData import TargetHspData


class HSPsReordering:
    def __init__(self, query_list, blast_runner):
        """
        :param query_list: list of query sequences
        :param blast_runner: instance of BlastRunner
        """
        self.query_list = query_list
        self.blast_runner = blast_runner

    def run_reorder_query(self):
        hit_id_to_sub_target_data = {}

        for query in self.query_list:
            blast_query_results = self.blast_runner.run_blast(query)
            hits_data = collect_hits(blast_query_results)

            for hit in hits_data:
                hit_id_to_sub_target_data.setdefault(hit.id, [])

                for hsp in hit.hsps:
                    hit_id_to_sub_target_data[hit.id].append(
                        TargetHspData(
                            hsp.query_start_index,
                            hsp.query_end_index,
                            query,
                            hsp.target_start_index,
                            hsp.target_end_index,
                            hsp.bitscore,
                            hsp.hit_strand
                        )
                    )

        if not hit_id_to_sub_target_data:
            print("Not match find in BLAST at all")
            return set()

        hit_id_to_new_string = {}
        for hit_id, sub_target_data in hit_id_to_sub_target_data.items():
            if len(sub_target_data) > 1:
                hit_id_to_new_string[hit_id] = self.reorder_hsp_data(sub_target_data)

        return set(hit_id_to_new_string.values())

    def reorder_hsp_data(self, hsp_data_list, separator='-' * 10):
        if not hsp_data_list:
            return "", 0

        # Sort HSPs by target coordinates
        sorted_data = sorted(
            hsp_data_list,
            key=lambda hsp: min(hsp.target_start_index, hsp.target_end_index)
        )

        concatenated_result = []

        for i, hsp in enumerate(sorted_data):
            if i > 0:
                concatenated_result.append(separator)

            # Normalize orientation of HSPs
            if hsp.target_strand == -1:
                concatenated_result.append(reverse_complement(hsp.data))
            else:
                concatenated_result.append(hsp.data)

        return "".join(concatenated_result), len(concatenated_result)
