#!/usr/bin/env python3
"""
Port Scanner Script
Checks if a specific port is open on a host using TCP socket connection.
Demonstrates low-level network programming with socket module.
"""

import socket
import sys
import time


def check_port(host, port, timeout=3):
    """
    Check if a specific port is open on a host.
    
    Args:
        host (str): The hostname or IP address to check
        port (int): The port number to check
        timeout (int): Connection timeout in seconds
        
    Returns:
        tuple: (is_open, status_message)
    """
    try:
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set socket timeout
        sock.settimeout(timeout)
        
        # Attempt to connect to the host and port
        # connect_ex() returns 0 if successful, non-zero if failed
        result = sock.connect_ex((host, port))
        
        # Close the socket
        sock.close()
        
        # Check the result
        if result == 0:
            return True, "OPEN"
        else:
            return False, "CLOSED"
            
    except socket.gaierror as e:
        # Name resolution error
        return False, f"DNS ERROR: {e}"
    except socket.timeout:
        # Connection timeout
        return False, "TIMEOUT"
    except ConnectionRefusedError:
        # Connection explicitly refused
        return False, "CLOSED"
    except Exception as e:
        # Other socket errors
        return False, f"ERROR: {e}"


def resolve_hostname(host):
    """
    Resolve hostname to IP address for display purposes.
    
    Args:
        host (str): Hostname or IP address
        
    Returns:
        str: IP address or original host if resolution fails
    """
    try:
        ip_address = socket.gethostbyname(host)
        return ip_address
    except socket.gaierror:
        return host


def validate_port(port_str):
    """
    Validate port number input.
    
    Args:
        port_str (str): Port number as string
        
    Returns:
        int or None: Valid port number or None if invalid
    """
    try:
        port = int(port_str)
        if 1 <= port <= 65535:
            return port
        else:
            print("Error: Port number must be between 1 and 65535")
            return None
    except ValueError:
        print("Error: Port must be a valid number")
        return None


def display_scan_result(host, port, is_open, status, ip_address=None):
    """
    Display the port scan result in a formatted way.
    
    Args:
        host (str): Target hostname
        port (int): Target port
        is_open (bool): Whether port is open
        status (str): Status message
        ip_address (str): Resolved IP address
    """
    print(f"Port {port} on {host}: {status}")
    
    if ip_address and ip_address != host:
        print(f"  Resolved IP: {ip_address}")
    
    if is_open:
        print(f"  Status: Connection successful")
    else:
        if status == "CLOSED":
            print(f"  Status: Port is closed or filtered")
        elif status == "TIMEOUT":
            print(f"  Status: Connection timed out")
        else:
            print(f"  Status: {status}")


def main():
    """
    Main function to handle user input and coordinate port scanning.
    """
    try:
        # Get host from user input
        host = input("Enter host (IP or hostname): ").strip()
        
        if not host:
            print("Error: Host cannot be empty")
            sys.exit(1)
        
        # Get port from user input
        port_input = input("Enter port number: ").strip()
        
        if not port_input:
            print("Error: Port number cannot be empty")
            sys.exit(1)
        
        # Validate port number
        port = validate_port(port_input)
        if port is None:
            sys.exit(1)
        
        print(f"\nScanning {host}:{port}...")
        
        # Resolve hostname to IP for display
        ip_address = resolve_hostname(host)
        
        # Record start time
        start_time = time.time()
        
        # Check if port is open
        is_open, status = check_port(host, port)
        
        # Record end time
        end_time = time.time()
        scan_time = round((end_time - start_time) * 1000, 2)
        
        # Display results
        display_scan_result(host, port, is_open, status, ip_address)
        print(f"  Scan time: {scan_time}ms")
        
    except KeyboardInterrupt:
        print("\nPort scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()