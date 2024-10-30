import argparse
from bs4 import BeautifulSoup
import scraper.html_fetcher as html_fetcher
import parsing.js_detection as js_detection
import parsing.html_parser as html_parser
import llm.pretty_printer as pretty_print
from models.website_content import WebsiteContent
import os
from dotenv import load_dotenv

load_dotenv()
DEFAULT_FILE_PATH = os.getenv('DEFAULT_FILE_PATH')
DEFAULT_LANGUAGE = os.getenv('LANGUAGE', 'english')

def run(url=DEFAULT_FILE_PATH, language=DEFAULT_LANGUAGE):
    soup = fetch_html_content(url)
    website_content_dict = parse_website_content(soup, url)
    # pretty = pretty_print.gpt(website_content_dict, language)
    # print(pretty)
    
# Fetches HTML content and handles JavaScript-dependent pages
def fetch_html_content(url):
    html_content = html_fetcher.request(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    if js_detection.check_javascript_needed(soup.body):
        html_content = html_fetcher.request(url)
        soup = BeautifulSoup(html_content, 'html.parser')
    return soup

# Parses content from HTML and initializes WebsiteContent
def parse_website_content(soup, url):
    website_content = WebsiteContent(
        url=url,
        language=html_parser.language(soup),
        title=html_parser.title(soup),
        headings=html_parser.headings(soup),
        spans=html_parser.span_texts(soup),
        texts=html_parser.texts(soup),
        images=html_parser.images(soup),
        links=html_parser.links(soup),
    )
    return website_content.to_dict()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Summarize website content.')
    parser.add_argument('url', nargs='?', default=DEFAULT_FILE_PATH, help='URL or file path of the website to summarize')
    parser.add_argument('--language', '-l', default=DEFAULT_LANGUAGE, help='Language of the summary (default: english)')
    args = parser.parse_args()
    run(args.url, args.language)