# SVMmargin

**Version:** 0.1.0  
**License:** MIT License  
**Author:** Eran Kaufman 
**Email:** erankfmn@gmail.com 

## Overview

SVMmargin is a Python package designed to address the problem of imbalanced data and cost-sensitive multiclass classification. The package increases the sensitivity of important classes by shifting the decision boundary between them according to a prioritization vector. This results in a tighter error bound for critical classes while reducing overall out-of-sample error.

The package supports various kernel methods, including linear, RBF, and polynomial kernels, and is adaptable to neural networks. It also includes generalization bounds and demonstrates Fisher consistency.

## Features

- **Imbalanced Classification:** Adjusts the imbalance of classes based on their inverse size.
- **Cost-Sensitive Classification:** Adjusts the sensitivity of classes based on their importance.
- **Apportioned Margin Framework:** Efficiently shifts decision boundaries according to a prioritization vector.
- **Support for Multiple Kernels:** Includes linear, RBF, and polynomial kernels.
- **Neural Network Adaptation:** Can be integrated with neural networks.
- **Fisher Consistency:** Ensures the consistency of the classifier.
- **Generalization Bounds:** Provides theoretical guarantees on performance.

## Installation

You can install the package directly from PyPI using pip:

```bash
pip install SVMmargin
```

## Usage

### Here is a basic example of how to use the package:
### linear comparison for different costs

```python
import numpy as np
from SVMmargin import ImbalancedSVM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Generate synthetic data
N = 20
s = np.random.normal(0, 0.5, (N, 2))
X1 = s + [0, 0]
X2 = s + [0, 6]
X3 = s + [6, 6]
X4 = s + [6, 0]

X = np.concatenate([X1, X2, X3, X4])
y = np.concatenate([0 * np.ones(N), 1 * np.ones(N), 2 * np.ones(N), 3 * np.ones(N)])
y = y.astype(int)

# Define class weights
thetas = np.array([
    [1, 1, 1, 1],
    [10, 1, 1, 1],
    [10, 10, 1, 1],
    [10, 10, 10, 1],
])

# Normalize the data
X = MinMaxScaler().fit_transform(X)

# Train and plot the decision boundaries for each set of weights
fig, sub = plt.subplots(2, 2)
for theta, title, ax in zip(thetas, thetas, sub.flatten()):
    cls = ImbalancedSVM(kernel='linear', class_weight=theta)
    cls.fit(X, y)
    plot_contours(ax, cls, xx, yy, xy, cmap=plt.cm.coolwarm, alpha=0.8)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_title(title)
plt.show()
```
### polynomial kernel example
``` python
#polynomial kernel example
N=100
X = np.random.normal(0, 0.5,(N,2))
y=np.zeros(N)
for index in range(N):
    if ((X[index][0]**2+X[index][1]**2)<0.3):
        y[index]=1
    else:
        y[index]=-1
xx, yy = make_meshgrid(X[:, 0], X[:, 1])
xy=np.c_[xx.ravel(), yy.ravel()]
fig, sub = plt.subplots(1,2)
for theta, title, ax in zip(thetas,thetas, sub.flatten()):
    cls = ImbalancedSVM(kernel='poly',class_weight=theta)
    cls.fit(X,y)
    plot_contours(ax, cls, xx, yy,xy,cmap=plt.cm.coolwarm, alpha=0.8)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')

  #  ax.set_xlim(xx.min(), xx.max())
  #  ax.set_ylim(yy.min(), yy.max())

    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_title(title)
    

plt.show()
```
## Available Kernels

- Linear Kernel: `linear`
- RBF Kernel: `rbf`
- Polynomial Kernel: `poly`

You can select the kernel by specifying the `kernel` parameter when creating an instance of `ImbalancedSVM`.

## Class Weights

The `class_weight` parameter allows you to assign different importance to different classes. It accepts a dictionary where keys are class labels, and values are the corresponding weights.

## Examples

Here are a few usage examples:

### Linear Kernel Example

```python
cls = ImbalancedSVM(kernel='linear', class_weight={0: 10, 1: 1})
cls.fit(X, y)
predictions = cls.predict(X_test)
```

### RBF Kernel Example

```python
cls = ImbalancedSVM(kernel='rbf', gamma=0.5, class_weight={0: 1, 1: 10})
cls.fit(X, y)
predictions = cls.predict(X_test)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- scikit-learn for providing the foundational tools for machine learning in Python.
- Matplotlib for data visualization.


## References

If you would like to learn more about the theoretical background and the research behind this package, please refer to the following article:
Please cite this article when using this package!
- **Apportioned Margin Approach for Cost Sensitive Large Margin Classifiers**  
Gottlieb, LA., Kaufman, E. & Kontorovich, A. Apportioned margin approach for cost sensitive large margin classifiers. Ann Math Artif Intell 89, 1215–1235 (2021). https://doi.org/10.1007/s10472-021-09776-w



## Contact

If you have any questions or suggestions, feel free to reach out at erankfmn@gmail.com.