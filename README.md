# HAR File Analyzer

A pair of Python utilities for analyzing HTTP Archive (HAR) files captured from web browsers. Extract HTTP headers, search for specific headers, and analyze network traffic across multiple captures.

## Overview

These scripts help you:
- **View all HTTP headers** captured in a HAR file
- **Search for specific headers** by name and value
- **Analyze multiple HAR files** at once
- **Export network traffic information** (domains, header counts, etc.)
- **Debug network issues** by inspecting captured traffic

## Scripts

### `har_analyzer.py` - Single File Analysis
Analyzes individual HAR files to display headers, domains, and traffic information.

### `har_analyzer_batch.py` - Batch Analysis
Analyzes multiple HAR files at once and can search across all files simultaneously.

## Requirements

- **Python 3.6+**
- **No external dependencies** - uses only Python standard library

## Installation

1. Save both scripts to your preferred location:
   ```bash
   /Users/cassle/Downloads/har_analyzer.py
   /Users/cassle/Downloads/har_analyzer_batch.py
   ```

2. (Optional) Make scripts executable:
   ```bash
   chmod +x /Users/cassle/Downloads/har_analyzer.py
   chmod +x /Users/cassle/Downloads/har_analyzer_batch.py
   ```

3. (Optional) Add to your PATH for easy access:
   ```bash
   export PATH="/Users/cassle/Downloads:$PATH"
   ```

## Usage

### Single File Analysis

#### View Summary
Display all x-headers, domains, and file information:
```bash
python3 har_analyzer.py file.har
```

**Example Output:**
```
================================================================================
HAR FILE ANALYSIS SUMMARY
================================================================================

File: www.example.com.har
Size: 25.13 MB (26,350,000 bytes)
Entries: 432

X-Headers Found: 19
--------------------------------------------------------------------------------
  x-browser-channel
  x-browser-copyright
  x-cache
  x-content-type-options
  ...

Domains Captured: 45
--------------------------------------------------------------------------------
  api.example.com
  cdn.example.com
  analytics.example.com
  ...
```

#### Search for Specific Header
Find a header by name:
```bash
python3 har_analyzer.py file.har --search x-custom-header
```

#### Search for Header with Value
Find headers matching both name and value:
```bash
python3 har_analyzer.py file.har --search x-request-id abc123
```

**Search Results Output:**
```
================================================================================
SEARCH RESULTS FOR: x-request-id
VALUE FILTER: abc123
================================================================================

Found 2 matching headers:

  URL: https://api.example.com/endpoint
  Type: Request
  Value: abc123-xyz789

  URL: https://api.example.com/data
  Type: Response
  Value: abc123-response
```

### Batch Analysis

#### Analyze Multiple Files
Summarize multiple HAR files:
```bash
python3 har_analyzer_batch.py file1.har file2.har file3.har
```

Using wildcards:
```bash
python3 har_analyzer_batch.py ~/Downloads/*.har
python3 har_analyzer_batch.py /path/to/captures/*.har
```

**Batch Summary Output:**
```
================================================================================
HAR BATCH ANALYSIS
================================================================================

Analyzing 4 files:

File                                     Size (MB)    Entries    X-Headers
--------------------------------------------------------------------------------
chatgpt.com.har                          25.13        432        19
copilot.microsoft.com.har                16.50        223        26
gemini.google.com.har                    22.61        79         15
example-site.har                         42.97        567        76
```

#### Search Across Multiple Files
Find a header across all files:
```bash
python3 har_analyzer_batch.py *.har --search x-custom-header
```

Find header with specific value:
```bash
python3 har_analyzer_batch.py *.har --search x-request-id abc123
```

**Batch Search Output:**
```
================================================================================
HAR BATCH ANALYSIS
================================================================================

SEARCHING FOR: x-request-id
VALUE FILTER: abc123
--------------------------------------------------------------------------------

Found in 2/4 files:

file1.har: ✓ FOUND
  Matches: 3
    - Request: abc123-request-1
    - Response: abc123-response-1

file2.har: ✗ NOT FOUND

file3.har: ✓ FOUND
  Matches: 1
    - Request: abc123-request-2

file4.har: ✗ NOT FOUND
```

## Features

### Single File Analysis
- ✅ List all x-headers found in the file
- ✅ Show file size and number of entries
- ✅ Extract all domains captured
- ✅ Search for specific headers by name
- ✅ Filter results by header value
- ✅ Display request and response headers separately
- ✅ Show URLs where headers are found

### Batch Analysis
- ✅ Analyze multiple files in one command
- ✅ Summarize key metrics (size, entries, header count)
- ✅ Search across all files simultaneously
- ✅ Compare header counts across captures
- ✅ Find which files contain specific headers

## Common Use Cases

### 1. Finding Missing Headers
Check if a specific header was captured:
```bash
python3 har_analyzer.py capture.har --search x-ps-ext
```

### 2. Comparing Network Traffic Across Sites
Get a quick overview of multiple site captures:
```bash
python3 har_analyzer_batch.py site1.har site2.har site3.har
```

### 3. Debugging API Responses
Find all custom headers in API responses:
```bash
python3 har_analyzer.py api-capture.har --search x-api
```

