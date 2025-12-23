#!/usr/bin/env python3
"""
DNS Resolver Script
Resolves a domain name to its IPv4 address using Python's socket library.
Demonstrates basic DNS resolution using socket.gethostbyname() function.
"""

import socket
import sys


def resolve_domain(domain):
    """
    Resolve a domain name to its IPv4 address.
    
    Args:
        domain (str): The domain name to resolve
        
    Returns:
        str: The IPv4 address of the domain
        
    Raises:
        socket.gaierror: If the domain cannot be resolved
    """
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        raise socket.gaierror(f"Failed to resolve domain '{domain}': {e}")


def main():
    """
    Main function to handle command-line input and perform DNS resolution.
    """
    # Check if domain name is provided as command-line argument
    if len(sys.argv) != 2:
        print("Usage: python 0-dns_resolver.py <domain_name>")
        print("Example: python 0-dns_resolver.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1].strip()
    
    # Validate domain input
    if not domain:
        print("Error: Domain name cannot be empty")
        sys.exit(1)
    
    print("=" * 60)
    print(f"Resolving: {domain}")
    print("=" * 60)
    
    try:
        # Resolve the domain to IPv4 address
        ip_address = resolve_domain(domain)
        print(f"IPv4 Resolution: {domain} → {ip_address}")
    except socket.gaierror as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    
    print("=" * 60)


if __name__ == "__main__":
    main()