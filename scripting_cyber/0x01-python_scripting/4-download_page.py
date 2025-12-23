#!/usr/bin/env python3
"""
Web Page Download Script
Downloads and saves a web page's HTML content using the requests library.
Formats HTML nicely with BeautifulSoup's prettify() method.
"""

import sys
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error: Required library not found: {e}")
    print("Install required libraries with:")
    print("  pip install requests beautifulsoup4")
    sys.exit(1)


def download_web_page(url):
    """
    Download a web page and return its HTML content.
    
    Args:
        url (str): The URL to download
        
    Returns:
        tuple: (status_code, html_content) or (None, error_message)
    """
    try:
        # Add http:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Set a user agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the HTTP GET request
        response = requests.get(url, headers=headers, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            return response.status_code, response.text
        else:
            return response.status_code, f"HTTP Error: {response.status_code} - {response.reason}"
            
    except requests.exceptions.Timeout:
        return None, "Error: Request timed out"
    except requests.exceptions.ConnectionError:
        return None, "Error: Could not connect to the URL"
    except requests.exceptions.RequestException as e:
        return None, f"Error: {e}"
    except Exception as e:
        return None, f"Unexpected error: {e}"


def format_html(html_content):
    """
    Format HTML content using BeautifulSoup's prettify method.
    
    Args:
        html_content (str): Raw HTML content
        
    Returns:
        str: Prettified HTML content
    """
    try:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Return prettified HTML
        return soup.prettify()
        
    except Exception as e:
        print(f"Warning: Could not prettify HTML: {e}")
        return html_content


def display_web_content(url, html_content):
    """
    Display the web page content in a formatted way.
    
    Args:
        url (str): The URL that was downloaded
        html_content (str): The HTML content to display
    """
    print(f"\nPage content from {url}:")
    print("=" * 50)
    
    # Format the HTML content
    formatted_html = format_html(html_content)
    
    # Display the formatted content
    print(formatted_html)
    
    print("=" * 50)
    print(f"Content length: {len(html_content)} characters")


def main():
    """
    Main function to handle user input and coordinate web page download.
    """
    try:
        # Get URL from user input
        url = input("Enter URL: ").strip()
        
        if not url:
            print("Error: URL cannot be empty")
            sys.exit(1)
        
        print(f"\nDownloading content from: {url}")
        
        # Download the web page
        status_code, content = download_web_page(url)
        
        if status_code == 200:
            # Successfully downloaded - display content
            display_web_content(url, content)
        else:
            # Error occurred
            print(f"\nFailed to download page: {content}")
            if status_code:
                print(f"HTTP Status Code: {status_code}")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()