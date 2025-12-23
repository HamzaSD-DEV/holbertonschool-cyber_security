#!/usr/bin/env python3
"""
Web Crawler Script
Recursively crawls a website with depth limiting.
Finds all links, visits each link, and repeats the process up to a specified depth.
Tracks visited URLs to avoid infinite loops and only crawls same domain.
"""

import sys
from urllib.parse import urljoin, urlparse
import time

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error: Required library not found: {e}")
    print("Install required libraries with:")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)


class WebCrawler:
    """
    Web crawler class that implements recursive crawling with depth limiting.
    """
    
    def __init__(self, start_url, max_depth=2, delay=1):
        """
        Initialize the web crawler.
        
        Args:
            start_url (str): The starting URL to crawl
            max_depth (int): Maximum depth to crawl
            delay (float): Delay between requests in seconds
        """
        self.start_url = start_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.crawled_urls = []
        
        # Parse the starting URL to get the base domain
        parsed_url = urlparse(start_url)
        self.base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.domain = parsed_url.netloc
        
        # Set up session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebCrawler/1.0)'
        })
    
    def is_valid_url(self, url):
        """
        Check if URL is valid for crawling.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL is valid for crawling
        """
        try:
            parsed_url = urlparse(url)
            
            # Must be HTTP or HTTPS
            if parsed_url.scheme not in ['http', 'https']:
                return False
            
            # Must be on the same domain
            if parsed_url.netloc != self.domain:
                return False
            
            # Skip certain file extensions
            skip_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.exe']
            if any(url.lower().endswith(ext) for ext in skip_extensions):
                return False
            
            return True
            
        except Exception:
            return False
    
    def extract_links(self, html_content, current_url):
        """
        Extract all links from HTML content.
        
        Args:
            html_content (str): HTML content to parse
            current_url (str): Current URL for resolving relative links
            
        Returns:
            list: List of absolute URLs found on the page
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            links = []
            
            # Find all anchor tags with href attributes
            for link in soup.find_all('a', href=True):
                href = link['href'].strip()
                
                # Skip empty hrefs and javascript/mailto links
                if not href or href.startswith(('#', 'javascript:', 'mailto:')):
                    continue
                
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(current_url, href)
                
                # Remove URL fragments
                absolute_url = absolute_url.split('#')[0]
                
                # Validate and add unique URLs
                if self.is_valid_url(absolute_url) and absolute_url not in links:
                    links.append(absolute_url)
            
            return links
            
        except Exception as e:
            print(f"Error extracting links: {e}")
            return []
    
    def crawl_page(self, url):
        """
        Crawl a single page and return its links.
        
        Args:
            url (str): URL to crawl
            
        Returns:
            list: List of links found on the page
        """
        try:
            print(f"Crawling: {url}")
            
            # Make HTTP request with timeout
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            # Check if request was successful
            if response.status_code != 200:
                print(f"  Warning: HTTP {response.status_code} for {url}")
                return []
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                print(f"  Skipping non-HTML content: {content_type}")
                return []
            
            # Extract links from the page
            links = self.extract_links(response.text, url)
            
            # Add current URL to crawled list
            self.crawled_urls.append(url)
            
            return links
            
        except requests.exceptions.Timeout:
            print(f"  Timeout: {url}")
            return []
        except requests.exceptions.ConnectionError:
            print(f"  Connection error: {url}")
            return []
        except Exception as e:
            print(f"  Error crawling {url}: {e}")
            return []
    
    def crawl_recursive(self, url, current_depth=0):
        """
        Recursively crawl website starting from given URL.
        
        Args:
            url (str): URL to start crawling from
            current_depth (int): Current crawling depth
        """
        # Check if we've reached maximum depth
        if current_depth > self.max_depth:
            return
        
        # Check if URL has already been visited
        if url in self.visited:
            return
        
        # Mark URL as visited
        self.visited.add(url)
        
        # Crawl the current page
        links = self.crawl_page(url)
        
        # Add delay between requests to be respectful
        if self.delay > 0:
            time.sleep(self.delay)
        
        # Recursively crawl found links if not at maximum depth
        if current_depth < self.max_depth:
            for link in links:
                if link not in self.visited:
                    self.crawl_recursive(link, current_depth + 1)
    
    def start_crawl(self):
        """
        Start the crawling process.
        
        Returns:
            list: List of all crawled URLs
        """
        print("=" * 50)
        print(f"Starting crawl of {self.start_url} (max depth: {self.max_depth})")
        
        try:
            self.crawl_recursive(self.start_url)
            
            print("=" * 50)
            print(f"Crawl completed. Found {len(self.crawled_urls)} pages:")
            for i, url in enumerate(self.crawled_urls, 1):
                print(f"  {i}. {url}")
            
            return self.crawled_urls
            
        except KeyboardInterrupt:
            print("\nCrawl interrupted by user")
            return self.crawled_urls
        except Exception as e:
            print(f"Error during crawling: {e}")
            return self.crawled_urls


def main():
    """
    Main function to handle user input and coordinate web crawling.
    """
    try:
        # Get URL from user input
        url = input("Enter URL to crawl: ").strip()
        
        if not url:
            print("Error: URL cannot be empty")
            sys.exit(1)
        
        # Add protocol if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Get max depth from user input
        depth_input = input("Enter max depth (default 2): ").strip()
        try:
            max_depth = int(depth_input) if depth_input else 2
            if max_depth < 0:
                print("Error: Depth must be non-negative")
                sys.exit(1)
        except ValueError:
            print("Error: Depth must be a valid number")
            sys.exit(1)
        
        # Create and start crawler
        crawler = WebCrawler(url, max_depth)
        crawled_urls = crawler.start_crawl()
        
        print("\nRemember: Always get permission before crawling websites!")
        print("Use only on authorized targets.")
        
    except KeyboardInterrupt:
        print("\nCrawling interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()