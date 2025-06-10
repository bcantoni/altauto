# Copilot Instructions for AltAuto Project

## Project Overview
AltAuto is a tool designed to automatically create and suggest alternative text for images referenced in Markdown files. The project aims to improve accessibility by ensuring all images in Markdown documents have proper alt text.

## Code Structure
- `check-files.py`: Main Python script that walks through directories to find Markdown files and report on image references missing alt text
- Future components to include:
  - Script/library using AI to analyze images and suggest alt text
  - GitHub action to automate the process

## Coding Guidelines

### General Guidelines
- Use Python PEP 8 standards as implemented by `black` to enforce a consistent style for all .py files
- Use descriptive variable and function names
- Include docstrings for all functions and modules
- Add appropriate type hints when possible
- Don't add comments except for these cases:
  - Any unusual logic (e.g. why a loop may be skipped)
  - Explaining the purpose of regular expressions

### Python-Specific Rules
- Target Python 3.6+ compatibility
- Use f-strings for string formatting
- Use pathlib for file path operations when appropriate
- Handle file operations with proper error handling and encoding (utf-8)

### Testing & PR Guidelines
- Ensure any modifications pass existing tests
- For new features, include appropriate tests
- Consider caching mechanisms for LLM results to avoid repeated requests
- When generating alt text, avoid recreating text for images in existing PRs

## License
This project is under the MIT License. All contributions should be compatible with this license.

## Feature Development Priorities
1. Enhance image detection in Markdown files
2. Develop AI integration for generating alt text suggestions
3. Create GitHub action for automation
4. Implement caching for LLM results
5. Support for multiple image formats and sources
