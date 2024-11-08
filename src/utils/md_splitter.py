from langchain_text_splitters import MarkdownHeaderTextSplitter
from typing import List, Dict
import os
import json

def split_markdown_file(file_path: str) -> List[Dict[str, str]]:
    """Split a markdown file into chunks based on headers.
    
    Args:
        file_path: Path to the markdown file to split
        
    Returns:
        List of dictionaries containing the chunks with their metadata
    """
    # Read the markdown file
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    
    # Configure the header types to split on
    headers_to_split_on = [
        ("#", "header_1"),
        ("##", "header_2"),
        ("###", "header_3"),
    ]
    
    # Initialize the markdown splitter
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False # Keep headers in content for context
    )
    
    # Process chunks to ensure URL is preserved and handle non-header content
    processed_chunks = []
    page_url = None
    
    # First check if the text starts with PAGE URL
    lines = markdown_text.split('\n')
    content_lines = []
    
    for line in lines:
        if line.startswith("PAGE URL:"):
            page_url = line.split("PAGE URL:")[1].strip()
            continue
        content_lines.append(line)
    
    # Rejoin the content without the URL line
    content = '\n'.join(content_lines).strip()
    
    # Try to split by headers
    chunks = markdown_splitter.split_text(content)
    
    # If no chunks were created (no headers found) but we have content,
    # create a single chunk with the entire content
    if not chunks and content:
        processed_chunks.append({
            "content": content,
            "metadata": {"page_url": page_url} if page_url else {}
        })
    else:
        # Process chunks with headers normally
        for chunk in chunks:
            metadata = chunk.metadata
            if page_url:
                metadata["page_url"] = page_url
                
            processed_chunks.append({
                "content": chunk.page_content.strip(),
                "metadata": metadata
            })
    
    return processed_chunks

def process_markdown_directory(directory_path: str) -> Dict[str, List[Dict[str, str]]]:
    """Process all markdown files in a directory and return a dictionary of file-wise chunks."""
    all_chunks = {}
    
    # Process each markdown file in directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.md'):
            file_path = os.path.join(directory_path, filename)
            chunks = split_markdown_file(file_path)
            all_chunks[filename] = chunks
    
    return all_chunks

def save_chunks_per_file(chunks_dict: Dict[str, List[Dict[str, str]]], output_dir: str) -> None:
    """Save each file's chunks into separate JSONL files."""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename, chunks in chunks_dict.items():
        base_name = os.path.splitext(filename)[0]
        chunk_file = os.path.join(output_dir, f"{base_name}.jsonl")
        
        with open(chunk_file, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                json.dump(chunk, f)
                f.write('\n')
        
        print(f"Chunks saved to: {chunk_file}")
