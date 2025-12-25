#!/usr/bin/env python3
"""
Chemical Composition Extraction Pipeline

Usage:
    python run.py <pdf_path> [-o output.csv]
    
Example:
    python run.py data/input/matcert.pdf
    python run.py data/input/matcert.pdf -o results.csv
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import extract_chemical_composition
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Extract chemical composition from material certificates'
    )
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', help='Output CSV file path', default=None)
    parser.add_argument('--dpi', type=int, default=400, help='DPI for PDF conversion')
    
    args = parser.parse_args()
    
    if not Path(args.pdf_path).exists():
        print(f"Error: File not found: {args.pdf_path}")
        return 1
    
    from src.config import CONFIG
    CONFIG['dpi'] = args.dpi
    
    df = extract_chemical_composition(args.pdf_path, args.output)
    
    if df is not None and not df.empty:
        print("\nExtracted data preview:")
        print(df.head(20).to_string())
        return 0
    else:
        print("No data extracted")
        return 1


if __name__ == '__main__':
    exit(main())
