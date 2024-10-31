import argparse
import parsing.content_parser as content_parser
import utils.http_client as http_client
import os
from dotenv import load_dotenv
import utils.md_converter as md_converter
import llm.pretty_printer as pretty_print

load_dotenv()
DEFAULT_FILE_PATH = os.getenv('DEFAULT_FILE_PATH')
DEFAULT_LANGUAGE = os.getenv('LANGUAGE', 'english')

def run(url=DEFAULT_FILE_PATH, language=DEFAULT_LANGUAGE):
    soup = http_client.fetch_html_content(url)
    website_content_dict = content_parser.parse_website_content(soup, url)
    # Convert dict to markdown
    markdown_output = md_converter.convert_to_md(website_content_dict)
    # Generate filename from title or URL
    filename = website_content_dict.get('title', 'extract').replace(' ', '_')
    # Save to file and get the file path
    saved_path = md_converter.save_md_to_file(filename, markdown_output)
    
    pretty = pretty_print.gpt(saved_path)
    # Save the pretty printed markdown to a file
    md_converter.save_md_to_file(f"{filename}_pretty", pretty)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Summarize website content.')
    parser.add_argument('url', nargs='?', default=DEFAULT_FILE_PATH, help='URL or file path of the website to summarize')
    parser.add_argument('--language', '-l', default=DEFAULT_LANGUAGE, help='Language of the summary (default: english)')
    args = parser.parse_args()
    run(args.url, args.language)