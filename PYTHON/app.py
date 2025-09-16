import re
import subprocess
import tempfile
import os
import json
from typing import List, Optional


def extract_m3u8_from_obfuscated_js(js_code: str) -> List[str]:
    """
    Extract M3U8 links from obfuscated JavaScript by executing it in Node.js.

    Args:
        js_code (str): The obfuscated JavaScript code

    Returns:
        List[str]: List of valid M3U8 URLs
    """

    try:
        # Method 1: Try to execute the JavaScript and capture output
        urls = execute_js_and_capture_urls(js_code)
        if urls:
            return urls
    except Exception as e:
        print(f"JavaScript execution failed: {e}")

    # Method 2: Manual deobfuscation of this specific pattern
    try:
        urls = manual_deobfuscation(js_code)
        if urls:
            return urls
    except Exception as e:
        print(f"Manual deobfuscation failed: {e}")

    # Method 3: Extract from document.write if present
    try:
        urls = extract_from_document_write(js_code)
        if urls:
            return urls
    except Exception as e:
        print(f"Document.write extraction failed: {e}")

    return []


def execute_js_and_capture_urls(js_code: str) -> List[str]:
    """
    Execute JavaScript code in Node.js and capture any URLs it generates.
    """

    # Create a wrapper that captures document.write calls and console output
    wrapper_js = f"""
// Mock document object to capture document.write calls
global.document = {{
    write: function(content) {{
        console.log('DOCUMENT_WRITE:', content);
    }},
    innerHTML: '',
    querySelector: function() {{ return null; }},
    addEventListener: function() {{}}
}};

// Mock window object
global.window = global;

// Capture console.log
const originalLog = console.log;
console.log = function(...args) {{
    originalLog('OUTPUT:', ...args);
}};

try {{
    // Execute the obfuscated code
    {js_code}
    
    // Try to extract any URLs from global variables
    for (let key in global) {{
        if (typeof global[key] === 'string' && global[key].includes('.m3u8')) {{
            console.log('FOUND_URL:', global[key]);
        }}
    }}
    
}} catch (error) {{
    console.log('ERROR:', error.message);
}}
"""

    try:
        # Write to temporary file and execute with Node.js
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            f.write(wrapper_js)
            temp_file = f.name

        # Execute with Node.js
        result = subprocess.run(
            ["node", temp_file], capture_output=True, text=True, timeout=10
        )

        # Clean up
        os.unlink(temp_file)

        # Parse output for URLs
        urls = []
        for line in result.stdout.split("\n"):
            if "DOCUMENT_WRITE:" in line or "FOUND_URL:" in line:
                # Extract URLs from the output
                url_matches = re.findall(r'https://[^\s<>"\']+\.m3u8[^\s<>"\']*', line)
                urls.extend(url_matches)

        return list(set(urls))

    except Exception as e:
        print(f"Node.js execution failed: {e}")
        return []


def manual_deobfuscation(js_code: str) -> List[str]:
    """
    Manual deobfuscation specifically for this type of obfuscated code.
    """

    # This code uses a string array and index-based access
    # First, find the string array

    # Pattern to find the main string array (usually contains base64-like strings)
    array_pattern = r"var\s+\w+\s*=\s*function\(\)\s*{\s*var\s+\w+\s*=\s*\[(.*?)\];"
    array_match = re.search(array_pattern, js_code, re.DOTALL)

    if not array_match:
        # Try alternative pattern
        array_pattern = r"function\s+\w+\(\)\s*{\s*var\s+\w+\s*=\s*\[(.*?)\];"
        array_match = re.search(array_pattern, js_code, re.DOTALL)

    if array_match:
        array_content = array_match.group(1)

        # Extract all strings from the array
        strings = re.findall(r"['\"]([^'\"]+)['\"]", array_content)

        # Decode base64-encoded strings
        decoded_strings = []
        for s in strings:
            try:
                # Try to decode as base64
                import base64

                if len(s) > 4:
                    decoded = base64.b64decode(s + "==").decode(
                        "utf-8", errors="ignore"
                    )
                    decoded_strings.append(decoded)
            except:
                pass
            decoded_strings.append(s)

        # Look for M3U8 URLs in decoded strings
        urls = []
        for s in decoded_strings:
            if ".m3u8" in s.lower():
                # Clean up the string
                url_matches = re.findall(r'https?://[^\s<>"\']+\.m3u8[^\s<>"\']*', s)
                urls.extend(url_matches)

        return list(set(urls))

    return []


