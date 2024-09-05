# Embedding Quality Evaluation

A Python package for unsupervised embedding quality evaluation.

## Installation

You can install the package using pip:

```bash
pip install embedding_quality




import numpy as np
from embedding_quality import UnsupervisedEmbeddingQualityEvaluation

# Create a sample matrix
M = np.random.rand(100, 50)

# Use the evaluation methods
rankme = UnsupervisedEmbeddingQualityEvaluation.RankMe(M)
nesum = UnsupervisedEmbeddingQualityEvaluation.NESum(M)
stable_rank = UnsupervisedEmbeddingQualityEvaluation.Stable_rank(M)

print(f"RankMe: {rankme}")
print(f"NESum: {nesum}")
print(f"Stable Rank: {stable_rank}")