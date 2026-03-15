#!/usr/bin/env python3
"""
HAR File Batch Analyzer - Analyze multiple HAR files and search across them
"""

import json
import sys
import os
from pathlib import Path
from har_analyzer import HARAnalyzer


def batch_analyze(har_files: list, search_header: str = None, search_value: str = None):
    """Analyze multiple HAR files"""

    print("=" * 80)
    print("HAR BATCH ANALYSIS")
    print("=" * 80)
    print()

    results = []

    for har_file in har_files:
        if not os.path.exists(har_file):
            print(f"⚠️  File not found: {har_file}")
            continue

        try:
            analyzer = HARAnalyzer(har_file)
            filename = os.path.basename(har_file)

            if search_header:
                # Search mode
                matches = analyzer.search_header(search_header, search_value)
                if matches:
                    results.append({
                        'file': filename,
                        'found': True,
                        'count': len(matches),
                        'matches': matches
                    })
                else:
                    results.append({
                        'file': filename,
                        'found': False,
                        'count': 0,
                        'matches': []
                    })
            else:
                # Summary mode
                info = analyzer.get_file_info()
                x_headers = analyzer.get_x_headers()
                # Check for x-ps-ext header
                x_ps_ext_found = any(h.lower() == 'x-ps-ext' for h in x_headers)
                results.append({
                    'file': filename,
                    'size_mb': info['size_mb'],
                    'entries': info['entries'],
                    'x_headers_count': len(x_headers),
                    'x_headers': x_headers[:10],  # Show first 10
                    'has_x_ps_ext': x_ps_ext_found
                })

        except Exception as e:
            print(f"❌ Error processing {har_file}: {e}")

    # Print results
    if search_header:
        print(f"SEARCHING FOR: {search_header}")
        if search_value:
            print(f"VALUE FILTER: {search_value}")
        print("-" * 80)
        print()

        found_count = sum(1 for r in results if r['found'])
        print(f"Found in {found_count}/{len(results)} files:\n")

        for result in results:
            status = "✓ FOUND" if result['found'] else "✗ NOT FOUND"
            print(f"{result['file']}: {status}")
            if result['found']:
                print(f"  Matches: {result['count']}")
                for url, value, header_type in result['matches'][:3]:  # Show first 3
                    print(f"    - {header_type}: {value[:50]}...")
            print()

    else:
        print(f"Analyzing {len(results)} files:\n")
        print(f"{'File':<40} {'Size (MB)':<12} {'Entries':<10} {'X-Headers':<10} {'x-ps-ext':<12}")
        print("-" * 90)

        for result in results:
            x_ps_ext_status = "✓ YES" if result['has_x_ps_ext'] else "✗ NO"
            print(f"{result['file']:<40} {result['size_mb']:<12.2f} {result['entries']:<10} {result['x_headers_count']:<10} {x_ps_ext_status:<12}")

        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 har_analyzer_batch.py <har_file1> [har_file2] ... [--search <header> [<value>]]")
        print()
        print("Examples:")
        print("  python3 har_analyzer_batch.py *.har")
        print("  python3 har_analyzer_batch.py file1.har file2.har file3.har")
        print("  python3 har_analyzer_batch.py *.har --search x-ps-ext")
        print("  python3 har_analyzer_batch.py *.har --search x-ps-ext 2024")
        sys.exit(1)

    # Parse arguments
    har_files = []
    search_header = None
    search_value = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--search':
            if i + 1 < len(sys.argv):
                search_header = sys.argv[i + 1]
                i += 2
                if i < len(sys.argv) and not sys.argv[i].startswith('--'):
                    search_value = sys.argv[i]
                    i += 1
            else:
                print("Error: --search requires a header name")
                sys.exit(1)
        else:
            har_files.append(arg)
            i += 1

    if not har_files:
        print("Error: No HAR files provided")
        sys.exit(1)

    batch_analyze(har_files, search_header, search_value)


if __name__ == '__main__':
    main()
