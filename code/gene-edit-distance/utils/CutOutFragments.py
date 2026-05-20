class CutOutFragment:
    def __init__(self, start, end):
        self.start: int = start
        self.end: int = end

        # Check if this cut point is valid.
        self.validate()

    def validate(self):
        if not isinstance(self.start, int) or \
                not isinstance(self.end, int):
            raise ValueError("Invalid cut point type.")

        if self.start < 0:
            raise ValueError("Invalid starting point.")

        if self.start > self.end:
            raise ValueError(
                "The ending point: " + str(self.end) + " must be bigger then the start point: " + str(self.start))

    def __lt__(self, other):
        CutOutFragment.validate_cut_point_type(other)
        return self.start < other.start

    def __le__(self, other):
        CutOutFragment.validate_cut_point_type(other)
        return self.start <= other.start

    def __eq__(self, other):
        CutOutFragment.validate_cut_point_type(other)
        return self.start == other.start and self.end == other.end

    def __add__(self, other):
        CutOutFragment.validate_cut_point_type(other)

    def __str__(self):
        return f'Start: {str(self.start)} End: {str(self.end)}'

    def __len__(self):
        return self.end - self.start

    def __repr__(self):
        return f'CutPoint(start={self.start}, end={self.end})'

    @staticmethod
    def validate_cut_point_type(object):
        # Check the object type.
        if not isinstance(object, CutOutFragment):
            raise ValueError("The type of the object isn't CutOutFragments")

    def is_contains(self, other):
        if self.start >= other.start and self.end <= other.end:
            return True
        if other.start >= self.start and other.end <= self.end:
            return True
        return False

    def is_overlaps(self, other):
        if self.start <= other.start <= self.end <= other.end:
            return True
        if other.start <= self.start <= other.end <= self.end:
            return True
        return False
