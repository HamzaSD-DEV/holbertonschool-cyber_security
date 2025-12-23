#!/usr/bin/env python3
"""
Complete Network Reconnaissance Tool
Integrates DNS, web, and port scanning into a single reconnaissance workflow.
Combines DNS resolution, HTTP analysis, and port scanning for comprehensive target assessment.
"""

import socket
import sys
import time
from urllib.parse import urlparse

try:
    import requests
    import dns.resolver
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error: Required library not found: {e}")
    print("Install required libraries with:")
    print("  pip install requests dnspython beautifulsoup4")
    sys.exit(1)


class NetworkRecon:
    """
    Complete network reconnaissance class integrating multiple scanning techniques.
    """
    
    def __init__(self, target):
        """
        Initialize reconnaissance tool with target domain.
        
        Args:
            target (str): Target domain to reconnaissance
        """
        self.target = target.strip().lower()
        self.ip_address = None
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
        
        # Results storage
        self.dns_results = {}
        self.web_results = {}
        self.port_results = {}
    
    def dns_recon(self):
        """
        Perform DNS reconnaissance including IP resolution and MX records.
        
        Returns:
            dict: DNS reconnaissance results
        """
        print("DNS RECONNAISSANCE")
        results = {}
        
        try:
            # Resolve IP address
            self.ip_address = socket.gethostbyname(self.target)
            results['ip_address'] = self.ip_address
            print(f"IP Address: {self.ip_address}")
            
        except socket.gaierror:
            results['ip_address'] = "Resolution failed"
            print(f"IP Address: Resolution failed")
        
        # Get MX records
        try:
            mx_records = dns.resolver.resolve(self.target, 'MX')
            mx_list = []
            for mx in mx_records:
                mx_record = f"{mx.preference} {mx.exchange}"
                mx_list.append(mx_record)
            
            results['mx_records'] = mx_list
            print(f"\nMX Records: {', '.join(mx_list)}")
            
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
            results['mx_records'] = []
            print(f"\nMX Records: None found")
        
        self.dns_results = results
        return results
    
    def web_recon(self):
        """
        Perform web reconnaissance including HTTP headers and link analysis.
        
        Returns:
            dict: Web reconnaissance results
        """
        print("\nWEB RECONNAISSANCE")
        results = {}
        
        # Try HTTPS first, then HTTP
        protocols = ['https', 'http']
        
        for protocol in protocols:
            url = f"{protocol}://{self.target}"
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (compatible; ReconTool/1.0)'
                }
                
                response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
                
                # Store status code
                results['status_code'] = response.status_code
                results['protocol'] = protocol
                results['final_url'] = response.url
                print(f"Status Code: {response.status_code}")
                
                # Analyze important headers
                important_headers = ['Server', 'Content-Type', 'X-Powered-By', 'X-Frame-Options']
                header_info = []
                
                for header in important_headers:
                    if header in response.headers:
                        header_info.append(f"{header}: {response.headers[header]}")
                
                results['headers'] = header_info
                if header_info:
                    print(f"\nImportant Headers: {' '.join(header_info)}")
                else:
                    print(f"\nImportant Headers: None found")
                
                # Count links in HTML content
                try:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = soup.find_all('a', href=True)
                    link_count = len(links)
                    
                    results['link_count'] = link_count
                    print(f"\nTotal Links Found: {link_count}")
                    
                except Exception:
                    results['link_count'] = 0
                    print(f"\nTotal Links Found: 0 (parsing error)")
                
                break  # Success, no need to try other protocols
                
            except requests.exceptions.RequestException:
                continue  # Try next protocol
        
        else:
            # No protocols worked
            results['status_code'] = "Connection failed"
            results['headers'] = []
            results['link_count'] = 0
            print(f"Status Code: Connection failed")
            print(f"\nImportant Headers: Connection failed")
            print(f"\nTotal Links Found: 0")
        
        self.web_results = results
        return results
    
    def port_scan(self):
        """
        Perform port scanning on common ports.
        
        Returns:
            dict: Port scanning results
        """
        print("\nPORT SCANNING")
        print(f"Scanning common ports on {self.target}...")
        
        results = {'open_ports': [], 'closed_ports': []}
        
        target_ip = self.ip_address or self.target
        
        for port in self.common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                result = sock.connect_ex((target_ip, port))
                sock.close()
                
                if result == 0:
                    results['open_ports'].append(port)
                else:
                    results['closed_ports'].append(port)
                    
            except Exception:
                results['closed_ports'].append(port)
        
        # Display open ports
        if results['open_ports']:
            print("Open ports:")
            for port in results['open_ports']:
                print(f"  Port {port}: OPEN")
        else:
            print("Open ports: None found")
        
        self.port_results = results
        return results
    
    def check_single_port(self, host, port, timeout=2):
        """
        Check if a single port is open.
        
        Args:
            host (str): Target host
            port (int): Port to check
            timeout (int): Connection timeout
            
        Returns:
            bool: True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def run_full_recon(self):
        """
        Run complete reconnaissance workflow.
        
        Returns:
            dict: Complete reconnaissance results
        """
        print("NETWORK RECONNAISSANCE TOOL")
        print(f"Target: {self.target}")
        print("=" * 50)
        
        # DNS Reconnaissance
        dns_results = self.dns_recon()
        print("=" * 50)
        
        # Web Reconnaissance
        web_results = self.web_recon()
        print("=" * 50)
        
        # Port Scanning
        port_results = self.port_scan()
        print("=" * 50)
        
        print("RECONNAISSANCE COMPLETE")
        
        # Compile full results
        full_results = {
            'target': self.target,
            'dns': dns_results,
            'web': web_results,
            'ports': port_results,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return full_results


def validate_domain(domain):
    """
    Validate domain name format.
    
    Args:
        domain (str): Domain to validate
        
    Returns:
        str or None: Cleaned domain or None if invalid
    """
    if not domain:
        return None
    
    # Remove protocol if present
    if domain.startswith(('http://', 'https://')):
        parsed = urlparse(domain)
        domain = parsed.netloc or parsed.path
    
    # Remove www. prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # Basic domain validation
    if '.' not in domain or len(domain) > 255:
        return None
    
    return domain.strip().lower()


def main():
    """
    Main function to handle user input and coordinate reconnaissance.
    """
    try:
        print("NETWORK RECONNAISSANCE TOOL")
        target = input("Enter target domain: ").strip()
        
        if not target:
            print("Error: Target domain cannot be empty")
            sys.exit(1)
        
        # Validate and clean domain
        cleaned_target = validate_domain(target)
        if not cleaned_target:
            print("Error: Invalid domain format")
            sys.exit(1)
        
        print(f"\nStarting reconnaissance of {cleaned_target}...")
        print("=" * 50)
        
        # Create reconnaissance tool and run
        recon = NetworkRecon(cleaned_target)
        results = recon.run_full_recon()
        
        # Optional: Save results to file
        # with open(f'recon_{cleaned_target}_{int(time.time())}.json', 'w') as f:
        #     import json
        #     json.dump(results, f, indent=2)
        
    except KeyboardInterrupt:
        print("\nReconnaissance interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()