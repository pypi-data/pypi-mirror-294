# datai/__init__.py

# Import essential functions from each module to make them accessible from the package
from .visualization import bar_chart, line_chart, scatter_plot, heatmap
from .data_cleaning import clean_missing_data, remove_outliers, normalize_data, get_cleaned_data
from .auto_plot import auto_plot

# Define the __all__ variable to specify what is accessible when using 'from datai import *'
__all__ = [
    "bar_chart",
    "line_chart",
    "scatter_plot",
    "heatmap",
    "clean_missing_data",
    "remove_outliers",
    "normalize_data",
    "get_cleaned_data",
    "auto_plot",
    "load_dataset"
]

# Version of the library
__version__ = "1.3"

# Brief description of the library (optional but helpful)
__description__ = "A Python library for easy data visualization, data cleaning, and automatic chart generation."

