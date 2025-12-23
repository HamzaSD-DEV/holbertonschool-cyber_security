#!/usr/bin/env python3
"""
HTTP Headers Analyzer Script
Retrieves and displays HTTP response headers from a website.
Shows status code, Server, Content-Type, and all other response headers.
"""

import sys
try:
    import requests
except ImportError:
    print("Error: requests library is required.")
    print("Install it with: pip install requests")
    sys.exit(1)


def get_http_headers(url):
    """
    Retrieve HTTP headers from a given URL.
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        tuple: (status_code, headers_dict, reason) or (None, None, error_message)
    """
    try:
        # Add https:// if no protocol is specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Set a realistic user agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make HTTP request (HEAD request is sufficient for headers, but some sites block it)
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        return response.status_code, dict(response.headers), response.reason
        
    except requests.exceptions.Timeout:
        return None, None, "Request timed out"
    except requests.exceptions.ConnectionError:
        return None, None, "Could not connect to the URL"
    except requests.exceptions.RequestException as e:
        return None, None, f"Request error: {e}"
    except Exception as e:
        return None, None, f"Unexpected error: {e}"


def analyze_headers(headers):
    """
    Analyze headers for security-related information.
    
    Args:
        headers (dict): Dictionary of HTTP headers
        
    Returns:
        list: List of security observations
    """
    security_headers = [
        'X-Frame-Options',
        'Content-Security-Policy',
        'X-XSS-Protection',
        'X-Content-Type-Options',
        'Strict-Transport-Security',
        'Content-Security-Policy-Report-Only'
    ]
    
    observations = []
    
    # Check for security headers
    found_security_headers = [header for header in security_headers if header in headers]
    if found_security_headers:
        observations.append(f"Security headers found: {', '.join(found_security_headers)}")
    
    # Check for server information
    if 'Server' in headers:
        observations.append(f"Server software: {headers['Server']}")
    
    # Check for cookies
    if 'Set-Cookie' in headers:
        observations.append("Cookies are being set by the server")
    
    return observations


def display_headers(url, status_code, headers, reason):
    """
    Display HTTP headers in a formatted way.
    
    Args:
        url (str): The URL that was analyzed
        status_code (int): HTTP status code
        headers (dict): Dictionary of HTTP headers
        reason (str): HTTP reason phrase
    """
    print(f"\nHTTP Headers for: {url}")
    print("=" * 50)
    print(f"Status Code: {status_code}")
    
    if reason:
        print(f"Reason: {reason}")
    
    print(f"\nHeaders:")
    
    # Display headers in alphabetical order for consistency
    for header, value in sorted(headers.items()):
        print(f"  {header}: {value}")
    
    # Analyze headers for security information
    observations = analyze_headers(headers)
    
    if observations:
        print(f"\nAnalysis:")
        for observation in observations:
            print(f"  • {observation}")


def main():
    """
    Main function to handle user input and coordinate header analysis.
    """
    try:
        # Get URL from user input
        url = input("Enter URL: ").strip()
        
        if not url:
            print("Error: URL cannot be empty")
            sys.exit(1)
        
        print(f"\nAnalyzing headers for: {url}")
        
        # Get HTTP headers
        status_code, headers, reason = get_http_headers(url)
        
        if status_code is not None:
            # Successfully retrieved headers - display them
            display_headers(url, status_code, headers, reason)
        else:
            # Error occurred
            print(f"Failed to retrieve headers: {reason}")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nHeader analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()