def extract_from_document_write(js_code: str) -> List[str]:
    """
    Extract URLs from document.write statements.
    """

    # Look for document.write or similar DOM manipulation
    write_patterns = [
        r"document\[[^\]]+\]\([^)]+\)",
        r"document\.write\([^)]+\)",
        r"innerHTML\s*=\s*[^;]+",
    ]

    urls = []

    for pattern in write_patterns:
        matches = re.findall(pattern, js_code, re.IGNORECASE)
        for match in matches:
            # Look for URLs in the document.write content
            url_matches = re.findall(r'https://[^\s<>"\']+\.m3u8[^\s<>"\']*', match)
            urls.extend(url_matches)

    return list(set(urls))


def decode_hex_strings(js_code: str) -> str:
    """
    Decode hex-encoded strings in the JavaScript code.
    """

    # Look for hex patterns like \x22, \x20, etc.
    hex_pattern = r"\\x([0-9a-fA-F]{2})"

    def hex_replace(match):
        hex_value = match.group(1)
        return chr(int(hex_value, 16))

    decoded = re.sub(hex_pattern, hex_replace, js_code)
    return decoded


def extract_final_urls(js_code: str) -> List[str]:
    """
    Extract the final constructed URLs from the JavaScript code.
    This looks at the end of the code where URLs are typically constructed.
    """

    # First decode any hex strings
    decoded_js = decode_hex_strings(js_code)

    # Look for the final part where URLs are constructed
    # The code seems to end with document write statements
    final_part = decoded_js[-2000:]  # Look at last 2000 characters

    # Extract all potential URLs
    url_pattern = r'https://[^"\'\s<>]+\.m3u8[^"\'\s<>]*'
    urls = re.findall(url_pattern, final_part, re.IGNORECASE)

    # Clean up URLs
    cleaned_urls = []
    for url in urls:
        # Remove any trailing non-URL characters
        cleaned = re.sub(r"[^a-zA-Z0-9\-\./:?&=_]+$", "", url)
        if cleaned and cleaned not in cleaned_urls:
            cleaned_urls.append(cleaned)

    return cleaned_urls


# Simple alternative that focuses on the visible URL patterns
def simple_extraction(js_code: str) -> List[str]:
    """
    Simple extraction that looks for obvious URL patterns.
    """

    # Look for complete URLs that are more obviously formed
    patterns = [
        r'https://r466[^"\'<>\s]*\.m3u8',
        r'https://[^"\'<>\s]*scdns\.io[^"\'<>\s]*\.m3u8',
        r'https://[^"\'<>\s]*faselhds[^"\'<>\s]*\.m3u8',
    ]

    urls = []
    for pattern in patterns:
        matches = re.findall(pattern, js_code, re.IGNORECASE)
        for match in matches:
            # Clean the URL
            clean_url = re.sub(r"[^a-zA-Z0-9\-\./:?&=_]+$", "", match)
            if clean_url not in urls:
                urls.append(clean_url)

    return urls


# Main function - use this one
def get_m3u8_links(js_code: str) -> List[str]:
    """
    Main function to extract M3U8 links from obfuscated JavaScript.

    Usage:
        with open('paste.txt', 'r') as f:
            js_code = f.read()

        urls = get_m3u8_links(js_code)
        for url in urls:
            print(url)

    Args:
        js_code (str): The obfuscated JavaScript code as string

    Returns:
        List[str]: List of M3U8 streaming URLs
    """

    print("Attempting to extract M3U8 links...")

    # Try simple extraction first
    urls = simple_extraction(js_code)
    if urls:
        print(f"Found {len(urls)} URLs using simple extraction")
        return urls

    # Try final URL extraction
    urls = extract_final_urls(js_code)
    if urls:
        print(f"Found {len(urls)} URLs using final extraction")
        return urls

    # Try the complex method
    urls = extract_m3u8_from_obfuscated_js(js_code)
    if urls:
        print(f"Found {len(urls)} URLs using complex extraction")
        return urls

    print(
        "No valid M3U8 URLs found. The JavaScript may need to be executed in a browser."
    )
    return []


# Test with your code
if __name__ == "__main__":
    # Your obfuscated JavaScript code
    with open("paste.txt", "r", encoding="utf-8") as f:
        js_code = f.read()

    m3u8_links = get_m3u8_links(js_code)

    if m3u8_links:
        print("Valid M3U8 Links:")
        for i, link in enumerate(m3u8_links, 1):
            print(f"{i}. {link}")
    else:
        print("No valid M3U8 links could be extracted.")
        print("Consider using a JavaScript engine or browser automation.")
