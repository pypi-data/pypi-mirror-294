from setuptools import setup, find_packages

setup(
    name='grid_search_utils',
    version='0.1',
    description='Utility functions for plotting and tabulating GridSearchCV results',
    author='Diogo Hajjar',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/grid_search_utils',
    packages=find_packages(),
    install_requires=[
        'xgboost',
        'scikit-learn',
        'pandas',
        'plotly',
        'matplotlib',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
