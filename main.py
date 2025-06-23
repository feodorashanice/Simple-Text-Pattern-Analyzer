#!/usr/bin/env python3
"""
Simple Ngram Viewer - Terminal-based program inspired by Google Ngram Viewer
Uses KMP and Boyer-Moore algorithms for pattern matching
Data source: Project Gutenberg books
"""

from src.analysis.ngram_analyzer import NgramAnalyzer


def main():
    """Main program entry point"""
    print("Simple Ngram Viewer")
    print("==================")
    print("Inspired by Google Ngram Viewer")
    print("Using KMP and Boyer-Moore algorithms for pattern matching")
    print()
    
    analyzer = NgramAnalyzer()
    
    # Setup data
    analyzer.setup_data()
    
    if not analyzer.is_data_ready():
        print("No data available. Please check your internet connection.")
        return
    
    # Main program loop
    while True:
        print("\n" + "="*50)
        word = input("Enter a word to search (or 'quit' to exit): ").strip()
        
        if word.lower() == 'quit':
            break
        
        if not word:
            continue
        
        # Choose algorithm
        algorithm = input("Choose algorithm (kmp/boyer-moore) [default: kmp]: ").strip().lower()
        if algorithm not in ['kmp', 'boyer-moore']:
            algorithm = 'kmp'
        
        analyzer.analyze_word(word, algorithm)


if __name__ == "__main__":
    main()