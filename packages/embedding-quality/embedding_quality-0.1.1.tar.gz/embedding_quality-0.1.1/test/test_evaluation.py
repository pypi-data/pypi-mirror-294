import unittest
import numpy as np
from embedding_quality import UnsupervisedEmbeddingQualityEvaluation

class TestUnsupervisedEmbeddingQualityEvaluation(unittest.TestCase):

    def setUp(self):
        self.M = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_RankMe(self):
        result = UnsupervisedEmbeddingQualityEvaluation.RankMe(self.M)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_NESum(self):
        result = UnsupervisedEmbeddingQualityEvaluation.NESum(self.M)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_Stable_rank(self):
        result = UnsupervisedEmbeddingQualityEvaluation.Stable_rank(self.M)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
        self.assertLessEqual(result, min(self.M.shape))

    def test_RankMe_identity_matrix(self):
        I = np.eye(3)
        result = UnsupervisedEmbeddingQualityEvaluation.RankMe(I)
        self.assertAlmostEqual(result, 3.0, places=6)

    def test_NESum_identity_matrix(self):
        I = np.eye(3)
        result = UnsupervisedEmbeddingQualityEvaluation.NESum(I)
        self.assertAlmostEqual(result, 3.0, places=6)

    def test_Stable_rank_identity_matrix(self):
        I = np.eye(3)
        result = UnsupervisedEmbeddingQualityEvaluation.Stable_rank(I)
        self.assertAlmostEqual(result, 3.0, places=6)

if __name__ == '__main__':
    unittest.main()