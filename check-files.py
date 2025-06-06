#!/usr/bin/env python3
"""
Script to find markdown files and report on image references within them.

This script walks through a directory structure starting from the specified path,
finds all markdown (.md) files, and reports any image references found.
It also reports image references that are missing alt text.
"""

import os
import re
import argparse
import sys
from pathlib import Path


def find_markdown_files(start_path):
    """
    Find all markdown files in the directory tree starting at start_path.

    Args:
        start_path (str): The starting directory path

    Returns:
        list: A list of paths to markdown files
    """
    if not os.path.exists(start_path):
        print(f"Error: Path '{start_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    md_files = []

    for root, _, files in os.walk(start_path):
        for file in files:
            if file.lower().endswith('.md'):
                md_files.append(os.path.join(root, file))

    return md_files


def check_image_references(file_path):
    """
    Check for image references in a markdown file and report missing alt text.

    Args:
        file_path (str): Path to the markdown file

    Returns:
        None: Prints results to stdout
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()

        found_images = False

        # Regular expression for markdown image syntax: ![alt text](image_url)
        # Captures alt text and image URL as groups
        img_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

        for i, line in enumerate(content):
            # Skip HTML image tags (not capturing these as per requirements)
            if '<img' in line and '>' in line:
                continue

            matches = img_pattern.findall(line)
            if matches:
                found_images = True
                line_num = i + 1

                for alt_text, img_url in matches:
                    if not alt_text.strip():
                        print(f"\nFile: {file_path}")
                        print(f"Missing alt text line {line_num}: {line.strip()}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)


def main():
    """Main function to parse arguments and execute the script."""
    parser = argparse.ArgumentParser(
        description="Find markdown files and report on image references."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to the directory to search for markdown files"
    )

    args = parser.parse_args()
    start_path = os.path.abspath(args.path)

    print(f"Searching for markdown files in: {start_path}")
    md_files = find_markdown_files(start_path)

    if not md_files:
        print("No markdown files found.")
        return

    print(f"Found {len(md_files)} markdown file(s).")

    for file_path in md_files:
        check_image_references(file_path)


if __name__ == "__main__":
    main()
