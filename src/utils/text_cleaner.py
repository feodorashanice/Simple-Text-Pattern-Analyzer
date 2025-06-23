"""
Text cleaning utilities for processing Project Gutenberg texts.
Removes headers, footers, and normalizes text.
"""


class TextCleaner:
    """Utilities for cleaning and preprocessing text"""
    
    @staticmethod
    def clean_gutenberg_text(text: str) -> str:
        """
        Remove Project Gutenberg headers and footers.
        
        Args:
            text: Raw text from Project Gutenberg
            
        Returns:
            Cleaned text with headers/footers removed
        """
        # Find start of actual content
        start_markers = [
            "*** START OF THE PROJECT GUTENBERG EBOOK",
            "*** START OF THIS PROJECT GUTENBERG EBOOK",
        ]
        
        start_pos = 0
        for marker in start_markers:
            pos = text.find(marker)
            if pos != -1:
                start_pos = text.find('\n', pos) + 1
                break
        
        # Find end of actual content
        end_markers = [
            "*** END OF THE PROJECT GUTENBERG EBOOK",
            "*** END OF THIS PROJECT GUTENBERG EBOOK",
        ]
        
        end_pos = len(text)
        for marker in end_markers:
            pos = text.find(marker)
            if pos != -1:
                end_pos = pos
                break
        
        return text[start_pos:end_pos]
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text for analysis.
        
        Args:
            text: Raw text to normalize
            
        Returns:
            Normalized text (lowercase, cleaned)
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text