"""
Visualization utilities for displaying ngram analysis results.
Provides ASCII-based terminal visualization.
"""

from typing import Dict


class Visualizer:
    """Handles visualization of ngram analysis results"""
    
    @staticmethod
    def plot_terminal_chart(word: str, results: Dict[int, float], metadata: Dict[int, list] = None):
        """
        Plot results in terminal using ASCII art.
        
        Args:
            word: The word that was searched
            results: Dictionary mapping decade to frequency
            metadata: Optional metadata about books per decade
        """
        if not results:
            print("No results to plot")
            return
        
        print(f"\nNgram results for '{word}':")
        print("=" * 50)
        
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
            print(f"{decade}s: {bar} {freq:.2f}")
        
        print("\nFrequency = occurrences per million words")
        
        # Show metadata for context
        if metadata:
            print(f"\nBooks analyzed by decade:")
            for decade in decades:
                if decade in metadata:
                    books = metadata[decade]
                    print(f"{decade}s: {len(books)} books")
    
    @staticmethod
    def display_summary(corpus_info: Dict[int, int]):
        """
        Display summary of corpus information.
        
        Args:
            corpus_info: Dictionary mapping decade to number of books
        """
        print(f"\nData setup complete!")
        print(f"Total books loaded: {sum(corpus_info.values())}")
        print(f"Decades covered: {sorted(corpus_info.keys())}")
        
        # Show summary by decade
        print("\nBooks by decade:")
        for decade in sorted(corpus_info.keys()):
            count = corpus_info[decade]
            print(f"  {decade}s: {count} books")