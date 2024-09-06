import numpy as np
from numpy.linalg import LinAlgError
from sklearn.base import BaseEstimator, ClassifierMixin
from cvxpy import *
#########################################
class ImbalancedSVM(BaseEstimator, ClassifierMixin):
    """ImbalancedSVM class
    An algorithm for imbalanced cost sensetive classification problems
    using imbalanced margins.
    """

    def linearKernel(self, x1, x2):
        return x1.dot(x2.T)  # /(np.linalg.norm(x1)*np.linalg.norm(x2))

    def RBFKernel(self, x1, x2, gamma=1):
        return np.exp(-np.linalg.norm((x2 - x1)) / self.gamma)

    def polyKernel(self, x1, x2, degree=2):
        return (1 + x1.dot(x2.T)) ** self.degree

    def __init__(self, class_weight=None, kernel='linear', degree=3, gamma=1, C=1):

        if isinstance(class_weight, dict):
            self.class_weight = np.array(list(class_weight.values()))
        else:
            self.class_weight = class_weight

        self.kernel = kernel
        if (kernel == 'linear'):
            self.ker = self.linearKernel
        if (kernel == 'rbf'):
            self.ker = self.RBFKernel
        if (kernel == 'poly'):
            self.ker = self.polyKernel

        self.degree = degree
        self.gamma = gamma
        self.C = C
        self.dict = {}

    def fit1(self, X, y, num_iter=30):
        """
          An attempt to solve the dual using SGD
        """
        # add intercept
        temp = np.ones([X.shape[0], 1])
        X = np.hstack((X, temp))
        self.y = np.unique(y)
        self.K = len(np.unique(y))
        self.alpha = np.zeros([X.shape[0], self.K])
        self.num_iter = num_iter
        for index, value in enumerate(self.y):
            self.dict[value] = index

        # self.class_weight=[1,1,1,1]
        #         if (sample_weight is not None):
        #             self.class_weight = sample_weight

        for t in range(X.shape[0] * self.num_iter):
            index = t % X.shape[0]  # np.random.randint(0, X.shape[0])#
            yt = self.dict[y[index]]
            for j in range(len(self.y)):
                if (yt == j):
                    delta = 1
                else:
                    delta = -1
                sum = 0
                for i in range(X.shape[0]):
                    sum += self.alpha[i, j] * self.ker(X[i, :], X[index, :])

                if (self.class_weight[yt] >= delta * sum):
                    self.alpha[index, j] += delta

        self.w2 = (X.T.dot(self.alpha)).T
        self.sv = X
        #    print("alphas are:", self.alpha)
        return self

    def fit2(self, X, y, sample_weight=None):

        """
          An attempt to solve the primal using convex optimization
        """
        # add intercept

        self.y = np.unique(y)
        self.K = len(np.unique(y))
        self.w2 = Variable([self.K, X.shape[1]])
        self.b = Variable(self.K)
        for index, value in enumerate(self.y):
            self.dict[value] = index

        if (sample_weight is not None):
            self.class_weight = sample_weight

        obj = 0
        # for all points
        for i in range(X.shape[0]):
            # for all classes
            for j in range(self.K):
                if y[i] == self.y[j]:
                    obj += pos(self.class_weight[self.dict[y[i]]] - (self.w2[j, :] @ (X[i, :]).T + self.b[j]))
                else:
                    obj += pos(self.class_weight[y[i]] + (self.w2[j, :] @ (X[i, :]).T + self.b[j]))

        reg = norm(self.w2)
        Problem(Minimize(obj + reg)).solve(solver=SCS)
        return self

    def predict1(self, X):
        temp = np.ones([X.shape[0], 1])
        X = np.hstack((X, temp))
        y = np.empty(X.shape[0])
        for i in range((X.shape[0])):
            sum = np.zeros(self.K)
            for j in range(self.K):
                for k in range(self.sv.shape[0]):
                    sum[j] += self.alpha[k, j] * self.ker(self.sv[k], X[i, :])
                sum[j] = (sum[j]) / self.class_weight[j]
            y[i] = self.y[sum.argmax()]
        return y

    def predict2(self, X):
        y = np.empty(X.shape[0])
        for i in range((X.shape[0])):
            # print("eran:", X[i, :].shape,X[i, :].reshape(1,-1).shape,X[i, :].reshape(1,-1))
            r = (np.matmul(X[i, :].reshape(1, -1), self.w2.value.T) + self.b.value.T) / self.class_weight
            y[i] = self.y[r.argmax()]
        return y

    def fit(self, X, y):
        if (self.kernel == 'linear'):
            return self.fit2(X, y)
        else:
            return self.fit1(X, y)

    def predict(self, X):
        if (self.kernel == 'linear'):
            return self.predict2(X)
        else:
            return self.predict1(X)
