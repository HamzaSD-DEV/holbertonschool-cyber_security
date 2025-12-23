#!/usr/bin/env python3
"""
Batch DNS Resolution Script
Reads domain names from a file and resolves each one to its IP address.
Demonstrates file I/O operations and batch processing with socket.gethostbyname().
"""

import socket
import sys
import os


def read_domains_from_file(filename):
    """
    Read domain names from a text file, one domain per line.
    
    Args:
        filename (str): Path to the file containing domain names
        
    Returns:
        list: List of cleaned domain names
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(filename, 'r') as file:
            # Read all lines and clean them up
            domains = []
            for line in file.read().splitlines():
                domain = line.strip()
                if domain:  # Skip empty lines
                    domains.append(domain)
            return domains
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found")
    except IOError as e:
        raise IOError(f"Error reading file '{filename}': {e}")


def resolve_domain(domain):
    """
    Resolve a domain name to its IPv4 address.
    
    Args:
        domain (str): The domain name to resolve
        
    Returns:
        str: The IPv4 address or error message
    """
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return "Resolution failed"
    except Exception:
        return "Error"


def batch_resolve_domains(domains):
    """
    Resolve multiple domains and display results.
    
    Args:
        domains (list): List of domain names to resolve
    """
    if not domains:
        print("No domains found in file")
        return
    
    print(f"\nResolving {len(domains)} domains...")
    print("=" * 50)
    
    for domain in domains:
        ip_address = resolve_domain(domain)
        print(f"{domain}: {ip_address}")


def main():
    """
    Main function to handle user input and coordinate batch DNS resolution.
    """
    try:
        # Get filename from user input
        filename = input("Enter filename containing domains: ").strip()
        
        if not filename:
            print("Error: Filename cannot be empty")
            sys.exit(1)
        
        # Check if file exists
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' does not exist")
            sys.exit(1)
        
        # Read domains from file
        try:
            domains = read_domains_from_file(filename)
        except (FileNotFoundError, IOError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        # Perform batch resolution
        batch_resolve_domains(domains)
        
    except KeyboardInterrupt:
        print("\nBatch resolution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()