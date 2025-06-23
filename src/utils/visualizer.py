"""
Terminal Visualization Utilities
Functions for displaying data in terminal using ASCII art
"""

from typing import Dict, List, Tuple
from collections import defaultdict

class TerminalVisualizer:
    """Utilities for terminal-based data visualization"""
    
    @staticmethod
    def plot_ngram_results(word: str, results: Dict[int, float], metadata: Dict[int, List[Tuple[str, int]]]):
        """
        Plot ngram results as ASCII bar chart
        
        Args:
            word: The searched word
            results: Dictionary mapping decades to frequencies
            metadata: Dictionary mapping decades to book metadata
        """
        if not results:
            print("No results to plot")
            return
        
        print(f"\nNgram results for '{word}':")
        print("=" * 60)
        
        decades = sorted(results.keys())
        frequencies = [results[d] for d in decades]
        
        if max(frequencies) == 0:
            print("No occurrences found")
            return
        
        # Normalize for ASCII plot
        max_freq = max(frequencies)
        max_width = 40
        
        for decade, freq in zip(decades, frequencies):
            bar_width = int((freq / max_freq) * max_width) if max_freq > 0 else 0
            bar = "█" * bar_width
            
            # Format frequency display
            if freq >= 1000:
                freq_str = f"{freq:.0f}"
            elif freq >= 10:
                freq_str = f"{freq:.1f}"
            else:
                freq_str = f"{freq:.2f}"
            
            print(f"{decade}s: {bar:<40} {freq_str}")
        
        print(f"\nFrequency = occurrences per million words")
        
        # Show metadata for context
        TerminalVisualizer.show_decade_summary(metadata)
    
    @staticmethod
    def show_decade_summary(metadata: Dict[int, List[Tuple[str, int]]]):
        """
        Show summary of books by decade
        
        Args:
            metadata: Dictionary mapping decades to book metadata
        """
        print(f"\nBooks analyzed:")
        print("-" * 40)
        
        total_books = 0
        for decade in sorted(metadata.keys()):
            books = metadata[decade]
            count = len(books)
            total_books += count
            print(f"{decade}s: {count} books")
        
        print(f"\nTotal: {total_books} books")
    
    @staticmethod
    def show_search_progress(current: int, total: int, word: str):
        """
        Show search progress bar
        
        Args:
            current: Current progress
            total: Total items
            word: Word being searched
        """
        if total == 0:
            return
        
        progress = current / total
        bar_length = 30
        filled_length = int(bar_length * progress)
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percentage = progress * 100
        
        print(f"\rSearching '{word}': [{bar}] {percentage:.1f}% ({current}/{total})", end='', flush=True)
        
        if current == total:
            print()  # New line when complete
    
    @staticmethod
    def show_welcome_banner():
        """Show welcome banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    Simple Ngram Viewer                      ║
║                                                              ║
║           Inspired by Google Ngram Viewer                   ║
║     Using KMP and Boyer-Moore pattern matching algorithms   ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    @staticmethod
    def show_algorithm_comparison(kmp_time: float, bm_time: float, pattern_length: int):
        """
        Show algorithm performance comparison
        
        Args:
            kmp_time: KMP algorithm execution time
            bm_time: Boyer-Moore algorithm execution time
            pattern_length: Length of search pattern
        """
        print(f"\nAlgorithm Performance Comparison:")
        print("-" * 40)
        print(f"Pattern length: {pattern_length} characters")
        print(f"KMP time:       {kmp_time:.4f} seconds")
        print(f"Boyer-Moore:    {bm_time:.4f} seconds")
        
        if kmp_time > 0 and bm_time > 0:
            if kmp_time < bm_time:
                speedup = bm_time / kmp_time
                print(f"KMP is {speedup:.2f}x faster")
            else:
                speedup = kmp_time / bm_time
                print(f"Boyer-Moore is {speedup:.2f}x faster")
    
    @staticmethod
    def show_menu():
        """Show main menu options"""
        menu = """
Options:
  1. Search for a word
  2. Compare algorithms
  3. Show database info
  4. Clear cache
  5. Exit

Enter your choice (1-5): """
        return input(menu).strip()
    
    @staticmethod
    def format_book_info(title: str, year: int, max_width: int = 50) -> str:
        """
        Format book information for display
        
        Args:
            title: Book title
            year: Publication year
            max_width: Maximum width for title
            
        Returns:
            Formatted string
        """
        if len(title) > max_width:
            title = title[:max_width-3] + "..."
        
        return f"{title:<{max_width}} ({year})"