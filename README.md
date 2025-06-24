# Simple-Text-Pattern-Analyzer
Simple Text Pattern Analyzer with KMP and Boyer-Moore Algorithms

## Overview
This tool allows users to input a specific word or phrase (the "pattern") and choose between the KMP or Boyer–Moore string matching algorithms to analyze its occurrence over time, based on a dataset of digitized literary works in JSON format. Each book entry contains metadata such as title, author, publication year, and content. The program then reports the frequency of the pattern across different years, emulating the core functionality of Google Ngram Viewer.

## Author

| NIM       | Name                     |
|-----------|--------------------------|
| 13523097  | Shanice Feodora Tjahjono |

## Features

- Reads a JSON dataset containing metadata and text of books
- Pattern search using KMP or Boyer–Moore algorithms
- Displays frequency of pattern by publication year

## How to Run

```bash
python main.py
```

### Interactive Process
You will be prompted to:
1. Enter the pattern to search - Input any word or phrase you want to analyze
2. Choose the algorithm - Select either KMP or Boyer-Moore for pattern matching

### Results
The program displays the trend of the word or phrase per decade and visualizes it in a bar chart format in the console.

### Additional Note
The input file (books_database.json) can be freely customized by the user, as long as it follows the expected structure with fields like title, author, year, and id.