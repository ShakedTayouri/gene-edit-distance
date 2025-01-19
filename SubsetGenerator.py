import configparser
import os

from utils.Node import Node
from utils.PriorityQueue import PriorityQueue
from utils.Subset import Subset


def calculate_cost(query, current_query) -> int:
    config = configparser.ConfigParser()
    config.read(os.path.dirname(__file__) + '/config.ini')

    rm = int(config['calculation_weights']['rm'])
    return (len(query) - len(current_query)) * rm


def generate_subsets(origin_query, query_cut_points, maximum_active_cut_points):
    # Create a priority queue to store live nodes of search tree
    pq = PriorityQueue()

    first_part_of_query = origin_query[:query_cut_points[0]]
    cost = calculate_cost(origin_query, query_cut_points)

    # Create the root node
    root = Node(None, first_part_of_query, [], query_cut_points, cost, 0)

    # Add root to list of live nodes
    pq.push(root)

    subsets = []
    while not pq.empty():
        # Find a live node with the least estimated cost and delete it from the list of live nodes
        minimum = pq.pop()

        if not minimum.potential_cut_points:
            minimum.query = minimum.query + origin_query[len(minimum.query):]
            if minimum.query != origin_query and minimum.query.count('-') != len(origin_query) and len(
                    minimum.active_cut_points) % 2 == 0:
                subsets.append(Subset(minimum.query, minimum.active_cut_points))
        else:
            potential_cut_point = minimum.potential_cut_points.pop(0)

            add_child_without_next_potential(minimum.cost, minimum, pq, origin_query, potential_cut_point)
            if len(minimum.active_cut_points) + 1 <= maximum_active_cut_points:
                add_child_with_next_potential(minimum, pq, origin_query, potential_cut_point)

    return subsets


def add_child_with_next_potential(minimum, pq, origin_query, potential_cut_point):
    """
    Add a child node with the next potential cut point to the priority queue.
    """
    active_cut_points = minimum.active_cut_points
    query_with_gaps = get_query_with_gaps(minimum, origin_query, potential_cut_point, active_cut_points)

    active_cut_points.append(potential_cut_point)

    pq.push(Node(minimum, query_with_gaps, active_cut_points, minimum.potential_cut_points,
                 calculate_cost(minimum.query, active_cut_points), minimum.level + 1))


def get_query_with_gaps(minimum, origin_query, potential_cut_point, active_cut_points):
    """
    Get the query with gaps based on the active cut points and the potential cut point.
    """
    if len(active_cut_points) % 2 != 0:
        last_active_cut_point = active_cut_points[-1]
        return get_gap_query_by_cut_point(minimum.query, last_active_cut_point, potential_cut_point)
    else:
        return query_without_gaps(minimum, origin_query, potential_cut_point)


def query_without_gaps(minimum, origin_query, potential_cut_point):
    """
    Get the query without gaps up to the potential cut point.
    """
    return minimum.query + origin_query[len(minimum.query):potential_cut_point]


def add_child_without_next_potential(cost, minimum, pq, origin_query, potential_cut_point):
    """
    Add a child node without the next potential cut point to the priority queue.
    """
    new_query = get_new_query(minimum, origin_query, potential_cut_point)
    pq.push(Node(minimum, new_query, minimum.active_cut_points, minimum.potential_cut_points,
                 cost, minimum.level + 1))


def get_new_query(minimum, origin_query, potential_cut_point):
    """
    Get the new query based on the active cut points.
    """
    if len(minimum.active_cut_points) % 2 != 0:
        return minimum.query
    else:
        return query_without_gaps(minimum, origin_query, potential_cut_point)


def get_gap_query_by_cut_point(query, start_cut_point, end_cut_point):
    """
    Get the query with gaps represented by '-' characters between the start and end cut points.
    """
    return query + '-' * (end_cut_point - start_cut_point)
