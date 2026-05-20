class Hsp:
    def __init__(self, query_start_index, query_end_index, target_start_index, target_end_index, bitscore, query_strand, hit_strand):
        self.query_start_index: int = query_start_index
        self.query_end_index: int = query_end_index
        self.target_start_index: int = target_start_index
        self.target_end_index: int = target_end_index
        self.bitscore: int = bitscore
        self.query_strand = query_strand
        self.hit_strand = hit_strand

    def __repr__(self):
        return f'HSP(query_start_index={self.query_start_index}, query_end_index={self.query_end_index}, target_start_index={self.target_start_index}, target_end_index={self.target_end_index}, bitscore={self.bitscore}), query_strand={self.query_strand}), hit_strand={self.hit_strand})' 
