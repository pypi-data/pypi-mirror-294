from setuptools import setup, find_packages
from importlib.metadata import version

setup(
    name='datai',
    version='1.1',
    description='A library for data visualization and cleaning',
    author='M Ans',
    author_email='m.ans.cs@outlook.com',
    packages=find_packages(),
    install_requires=[
        'pandas==2.0.3',
        'numpy==1.25.1',
        'seaborn==0.12.2',
        'matplotlib==3.8.0',
        'setuptools>=68.0.0',
        'scikit-learn==1.3.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',    # Python version requirement
)
