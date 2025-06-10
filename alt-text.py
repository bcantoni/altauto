#!/usr/bin/env python3
"""
Create alt text for images using a language model

Specification for this script:

Create a function generate-alt-text()
- accepts a path to an image and an LLM prompt
- shells out to a local LLM utility as follows: `llm -a {image-file-path} "{prompt}"`
- save the output of the LLM utility and use that for the return value
- if the image file is not found at the path provided, return "ERROR file not found"

If someone runs this script by itself, include "main" functionality as follows:
- look for images in the ./images folder
- for each image and for each of the LLM prompts shown below, call generate-alt-text() to create alt text
- create a simple HTML output file alt-text.html which shows each image along with each of the 3 alt text snippets created

LLM prompts:
1. You are a helpful alt-text generator assisting visually impaired users. Generate a clear and concise caption (15-30 words) that highlights the most important subject and action. Focus only on essential details, avoiding unnecessary background elements. Use simple, everyday language and avoid overly descriptive or poetic words.
2. What's in this image? Be brief, it's for image alt description on a social network. Don't write in the first person.
3. You write alt text for any image pasted in by the user. Alt text is always presented on a single line so it can be used easily in Markdown images. All text on the image (for screenshots etc) must be exactly included. A short note describing the nature of the image itself should go first.

"""

import os
import subprocess
import glob
from pathlib import Path
from time import sleep


def generate_alt_text(image_path, prompt):
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
    
    try:
        cmd = ['llm', '-a', image_path, prompt]
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


def main():
    """Main functionality to process images and generate alt text"""
    prompts = [
        "You are a helpful alt-text generator assisting visually impaired users. Generate a clear and concise caption (15-30 words) that highlights the most important subject and action. Focus only on essential details, avoiding unnecessary background elements. Use simple, everyday language and avoid overly descriptive or poetic words.",
        "What's in this image? Be brief, it's for image alt description on a social network. Don't write in the first person.",
        "You write alt text for any image pasted in by the user. Alt text is always presented on a single line so it can be used easily in Markdown images. All text on the image (for screenshots etc) must be exactly included. A short note describing the nature of the image itself should go first."
    ]
    
    image_dir = "./images"
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(image_dir, ext)))
    
    if not image_files:
        print("No image files found in ./images directory")
        return
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Image Alt Text Generator Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .image-container { margin-bottom: 40px; border-bottom: 1px solid #ccc; padding-bottom: 20px; }
        .alt-text { margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-left: 4px solid #4CAF50; }
        img { max-width: 600px; max-height: 400px; }
        h3 { color: #333; }
    </style>
</head>
<body>
    <h1>Image Alt Text Generator Results</h1>
"""
    
    for image_file in image_files:
        img_path = os.path.abspath(image_file)
        img_name = Path(image_file).name
        
        html_content += f'<div class="image-container">\n'
        html_content += f'    <h2>Image: {img_name}</h2>\n'
        html_content += f'    <img src="{image_file}" alt="Original image">\n'
        
        for i, prompt in enumerate(prompts, 1):
            print(f"Generating alt text for {img_name} with prompt {i}...")
            alt_text = generate_alt_text(img_path, prompt)
            html_content += f'    <h3>Alt Text {i}:</h3>\n'
            html_content += f'    <div class="alt-text">{alt_text}</div>\n'
            sleep(3)
            
        html_content += '</div>\n'
    
    html_content += """</body>
</html>
"""
    
    with open('alt-text.html', 'w') as f:
        f.write(html_content)
    
    print(f"Generated alt text for {len(image_files)} images. Results saved to alt-text.html")


if __name__ == "__main__":
    main()
