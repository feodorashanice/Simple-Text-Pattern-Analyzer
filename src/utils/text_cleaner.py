"""
Text Cleaning Utilities
Functions for cleaning and preprocessing text data
"""

import re
from typing import List

class TextCleaner:
    """Utilities for cleaning and preprocessing text"""
    
    @staticmethod
    def clean_gutenberg_text(text: str) -> str:
        """
        Remove Project Gutenberg headers and footers
        
        Args:
            text: Raw text from Project Gutenberg
            
        Returns:
            Cleaned text content
        """
        # Find start of actual content
        start_markers = [
            "*** START OF THE PROJECT GUTENBERG EBOOK",
            "*** START OF THIS PROJECT GUTENBERG EBOOK",
            "***START OF THE PROJECT GUTENBERG EBOOK",
        ]
        
        start_pos = 0
        for marker in start_markers:
            pos = text.find(marker)
            if pos != -1:
                # Find end of the header line
                start_pos = text.find('\n', pos) + 1
                break
        
        # Find end of actual content
        end_markers = [
            "*** END OF THE PROJECT GUTENBERG EBOOK",
            "*** END OF THIS PROJECT GUTENBERG EBOOK", 
            "***END OF THE PROJECT GUTENBERG EBOOK",
            "End of the Project Gutenberg EBook",
            "End of Project Gutenberg's",
        ]
        
        end_pos = len(text)
        for marker in end_markers:
            pos = text.find(marker)
            if pos != -1:
                end_pos = pos
                break
        
        return text[start_pos:end_pos].strip()
    
    @staticmethod
    def extract_words(text: str) -> List[str]:
        """
        Extract words from text using regex
        
        Args:
            text: Input text
            
        Returns:
            List of words (lowercase, alphanumeric only)
        """
        # Extract words (alphanumeric characters only)
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return words
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text for consistent processing
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def remove_common_artifacts(text: str) -> str:
        """
        Remove common Project Gutenberg text artifacts
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Remove chapter markers
        text = re.sub(r'CHAPTER [IVXLC]+\.?\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Chapter \d+\.?\s*', '', text, flags=re.IGNORECASE)
        
        # Remove page markers
        text = re.sub(r'\[Pg \d+\]', '', text)
        text = re.sub(r'Page \d+', '', text)
        
        # Remove illustration markers
        text = re.sub(r'\[Illustration[^\]]*\]', '', text)
        
        # Remove footnote markers
        text = re.sub(r'\[\d+\]', '', text)
        
        return text
    
    @classmethod
    def full_clean(cls, text: str) -> str:
        """
        Apply all cleaning steps
        
        Args:
            text: Raw text from Project Gutenberg
            
        Returns:
            Fully cleaned and normalized text
        """
        # Remove Gutenberg headers/footers
        text = cls.clean_gutenberg_text(text)
        
        # Remove common artifacts
        text = cls.remove_common_artifacts(text)
        
        # Normalize
        text = cls.normalize_text(text)
        
        return text