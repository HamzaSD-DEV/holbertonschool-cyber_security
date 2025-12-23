#!/usr/bin/env python3
"""
Save DNS Results to File Script
Extends Task 2 - Reads domains from a file, resolves them, and saves results to an output file.
Demonstrates combined file reading and writing operations with formatted output.
"""

import socket
import sys
import os
from datetime import datetime


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
    Resolve multiple domains and collect results.
    
    Args:
        domains (list): List of domain names to resolve
        
    Returns:
        list: List of tuples containing (domain, ip_address) pairs
    """
    if not domains:
        print("No domains found in file")
        return []
    
    print(f"\nResolving {len(domains)} domains...")
    print("=" * 50)
    
    results = []
    for domain in domains:
        ip_address = resolve_domain(domain)
        print(f"{domain}: {ip_address}")
        results.append((domain, ip_address))
    
    return results


def save_results_to_file(results, output_filename):
    """
    Save DNS resolution results to a formatted output file.
    
    Args:
        results (list): List of tuples containing (domain, ip_address) pairs
        output_filename (str): Path to the output file
        
    Raises:
        IOError: If there's an error writing to the file
    """
    try:
        with open(output_filename, 'w') as file:
            # Write header
            file.write("DNS Resolution Results\n")
            file.write("=" * 50 + "\n\n")
            
            # Write results in formatted style
            for domain, ip_address in results:
                file.write(f"Domain: {domain}\n")
                file.write(f"IP Address: {ip_address}\n\n")
            
    except IOError as e:
        raise IOError(f"Error writing to file '{output_filename}': {e}")


def display_saved_file(output_filename):
    """
    Display the contents of the saved results file.
    
    Args:
        output_filename (str): Path to the output file to display
    """
    try:
        print(f"Saved File ({output_filename}):")
        print()
        with open(output_filename, 'r') as file:
            content = file.read()
            print(content)
    except IOError as e:
        print(f"Error reading saved file: {e}")


def main():
    """
    Main function to handle user input and coordinate DNS resolution with file operations.
    """
    try:
        # Get input filename from user
        input_filename = input("Enter input filename (domains): ").strip()
        
        if not input_filename:
            print("Error: Input filename cannot be empty")
            sys.exit(1)
        
        # Get output filename from user
        output_filename = input("Enter output filename (results): ").strip()
        
        if not output_filename:
            print("Error: Output filename cannot be empty")
            sys.exit(1)
        
        # Check if input file exists
        if not os.path.exists(input_filename):
            print(f"Error: Input file '{input_filename}' does not exist")
            sys.exit(1)
        
        # Read domains from input file
        try:
            domains = read_domains_from_file(input_filename)
        except (FileNotFoundError, IOError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        
        # Perform batch resolution and collect results
        results = batch_resolve_domains(domains)
        
        if not results:
            print("No results to save")
            sys.exit(1)
        
        # Save results to output file
        try:
            save_results_to_file(results, output_filename)
            print("=" * 50)
            print(f"Results saved to {output_filename}")
            
            # Display the saved file contents
            display_saved_file(output_filename)
            
        except IOError as e:
            print(f"Error saving results: {e}")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()