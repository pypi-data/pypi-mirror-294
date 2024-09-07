import unittest
import pandas as pd
from balance_point_clustering import balance_point_clustering

class TestBalancePointClustering(unittest.TestCase):

    def setUp(self):
        self.data = {
            'Feature1': [1, 2, 5, 7, 14],
            'Feature2': [1, 2, 9, 14, 199],
        }
        self.df = pd.DataFrame(self.data)

    def test_cluster_with_specified_no_clusters(self):
        clusters = balance_point_clustering(self.df, no_clusters=3)
        self.assertEqual(len(clusters), 3)

    def test_cluster_with_auto_no_clusters(self):
        clusters = balance_point_clustering(self.df)
        self.assertGreaterEqual(len(clusters), 1)

if __name__ == '__main__':
    unittest.main()
