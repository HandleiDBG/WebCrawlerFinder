import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin, urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

visited_urls = set()

def crawl_site(url, search_string=None, extract_dirs=False):
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    try:
        response = requests.get(url, verify=False)
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    if search_string:
        if search_string in response.text:
            print(f"String found in: {url}")

    if extract_dirs:
        print(url)

    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc == urlparse(url).netloc:
            crawl_site(full_url, search_string, extract_dirs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="WebCrawler Finder")
    parser.add_argument('--url', required=True, help="URL of the website to be analyzed")
    parser.add_argument('--search', help="String to be searched for on the website")
    parser.add_argument('--extract-dirs', action='store_true', help="Extract all site directories")

    args = parser.parse_args()

    if args.search:
        crawl_site(args.url, search_string=args.search)
    elif args.extract_dirs:
        crawl_site(args.url, extract_dirs=True)