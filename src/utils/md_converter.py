import os

# This function converts dicts to markdown strings
def convert_to_md(dict):
    md_output = ""
    
    for key, value in dict.items():
        # Add the main section header
        md_output += f"# {key}\n"
        
        # Handle different value types
        if isinstance(value, list):
            # For lists, create a subsection for each item
            for item in value:
                md_output += f"## {item}\n"
        else:
            # For single values, create one subsection
            md_output += f"## {value}\n"
        
        # Add a blank line between sections
        md_output += "\n"
    
    return md_output

# This function saves markdown strings to a file
def save_md_to_file(filename, md_content):
    # Create the extracts directory if it doesn't exist
    output_dir = os.path.join('data', 'extracts')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{filename}.md"
    
    # Create full file path
    file_path = os.path.join(output_dir, filename)
    
    # Write content to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return file_path