### 4. Compliance/Security Audit
Search for security headers across multiple captures:
```bash
python3 har_analyzer_batch.py *.har --search x-frame-options
python3 har_analyzer_batch.py *.har --search x-xss-protection
python3 har_analyzer_batch.py *.har --search x-content-type-options
```

### 5. Finding Tracking/Analytics Headers
Identify third-party tracking across captures:
```bash
python3 har_analyzer_batch.py *.har --search x-facebook
python3 har_analyzer_batch.py *.har --search x-pinterest
```

## How to Capture HAR Files

### In Google Chrome
1. Open **Developer Tools** (F12 or Cmd+Option+I)
2. Go to the **Network** tab
3. Visit the website(s) you want to analyze
4. Right-click in the Network panel
5. Select **Save all as HAR with content**
6. Choose a location and filename

### In Firefox
1. Open **Developer Tools** (F12)
2. Go to the **Network** tab
3. Visit the website(s) to capture
4. Right-click in the Network panel
5. Select **Save All As HAR**

### In Safari
1. Open **Develop menu** (enable in Preferences → Advanced)
2. Go to **Develop → Show Web Inspector**
3. Go to **Network** tab
4. Visit website(s)
5. File → Export Network Report

## Tips & Tricks

### 1. Filter by Header Type
To see only custom headers (x-*), the scripts automatically filter for headers starting with "x-"

### 2. Case-Insensitive Search
Header searches are case-insensitive:
```bash
python3 har_analyzer.py file.har --search X-Custom-Header
python3 har_analyzer.py file.har --search x-custom-header
# Both work the same
```

### 3. Partial Value Matching
Value searches match partial strings:
```bash
# Will find headers with values containing "2024"
python3 har_analyzer.py file.har --search x-header 2024
```

### 4. Large File Handling
Both scripts can handle large HAR files efficiently:
```bash
python3 har_analyzer.py huge-capture-500mb.har
```

### 5. Batch Processing with Glob Patterns
Use shell globbing for flexible batch processing:
```bash
# All .har files in current directory
python3 har_analyzer_batch.py *.har

# All .har files in subdirectory
python3 har_analyzer_batch.py captures/*.har

# All .har files recursively
python3 har_analyzer_batch.py **/*.har
```

## Troubleshooting

### Error: File not found
```bash
python3 har_analyzer.py /path/to/file.har
```
Ensure the path is correct and the file exists.

### Error: Failed to parse HAR file
The HAR file may be corrupted or not valid JSON. Try:
1. Re-export the HAR file from your browser
2. Check the file wasn't edited or truncated

### No matches found
- Header may not exist in the capture
- Try searching without a value filter first to see available headers
- Use wildcards: `python3 har_analyzer_batch.py *.har --search x-`

### Command not found
Make sure you're using the correct path:
```bash
python3 /Users/cassle/Downloads/har_analyzer.py file.har
```

Or add the directory to PATH:
```bash
export PATH="/Users/cassle/Downloads:$PATH"
har_analyzer.py file.har
```

## Performance Notes

- **Single file analysis**: Near-instant for typical captures (25-50MB)
- **Batch analysis**: 5-10 seconds for 4+ large files
- **Search across files**: Linear complexity - faster with fewer files to scan
- **Memory usage**: Depends on HAR file size (loads entire JSON into memory)

## Examples

### Example 1: Audit all captured domains
```bash
python3 har_analyzer.py website.har
# Shows all domains connected to during page load
```

### Example 2: Find security headers
```bash
python3 har_analyzer_batch.py *.har --search x-xss-protection
python3 har_analyzer_batch.py *.har --search content-security-policy
```

### Example 3: Debug API calls
```bash
python3 har_analyzer.py api-capture.har --search x-request-id
# Find all request IDs in the capture
```

### Example 4: Compare three competitor websites
```bash
python3 har_analyzer_batch.py site-a.har site-b.har site-c.har
# See header counts and domains for each
```

## File Structure

```
.
├── har_analyzer.py           # Single file analysis tool
├── har_analyzer_batch.py     # Batch analysis tool
└── README.md                 # This file
```

## License

These scripts are provided as-is for personal use.

## FAQ

**Q: Will these scripts modify my HAR files?**
A: No, they are read-only. Your HAR files are never modified.

**Q: Can I use these with HAR files from other sources?**
A: Yes, as long as they're valid HAR format (JSON).

**Q: What's the maximum file size these can handle?**
A: Limited only by your system RAM. Tested with files up to 500MB+

**Q: Can I export the results?**
A: Yes, redirect output to a file:
```bash
python3 har_analyzer.py file.har > results.txt
```

**Q: Why search for x-headers specifically?**
A: Custom headers (starting with x-) are used for debugging, analytics, and custom business logic. They're often most interesting to analyze.

**Q: Can I search for regular (non-x-) headers?**
A: Yes, modify the scripts to remove the "startswith('x-')" filter or use grep on the output.

## Support

For issues or questions:
1. Verify your HAR file is valid JSON
2. Check file permissions
3. Try with a smaller sample HAR file first
4. Review the error message carefully

---

**Last Updated:** March 2026
**Python Version:** 3.6+
