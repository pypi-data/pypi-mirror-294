from setuptools import setup, find_packages

setup(
    name='SVMmargin',
    version='0.1.1',
    description='A package for cost-sensitive multiclass classification that increases the sensitivity of important classes by shifting the decision boundary between them according to a prioritization vector.',
    author='Eran Kaufman',
    author_email='erankfmn@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'cvxpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
