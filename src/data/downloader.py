"""
Data downloader for Project Gutenberg books.
Handles downloading and managing book files.
"""

import os
import json
import requests
from typing import Dict, Tuple


class DataDownloader:
    """Downloads and manages Project Gutenberg data"""
    
    def __init__(self, data_dir="gutenberg_data"):
        self.data_dir = data_dir
        self.metadata_file = os.path.join(data_dir, "metadata.json")
        os.makedirs(data_dir, exist_ok=True)
    
    def download_catalog(self):
        """Download Project Gutenberg catalog"""
        catalog_url = "https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.zip"
        print("Downloading Project Gutenberg catalog...")
        
        try:
            response = requests.get(catalog_url, stream=True)
            catalog_path = os.path.join(self.data_dir, "catalog.zip")
            
            with open(catalog_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("Catalog downloaded successfully!")
            return catalog_path
        except Exception as e:
            print(f"Error downloading catalog: {e}")
            return None
    
    def load_books_from_json(self, json_file: str = None) -> Dict[str, Tuple[str, int]]:
        """
        Load books from JSON database.
        
        Args:
            json_file: Path to JSON file containing book metadata
            
        Returns:
            Dictionary mapping book ID to (title, year) tuple
        """
        # Try multiple possible file locations
        if json_file is None:
            possible_files = [
                "books_database.json",
                "data/books_database.json",
                os.path.join(self.data_dir, "books_database.json")
            ]
        else:
            possible_files = [json_file]
        
        books_dict = {}
        
        for file_path in possible_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    for book in data['books']:
                        book_id = str(book['id'])  # Ensure book_id is string
                        title = book['title']
                        year = book['year']
                        author = book.get('author', 'Unknown')
                        
                        # Skip very old books (before 1500) for better decade distribution
                        if year < 1500:
                            continue
                            
                        books_dict[book_id] = (f"{title} by {author}", year)
                    
                    print(f"Loaded {len(books_dict)} books from {file_path}")
                    return books_dict
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from {file_path}: {e}")
                continue
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
        
        print(f"Warning: Could not find or load books database. Using fallback sample.")
        return self.get_fallback_books()
    
    def get_fallback_books(self) -> Dict[str, Tuple[str, int]]:
        """
        Fallback books if JSON loading fails.
        
        Returns:
            Dictionary of sample books for testing
        """
        return {
            "1342": ("Pride and Prejudice by Jane Austen", 1813),
            "11": ("Alice's Adventures in Wonderland by Lewis Carroll", 1865),
            "74": ("The Adventures of Tom Sawyer by Mark Twain", 1876),
            "84": ("Frankenstein by Mary Shelley", 1818),
            "2701": ("Moby Dick by Herman Melville", 1851),
        }
    
    def download_book(self, book_id: str) -> str:
        """
        Download a single book from Project Gutenberg.
        
        Args:
            book_id: The Project Gutenberg book ID
            
        Returns:
            Path to downloaded book file, or None if failed
        """
        book_path = os.path.join(self.data_dir, f"{book_id}.txt")
        
        if os.path.exists(book_path):
            print(f"Book {book_id} already exists")
            return book_path
        
        url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        try:
            print(f"Downloading book {book_id}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(book_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(response.text)
            
            print(f"Book {book_id} downloaded successfully!")
            return book_path
        
        except Exception as e:
            print(f"Error downloading book {book_id}: {e}")
            # Try alternative URL format
            alt_url = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
            try:
                response = requests.get(alt_url, timeout=10)
                response.raise_for_status()
                
                with open(book_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(response.text)
                
                print(f"Book {book_id} downloaded successfully (alternative URL)!")
                return book_path
            except Exception as e2:
                print(f"Failed to download book {book_id} from alternative URL: {e2}")
                return None