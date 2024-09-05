import numpy as np

class UnsupervisedEmbeddingQualityEvaluation:
    
    @staticmethod
    def RankMe(M, epsilon=1e-7):
        U, Sigma, Vt = np.linalg.svd(M, full_matrices=False)
        pk = Sigma / (np.sum(Sigma)) + epsilon
        min_dim = min(M.shape)
        entropy = -np.sum(pk[:min_dim] * np.log(pk[:min_dim]))
        rankme_value = np.exp(entropy)
        return rankme_value

    @staticmethod
    def NESum(M):
        C = np.cov(M, rowvar=False)
        Lambda, U = np.linalg.eig(C)
        idx = np.argsort(Lambda)[::-1]
        Lambda = Lambda[idx]
        U = U[:, idx]
        n = min(C.shape)
        NESum = np.sum([Lambda[i] / (Lambda[0]) for i in range(n)])
        return NESum
    
    @staticmethod
    def Stable_rank(M):
        fro_norm = np.linalg.norm(M, 'fro')
        two_norm = np.linalg.norm(M, 2)
        numerical_rank = fro_norm**2 / two_norm**2
        return numerical_rank