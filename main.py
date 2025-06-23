#!/usr/bin/env python3
"""
Simple Ngram Viewer - Main Entry Point
Terminal-based ngram viewer inspired by Google Ngram Viewer
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analysis.ngram_analyzer import NgramAnalyzer

def main():
    """Main entry point"""
    print("Simple Ngram Viewer")
    print("==================")
    print("Inspired by Google Ngram Viewer")
    print("Using KMP and Boyer-Moore algorithms for pattern matching")
    print()
    
    try:
        analyzer = NgramAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())