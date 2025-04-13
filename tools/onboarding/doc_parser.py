"""
Document parsing utilities for ThinkAlike project.
"""

def create_doc_list(directory_path, file_extension='.md'):
    """
    Create a list of documentation files from a directory.
    
    Args:
        directory_path: Path to directory containing documentation files
        file_extension: File extension to filter (default: '.md')
        
    Returns:
        list: List of file paths
    """
    import os
    doc_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(file_extension):
                doc_files.append(os.path.join(root, file))
    return doc_files

def extract_code_comments(file_path):
    """
    Extract code comments from a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        list: List of comments
    """
    import re
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract comments (simplistic implementation)
    # For Python files
    python_comments = re.findall(r'#\s*(.*?)$', content, re.MULTILINE)
    # For JS/TS files
    js_comments = re.findall(r'\/\/\s*(.*?)$', content, re.MULTILINE)
    # For multi-line comments
    multi_comments = re.findall(r'\/\*\*(.*?)\*\/', content, re.DOTALL)
    
    return python_comments + js_comments + multi_comments

def transform_markdown(content):
    """
    Transform markdown content according to project standards.
    
    Args:
        content: Markdown content to transform
        
    Returns:
        str: Transformed markdown content
    """
    # Add blank lines around lists for proper rendering
    import re
    content = re.sub(r'([^\n])\n([\*\-\+])', r'\1\n\n\2', content)
    content = re.sub(r'([\*\-\+].*)\n([^\s\*\-\+\n])', r'\1\n\n\2', content)
    
    # Ensure headers have proper spacing
    content = re.sub(r'(#+)([^#\s])', r'\1 \2', content)
    
    # Ensure code blocks are properly spaced
    content = re.sub(r'([^\n])\n```', r'\1\n\n```', content)
    content = re.sub(r'```\n([^\n])', r'```\n\n\1', content)
    
    return content
