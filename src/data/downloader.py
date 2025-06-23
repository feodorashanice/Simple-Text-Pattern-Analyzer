"""
Data Downloader
Downloads and manages Project Gutenberg books
"""

import os
import json
import requests
from typing import Dict, Tuple, Optional

class DataDownloader:
    """Downloads and manages Project Gutenberg data"""
    
    def __init__(self, data_dir: str = "gutenberg_data"):
        """
        Initialize downloader
        
        Args:
            data_dir: Directory to store downloaded books
        """
        self.data_dir = data_dir
        self.metadata_file = os.path.join(data_dir, "metadata.json")
        os.makedirs(data_dir, exist_ok=True)
    
    def load_books_from_json(self, json_file: str = "data/books_database.json") -> Dict[str, Tuple[str, int]]:
        """
        Load books from JSON database
        
        Args:
            json_file: Path to JSON database file
            
        Returns:
            Dictionary mapping book IDs to (title, year) tuples
        """
        books_dict = {}
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for book in data['books']:
                book_id = book['id']
                title = book['title']
                year = book['year']
                author = book.get('author', 'Unknown')
                
                # Skip very old books (before 1500) for better decade distribution
                if year < 1500:
                    continue
                    
                books_dict[book_id] = (f"{title} by {author}", year)
            
            print(f"Loaded {len(books_dict)} books from {json_file}")
            return books_dict
            
        except FileNotFoundError:
            print(f"Warning: {json_file} not found. Using fallback sample.")
            return self._get_fallback_books()
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}. Using fallback sample.")
            return self._get_fallback_books()
    
    def _get_fallback_books(self) -> Dict[str, Tuple[str, int]]:
        """
        Fallback books if JSON loading fails
        
        Returns:
            Dictionary of fallback books
        """
        return {
            "1342": ("Pride and Prejudice by Jane Austen", 1813),
            "11": ("Alice's Adventures in Wonderland by Lewis Carroll", 1865),
            "74": ("The Adventures of Tom Sawyer by Mark Twain", 1876),
            "84": ("Frankenstein by Mary Shelley", 1818),
            "2701": ("Moby Dick by Herman Melville", 1851),
        }
    
    def download_book(self, book_id: str) -> Optional[str]:
        """
        Download a single book from Project Gutenberg
        
        Args:
            book_id: Project Gutenberg book ID
            
        Returns:
            Path to downloaded file, or None if failed
        """
        book_path = os.path.join(self.data_dir, f"{book_id}.txt")
        
        if os.path.exists(book_path):
            return book_path
        
        # Try multiple URL formats
        urls = [
            f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
            f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
            f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
        ]
        
        for url in urls:
            try:
                print(f"Downloading book {book_id} from {url}...")
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                
                with open(book_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(response.text)
                
                print(f"✓ Book {book_id} downloaded successfully!")
                return book_path
                
            except requests.RequestException as e:
                print(f"  Failed: {e}")
                continue
        
        print(f"✗ Failed to download book {book_id} from all URLs")
        return None
    
    def get_book_path(self, book_id: str) -> Optional[str]:
        """
        Get path to book file (download if necessary)
        
        Args:
            book_id: Project Gutenberg book ID
            
        Returns:
            Path to book file, or None if not available
        """
        book_path = os.path.join(self.data_dir, f"{book_id}.txt")
        
        if os.path.exists(book_path):
            return book_path
        
        return self.download_book(book_id)
    
    def clear_cache(self):
        """Clear downloaded books cache"""
        import shutil
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
        print("Cache cleared successfully!")