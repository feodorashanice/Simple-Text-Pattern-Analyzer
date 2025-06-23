# src/__init__.py
"""
Simple Text Pattern Analysis package
"""

__version__ = "1.0.0"

# src/algorithms/__init__.py
"""
Pattern matching algorithms module
"""

from src.algorithms.pattern_matching import PatternMatcher

__all__ = ['PatternMatcher']

# src/analysis/__init__.py
"""
Text analysis module
"""

from src.analysis.ngram_analyzer import NgramAnalyzer

__all__ = ['NgramAnalyzer']

# src/data/__init__.py
"""
Data handling module
"""

from src.data.downloader import DataDownloader

__all__ = ['DataDownloader']

# src/utils/__init__.py
"""
Utility functions module
"""

from src.utils.text_cleaner import TextCleaner
from src.utils.visualizer import Visualizer

__all__ = ['TextCleaner', 'Visualizer']