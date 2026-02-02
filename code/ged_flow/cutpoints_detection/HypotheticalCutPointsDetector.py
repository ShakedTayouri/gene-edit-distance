from ged_flow.cutpoints_detection.AbstractCutPointsDetector import BaseCutPointsDetector


class HypotheticalCutPointsDetector(BaseCutPointsDetector):
    def detect_query_cut_points(self, hsps, query):
        """
        Detect cut points by the hsps per hit.
        :param: hsps per hit.
        :return: List of cut points
        """

        cut_points = []

        for hsp in hsps:
            cut_points.append(hsp.query_start_index)
            cut_points.append(hsp.query_end_index)

        cut_points.sort()
        return sorted(list(set(cut_points[1:-1])))
