"""
Main ngram analysis engine.
Coordinates data loading, text processing, and pattern matching.
"""

import os
import re
import time
from collections import defaultdict
from typing import Dict, List

from ..algorithms.pattern_matching import PatternMatcher
from ..data.downloader import DataDownloader
from ..utils.text_cleaner import TextCleaner
from ..utils.visualizer import Visualizer


class NgramAnalyzer:
    """Main class for ngram analysis"""
    
    def __init__(self):
        self.downloader = DataDownloader()
        self.matcher = PatternMatcher()
        self.cleaner = TextCleaner()
        self.visualizer = Visualizer()
        self.corpus = defaultdict(list)  # decade -> list of texts
        self.metadata = {}  # decade -> list of (title, year) tuples
    
    def setup_data(self):
        """Download and organize data by decades"""
        print("Setting up data...")
        books = self.downloader.load_books_from_json()
        
        print(f"Found {len(books)} books in database")
        
        for book_id, (title, year) in books.items():
            decade = (year // 10) * 10
            book_path = self.downloader.download_book(book_id)
            
            if book_path and os.path.exists(book_path):
                try:
                    with open(book_path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    
                    # Clean and normalize text
                    text = self.cleaner.clean_gutenberg_text(text)
                    text = self.cleaner.normalize_text(text)
                    self.corpus[decade].append(text)
                    
                    if decade not in self.metadata:
                        self.metadata[decade] = []
                    self.metadata[decade].append((title, year))
                    
                    print(f"✓ Processed: {title} ({year})")
                    
                except Exception as e:
                    print(f"✗ Error processing {title}: {e}")
            else:
                print(f"✗ Failed to download: {title}")
        
        # Display summary
        corpus_info = {decade: len(texts) for decade, texts in self.corpus.items()}
        self.visualizer.display_summary(corpus_info)
    
    def search_word(self, word: str, algorithm: str = "kmp") -> Dict[int, float]:
        """
        Search for a word across all decades.
        
        Args:
            word: The word to search for
            algorithm: Algorithm to use ("kmp" or "boyer-moore")
            
        Returns:
            Dictionary mapping decade to frequency per million words
        """
        print(f"Searching for '{word}' using {algorithm.upper()} algorithm...")
        
        word = word.lower()
        results = {}
        
        for decade, texts in self.corpus.items():
            total_matches = 0
            total_words = 0
            
            for text in texts:
                # Use word boundaries to match whole words only
                words = re.findall(r'\b\w+\b', text)
                total_words += len(words)
                
                # Join words back for pattern matching
                text_joined = ' '.join(words)
                
                if algorithm.lower() == "kmp":
                    matches = self.matcher.kmp_search(text_joined, word)
                else:
                    matches = self.matcher.boyer_moore_search(text_joined, word)
                
                total_matches += len(matches)
            
            # Calculate frequency per million words
            if total_words > 0:
                frequency = (total_matches / total_words) * 1000000
                results[decade] = frequency
            else:
                results[decade] = 0.0
        
        return results
    
    def analyze_word(self, word: str, algorithm: str = "kmp"):
        """
        Complete analysis workflow for a word.
        
        Args:
            word: The word to analyze
            algorithm: Algorithm to use for pattern matching
        """
        start_time = time.time()
        results = self.search_word(word, algorithm)
        end_time = time.time()
        
        print(f"Search completed in {end_time - start_time:.3f} seconds")
        self.visualizer.plot_terminal_chart(word, results, self.metadata)
    
    def is_data_ready(self) -> bool:
        """Check if corpus data is available"""
        return len(self.corpus) > 0