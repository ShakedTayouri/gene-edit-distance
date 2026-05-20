import copy


class Node:

    def __init__(self, parent, query, active_cut_points, potential_cut_points, cost, level):
        # Stores the parent node of the current node helps in tracing path when the answer is found
        self.parent = parent
        self.query = query
        self.potential_cut_points = copy.deepcopy(potential_cut_points)
        self.active_cut_points: list = copy.deepcopy(active_cut_points)
        # Stores the number of misplaced tiles
        self.cost = cost
        # Stores the number of moves so far
        self.level = level

    # This method is defined so that the priority queue is formed based on the cost variable of the objects
    def __lt__(self, nxt):
        return self.cost < nxt.cost
