"""
Pattern matching algorithms for text search.
Implements KMP and Boyer-Moore algorithms.
"""

from typing import List


class PatternMatcher:
    """Implements KMP and Boyer-Moore algorithms for string matching"""
    
    @staticmethod
    def kmp_search(text: str, pattern: str) -> List[int]:
        """
        Knuth-Morris-Pratt algorithm for pattern matching.
        
        Args:
            text: The text to search in
            pattern: The pattern to search for
            
        Returns:
            List of starting positions where pattern is found
        """
        if not pattern:
            return []
        
        # Build failure function (partial match table)
        def build_failure_function(pattern):
            failure = [0] * len(pattern)
            j = 0
            for i in range(1, len(pattern)):
                while j > 0 and pattern[i] != pattern[j]:
                    j = failure[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                failure[i] = j
            return failure
        
        failure = build_failure_function(pattern)
        matches = []
        j = 0
        
        for i in range(len(text)):
            while j > 0 and text[i] != pattern[j]:
                j = failure[j - 1]
            if text[i] == pattern[j]:
                j += 1
            if j == len(pattern):
                matches.append(i - j + 1)
                j = failure[j - 1]
        
        return matches
    
    @staticmethod
    def boyer_moore_search(text: str, pattern: str) -> List[int]:
        """
        Boyer-Moore algorithm for pattern matching.
        
        Args:
            text: The text to search in
            pattern: The pattern to search for
            
        Returns:
            List of starting positions where pattern is found
        """
        if not pattern:
            return []
        
        # Build bad character table
        def build_bad_char_table(pattern):
            table = {}
            for i in range(len(pattern)):
                table[pattern[i]] = i
            return table
        
        bad_char = build_bad_char_table(pattern)
        matches = []
        shift = 0
        
        while shift <= len(text) - len(pattern):
            j = len(pattern) - 1
            
            while j >= 0 and pattern[j] == text[shift + j]:
                j -= 1
            
            if j < 0:
                matches.append(shift)
                shift += len(pattern) if shift + len(pattern) < len(text) else 1
            else:
                char = text[shift + j]
                shift += max(1, j - bad_char.get(char, -1))
        
        return matches