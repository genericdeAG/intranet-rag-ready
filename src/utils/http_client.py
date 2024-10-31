from typing import Optional
import requests
import scraper.html_fetcher as html_fetcher
import parsing.js_detection as js_detection
from bs4 import BeautifulSoup

# Performs an HTTP GET request to the passed URL and returns the content as bytes if the status code is successful, or None in case of errors.
def fetch_web_content(url: str) -> Optional[bytes]:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
            return None
    except Exception as e:
        print(f'Failed to fetch web content: {e}')
        return None
    
# Fetches HTML content and handles JavaScript-dependent pages
def fetch_html_content(url):
    html_content = html_fetcher.request(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    if js_detection.check_javascript_needed(soup.body):
        html_content = html_fetcher.request(url)
        soup = BeautifulSoup(html_content, 'html.parser')
    return soup