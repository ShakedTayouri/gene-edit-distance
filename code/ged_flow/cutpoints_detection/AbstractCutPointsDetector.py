from abc import ABC, abstractmethod


class BaseCutPointsDetector(ABC):
    @abstractmethod
    def detect_query_cut_points(self, hsps, query):
        """
        Detect cut points.
        :param: hsps per hit.
        :return: List of cut points.
        """
        pass
