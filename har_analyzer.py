#!/usr/bin/env python3
"""
HAR File Analyzer - Extract and analyze HTTP headers from HAR files
Provides information about x- headers, domains, and more
"""

import json
import sys
import os
from pathlib import Path
from collections import defaultdict
from typing import Set, Dict, List, Tuple


class HARAnalyzer:
    def __init__(self, har_file: str):
        self.har_file = har_file
        self.file_size = os.path.getsize(har_file)
        self.data = self._load_har()

    def _load_har(self) -> dict:
        """Load and parse HAR file"""
        try:
            with open(self.har_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse HAR file: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: HAR file not found: {self.har_file}")
            sys.exit(1)

    def get_x_headers(self) -> Set[str]:
        """Extract all x- headers from the HAR file"""
        x_headers = set()

        if 'log' not in self.data or 'entries' not in self.data['log']:
            return x_headers

        for entry in self.data['log']['entries']:
            # Check request headers
            if 'request' in entry and 'headers' in entry['request']:
                for header in entry['request']['headers']:
                    if header.get('name', '').lower().startswith('x-'):
                        x_headers.add(header['name'])

            # Check response headers
            if 'response' in entry and 'headers' in entry['response']:
                for header in entry['response']['headers']:
                    if header.get('name', '').lower().startswith('x-'):
                        x_headers.add(header['name'])

        return sorted(x_headers)

    def get_domains(self) -> Set[str]:
        """Extract all domains from URLs in the HAR file"""
        domains = set()

        if 'log' not in self.data or 'entries' not in self.data['log']:
            return domains

        for entry in self.data['log']['entries']:
            if 'request' in entry and 'url' in entry['request']:
                url = entry['request']['url']
                # Extract domain from URL
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    if parsed.netloc:
                        domains.add(parsed.netloc)
                except:
                    pass

        return sorted(domains)

    def search_header(self, header_name: str, value: str = None) -> List[Tuple[str, str, str]]:
        """
        Search for a specific header by name and optionally value
        Returns list of tuples: (url, header_value, header_type)
        """
        results = []

        if 'log' not in self.data or 'entries' not in self.data['log']:
            return results

        header_name_lower = header_name.lower()

        for entry in self.data['log']['entries']:
            url = entry.get('request', {}).get('url', 'Unknown')

            # Check request headers
            if 'request' in entry and 'headers' in entry['request']:
                for header in entry['request']['headers']:
                    if header.get('name', '').lower() == header_name_lower:
                        header_value = header.get('value', '')
                        if value is None or value.lower() in header_value.lower():
                            results.append((url, header_value, 'Request'))

            # Check response headers
            if 'response' in entry and 'headers' in entry['response']:
                for header in entry['response']['headers']:
                    if header.get('name', '').lower() == header_name_lower:
                        header_value = header.get('value', '')
                        if value is None or value.lower() in header_value.lower():
                            results.append((url, header_value, 'Response'))

        return results

    def get_file_info(self) -> Dict:
        """Get basic file information"""
        return {
            'filename': os.path.basename(self.har_file),
            'size_bytes': self.file_size,
            'size_mb': round(self.file_size / (1024 * 1024), 2),
            'entries': len(self.data.get('log', {}).get('entries', []))
        }

    def print_summary(self):
        """Print a summary of the HAR file"""
        info = self.get_file_info()
        x_headers = self.get_x_headers()
        domains = self.get_domains()

        print("=" * 80)
        print("HAR FILE ANALYSIS SUMMARY")
        print("=" * 80)
        print()

        print(f"File: {info['filename']}")
        print(f"Size: {info['size_mb']} MB ({info['size_bytes']:,} bytes)")
        print(f"Entries: {info['entries']}")
        print()

        print(f"X-Headers Found: {len(x_headers)}")
        print("-" * 80)
        if x_headers:
            for header in x_headers:
                print(f"  {header}")
        else:
            print("  (none)")
        print()

        print(f"Domains Captured: {len(domains)}")
        print("-" * 80)
        if domains:
            for domain in domains:
                print(f"  {domain}")
        else:
            print("  (none)")
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 har_analyzer.py <har_file> [--search <header_name> [<value>]]")
        print()
        print("Examples:")
        print("  python3 har_analyzer.py file.har")
        print("  python3 har_analyzer.py file.har --search x-ps-ext")
        print("  python3 har_analyzer.py file.har --search x-ps-ext 2024")
        sys.exit(1)

    har_file = sys.argv[1]

    # Validate file exists
    if not os.path.exists(har_file):
        print(f"Error: File not found: {har_file}")
        sys.exit(1)

    analyzer = HARAnalyzer(har_file)

    # Check for search arguments
    if '--search' in sys.argv:
        search_idx = sys.argv.index('--search')
        if search_idx + 1 >= len(sys.argv):
            print("Error: --search requires a header name")
            sys.exit(1)

        header_name = sys.argv[search_idx + 1]
        search_value = None
        if search_idx + 2 < len(sys.argv):
            search_value = sys.argv[search_idx + 2]

        results = analyzer.search_header(header_name, search_value)

        print("=" * 80)
        print(f"SEARCH RESULTS FOR: {header_name}")
        if search_value:
            print(f"VALUE FILTER: {search_value}")
        print("=" * 80)
        print()

        if results:
            print(f"Found {len(results)} matching headers:\n")
            for url, value, header_type in results:
                print(f"  URL: {url}")
                print(f"  Type: {header_type}")
                print(f"  Value: {value}")
                print()
        else:
            print(f"No matches found for '{header_name}'")
            if search_value:
                print(f"with value containing '{search_value}'")
        print()
    else:
        # Print summary
        analyzer.print_summary()


if __name__ == '__main__':
    main()
