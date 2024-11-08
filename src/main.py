import argparse
import os
from dotenv import load_dotenv
import utils.md_converter as md_converter
import utils.md_splitter as md_splitter
import llm.pretty_printer as pretty_print
import asyncio
from factories.msgraph_client_factory import MSGraphClientFactory

load_dotenv()
DEFAULT_FILE_PATH = os.getenv('DEFAULT_FILE_PATH')

async def process_sharepoint_site(site_id: str, use_mock: bool) -> None:
    """Process all pages and webparts for a SharePoint site
    
    Args:
        site_id: The ID of the SharePoint site
        use_mock: Whether to use mock client instead of real one
    """
    # Get appropriate client instance
    graph_client = MSGraphClientFactory.get_client(use_mock=use_mock)
    
    # Get all pages for the site
    pages = await graph_client.get_sharepoint_site_pages(site_id)
    
    if pages and "value" in pages:
        for page in pages["value"]:
            page_id = page["id"]
            page_url = page["webUrl"]
            # get the site name from the page url. It is after the "sites/" and before the next "/"
            site_name = page_url.split("/sites/")[1].split("/")[0]
            page_name = page["name"]
            print(f"Processing page: {page_url}")
            # Get webparts for each page
            webparts = await graph_client.get_sharepoint_site_page_webparts(site_id, page_id)
            if webparts:
                # Process webparts through GPT
                pretty = pretty_print.gpt(webparts)
                # add page url at the beginning of the markdown with two newlines afterwards
                pretty = f"PAGE URL: {page_url}\n\n{pretty}"
                # Save the processed markdown
                md_converter.save_md_to_file(f"{site_name}_{page_name}", pretty)

def chunk_markdown_files(input_dir: str = None) -> None:
    """Process existing markdown files and split them into chunks.
    
    Args:
        input_dir: Directory containing markdown files to process. 
                  Defaults to data/extracts if not specified.
    """
    # Use default directory if none specified
    if not input_dir:
        input_dir = os.path.join('data', 'extracts')
    
    # Ensure directory exists
    if not os.path.exists(input_dir):
        raise ValueError(f"Directory not found: {input_dir}")
        
    chunks_dict = md_splitter.process_markdown_directory(input_dir)
    
    chunks_dir = os.path.join('data', 'chunks')
    md_splitter.save_chunks_per_file(chunks_dict, chunks_dir)
    
    total_chunks = sum(len(chunks) for chunks in chunks_dict.values())
    print(f"Processed {total_chunks} chunks from markdown files")

def run(site_id: str = os.getenv("SITE_ID_1"), use_mock: bool = False) -> None:
    """Main run function for processing SharePoint content
    
    Args:
        use_mock: Whether to use mock client
    """
    # Process content based on site IDs
    asyncio.run(process_sharepoint_site(site_id, use_mock))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process SharePoint pages and chunk markdown files.')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Parser for the sharepoint command
    sp_parser = subparsers.add_parser('sharepoint', help='Process SharePoint sites')
    sp_parser.add_argument('--site-id', help='SharePoint site ID or site number (1, 2, etc.) to draw from env')
    sp_parser.add_argument('--mock', action='store_true', help='Use mock client instead of real one')
    
    # Parser for the chunk command
    chunk_parser = subparsers.add_parser('chunk', help='Chunk existing markdown files')
    chunk_parser.add_argument('--input-dir', help='Directory containing markdown files to process')
    
    args = parser.parse_args()
    
    if args.command == 'sharepoint':
        if args.site_id:
            # Check if the input is a number
            if args.site_id.isdigit():
                # Get the site ID from environment variable (e.g., SITE_ID_1, SITE_ID_2)
                env_site_id = os.getenv(f"SITE_ID_{args.site_id}")
                if not env_site_id:
                    raise ValueError(f"No site ID found in environment for number {args.site_id}")
                site_id = env_site_id
            else:
                site_id = args.site_id
                
            asyncio.run(process_sharepoint_site(site_id, args.mock))
        else:
            run(use_mock=args.mock)
            
    elif args.command == 'chunk':
        chunk_markdown_files(args.input_dir)
    else:
        # Default to original behavior if no command specified
        run(use_mock=False)