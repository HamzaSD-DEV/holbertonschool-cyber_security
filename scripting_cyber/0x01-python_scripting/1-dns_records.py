#!/usr/bin/env python3
"""
DNS Records Enumeration Script
Queries and displays all DNS record types using the dnspython library.
Retrieves A, AAAA, MX, NS, TXT, and SOA records in a readable format.
"""

import sys
try:
    import dns.resolver
    import dns.rdatatype
except ImportError:
    print("Error: dnspython library is required.")
    print("Install it with: pip install dnspython")
    sys.exit(1)


class DNSEnumerator:
    """
    Class to handle DNS record enumeration for various record types.
    """
    
    def __init__(self, domain):
        """
        Initialize DNS enumerator with target domain.
        
        Args:
            domain (str): The domain to enumerate DNS records for
        """
        self.domain = domain.strip().rstrip('.')
        self.record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
        self.results = {}
        self.total_records = 0
        self.found_types = 0
    
    def query_record_type(self, record_type):
        """
        Query a specific DNS record type for the domain.
        
        Args:
            record_type (str): The DNS record type to query
            
        Returns:
            list: List of record data or empty list if not found
        """
        try:
            answers = dns.resolver.resolve(self.domain, record_type)
            records = []
            
            for rdata in answers:
                if record_type == 'MX':
                    # MX records have preference and exchange
                    records.append(f"{rdata.preference} {rdata.exchange}")
                elif record_type == 'SOA':
                    # SOA records have multiple fields
                    records.append(f"Primary: {rdata.mname}, Admin: {rdata.rname}, Serial: {rdata.serial}")
                elif record_type == 'TXT':
                    # TXT records may have multiple strings, join them
                    txt_data = ''.join([s.decode() if isinstance(s, bytes) else str(s) for s in rdata.strings])
                    records.append(f'"{txt_data}"')
                else:
                    # A, AAAA, NS records - just the address/name
                    records.append(str(rdata))
            
            return records
            
        except dns.resolver.NXDOMAIN:
            return []
        except dns.resolver.NoAnswer:
            return []
        except dns.resolver.Timeout:
            return []
        except Exception:
            return []
    
    def enumerate_all_records(self):
        """
        Enumerate all DNS record types for the domain.
        """
        print("=" * 70)
        print(f"DNS Record Enumeration: {self.domain}")
        print("=" * 70)
        print()
        
        for record_type in self.record_types:
            records = self.query_record_type(record_type)
            
            if records:
                self.results[record_type] = records
                self.found_types += 1
                self.total_records += len(records)
                
                print(f"{record_type} Records ({len(records)}):")
                for record in records:
                    print(f"  • {record}")
                print()
        
        # Display summary
        print("=" * 70)
        print(f"Summary: Found {self.found_types} record types with {self.total_records} total records")
        print("=" * 70)
    
    def get_results(self):
        """
        Get the enumeration results.
        
        Returns:
            dict: Dictionary containing all found DNS records
        """
        return self.results


def main():
    """
    Main function to handle command-line input and perform DNS enumeration.
    """
    # Check if domain name is provided as command-line argument
    if len(sys.argv) != 2:
        print("Usage: python 1-dns_records.py <domain_name>")
        print("Example: python 1-dns_records.py google.com")
        sys.exit(1)
    
    domain = sys.argv[1].strip()
    
    # Validate domain input
    if not domain:
        print("Error: Domain name cannot be empty")
        sys.exit(1)
    
    try:
        # Create DNS enumerator and perform enumeration
        enumerator = DNSEnumerator(domain)
        enumerator.enumerate_all_records()
        
    except KeyboardInterrupt:
        print("\nEnumeration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error during DNS enumeration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()