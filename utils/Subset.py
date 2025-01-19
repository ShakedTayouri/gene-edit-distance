import re
from typing import List

from utils.CutOutFragments import CutOutFragment


def find_cut_out_fragments(input_string) -> List[CutOutFragment]:
    # This pattern matches sequences of hyphens
    pattern = r"-+"
    # Find all matches of the pattern
    matches = [match.span() for match in re.finditer(pattern, input_string)]
    # Adjust the end index to be inclusive
    ranges = [CutOutFragment(start, end) for start, end in matches]

    return ranges


class Subset:
    def __init__(self, query, cut_points):
        self.query = query
        self.cut_points = sorted(cut_points)
        self.merge_query = query.replace('-', '')
        self.cut_out_fragments: List[CutOutFragment] = find_cut_out_fragments(query)

    def __eq__(self, other):
        Subset.validate_subset(other)
        return self.query == other.query and sorted(self.cut_points) == sorted(other.cut_points)

    def __lt__(self, other):
        Subset.validate_subset(other)
        return (self.query, self.cut_points) < (other.query, other.cut_points)

    def __str__(self):
        return f'Query: {str(self.query)} cut_points {str(self.cut_points)}'

    def __repr__(self):
        return f'Subset(query={self.query}, cut_points={self.cut_points})'

    @staticmethod
    def validate_subset(object):
        # Check the object type.
        if not isinstance(object, Subset):
            raise ValueError("The type of the object isn't Subset")
