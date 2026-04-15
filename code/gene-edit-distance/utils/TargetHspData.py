class TargetHspData:
    def __init__(self, query_start_index, query_end_index, query, target_start_index, target_end_index, bitscore,
                 target_strand):
        self.target_start_index: int = target_start_index
        self.target_end_index: int = target_end_index
        self.bitscore: int = bitscore
        self.data = query[query_start_index: query_end_index]
        self.target_strand = target_strand

    def __repr__(self):
        return (f"TargetHspData("
                f"target_start_index={self.target_start_index}, "
                f"target_end_index={self.target_end_index}, "
                f"bitscore={self.bitscore}, "
                f"data='{self.data}')")
