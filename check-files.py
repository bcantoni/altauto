#!/usr/bin/env python3
"""
Find markdown files and report on image references within them.

This script walks through a directory structure starting from the specified path,
finds all markdown files, and reports any image references that are missing alt text.
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def generate_alt_text(image_path):
    """
    Generate alt text for an image using a language model.

    Args:
        image_path (str): Path to the image file
        prompt (str): Prompt for the language model

    Returns:
        str: Generated alt text or error message
    """
    if not os.path.isfile(image_path):
        return "ERROR file not found"

    prompt = "You are a helpful alt-text generator assisting visually impaired users. Generate a clear and concise caption (15-30 words) that highlights the most important subject and action. Focus only on essential details, avoiding unnecessary background elements. Use simple, everyday language and avoid overly descriptive or poetic words."
    model = "4o-mini"

    try:
        print(f"Generating alt text for image: {image_path}, model: {model}")
        cmd = ["llm", "-a", image_path, "-m", model, prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.returncode != 0:
            return f"ERROR1 running LLM: {result.stderr.strip()}"
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # This exception has stdout and stderr attributes
        return f"ERROR2 running LLM: {str(e)}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
    except subprocess.SubprocessError as e:
        # Other subprocess exceptions may not have stdout/stderr attributes
        return f"ERROR3 running LLM: {str(e)}"


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
            if file.lower().endswith(".md"):
                md_files.append(os.path.join(root, file))

    return md_files


def check_image_references(file_path, base_path):
    """
    Check for image references in a markdown file and report missing alt text.

    Args:
        file_path (str): Path to the markdown file

    Returns:
        None: Prints results to stdout
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()

        # Regular expression for markdown image syntax: ![alt text](image_url)
        # Captures alt text and image URL as groups
        img_pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")

        for i, line in enumerate(content):
            # Skip HTML image tags (only focused on markdown syntax)
            if "<img" in line and ">" in line:
                continue

            matches = img_pattern.findall(line)
            if matches:
                line_num = i + 1

                for alt_text, img_url in matches:
                    if not img_url.startswith("http") and not alt_text.strip():
                        print(f"\nFile: {file_path}")
                        print(f"Missing alt text line {line_num}: {line.strip()}")
                        print(generate_alt_text(f"{base_path}{img_url}"))

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Find markdown files and report on image references."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to the directory to search for markdown files",
    )
    parser.add_argument(
        "--base",
        required=True,
        help="Path to the base directory for image files",
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
        check_image_references(file_path, args.base)


if __name__ == "__main__":
    main()
