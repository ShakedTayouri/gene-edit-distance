from utils.Hit import Hit
from utils.Hsp import Hsp
from typing import List


def collect_hits(query_results: list) -> List[Hit]:
    """
    Analyze the blast result. Collect all the hsps from the hits list.
    parm all_hits: List for all the hits from blast.
    :return: a dictionary with key - hit id (the id of the hit in the searched DB),
            value - list of hsp - part of the query that create the hit. include (query_start, query_end, hit_start, hit_end)
    """

    hits_data = []

    for hit in query_results:
        hsps = []
        for hsp in hit.hsps:
            hsps.append(Hsp(hsp.query_range[0], hsp.query_range[1],
                            hsp.hit_range[0], hsp.hit_range[1], hsp.bitscore))

        hits_data.append(Hit(hit.id, hit.seq_len, hsps))

    return hits_data
