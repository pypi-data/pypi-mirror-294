from setuptools import setup, find_packages
from importlib.metadata import version

setup(
    name='datai',
    version='1.2',
    description='A library for data visualization and cleaning',
    author='M Ans',
    author_email='m.ans.cs@outlook.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'seaborn',
        'matplotlib',
        'setuptools',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',    # Python version requirement
)
