"""
api_extract.py
==============
Reusable API data extraction toolkit.
Copy into any project. Handles the most common API patterns.

USAGE:
    from scripts.api_extract import (
        get_json, get_csv, get_paginated,
        scrape_table, scrape_links
    )

SUPPORTS:
    - Simple GET requests (JSON and CSV)
    - Authenticated requests (API keys, Bearer tokens)
    - Paginated APIs (multiple pages of results)
    - Web scraping (tables and links)
    - Rate limiting (respects API limits)
"""

import os
import time
import requests
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

load_dotenv()


# ══════════════════════════════════════════════════════════════
# 1. SIMPLE REQUESTS
# ══════════════════════════════════════════════════════════════


def get_json(
    url, params=None, headers=None, api_key=None, api_key_name="Authorization"
):
    """
    Pull JSON data from any REST API endpoint.
    Returns a pandas DataFrame.

    Example — no auth:
        df = get_json('https://api.example.com/data')

    Example — with API key in header:
        df = get_json(
            url='https://api.example.com/data',
            api_key='your_key',
            api_key_name='X-API-Key'
        )

    Example — with params:
        df = get_json(
            url='https://api.example.com/data',
            params={'country': 'MX', 'year': 2024}
        )
    """
    if headers is None:
        headers = {}

    if api_key:
        headers[api_key_name] = f"Bearer {api_key}"

    print(f"Extracting from: {url}")
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()

    # Handle different JSON structures
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        # Try common keys that hold the records
        for key in ["data", "results", "records", "items", "response"]:
            if key in data and isinstance(data[key], list):
                df = pd.DataFrame(data[key])
                break
        else:
            df = pd.DataFrame([data])
    else:
        raise ValueError(f"Unexpected JSON structure: {type(data)}")

    print(f"✅ Extracted {len(df):,} rows, {len(df.columns)} columns")
    return df


def get_csv(url, params=None, headers=None, **read_csv_kwargs):
    """
    Pull CSV data from a URL directly into a DataFrame.
    Works for direct CSV links and APIs that return CSV.

    Example:
        df = get_csv('https://example.com/data.csv')
        df = get_csv('https://example.com/data.csv', encoding='latin-1')
    """
    print(f"Extracting CSV from: {url}")
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text), **read_csv_kwargs)

    print(f"✅ Extracted {len(df):,} rows, {len(df.columns)} columns")
    return df


# ══════════════════════════════════════════════════════════════
# 2. AUTHENTICATED REQUESTS
# ══════════════════════════════════════════════════════════════


def get_with_auth(url, auth_type="bearer", params=None):
    """
    Pull data from APIs requiring authentication.
    Reads credentials from .env file automatically.

    auth_type options:
        'bearer'  → Authorization: Bearer <token>
        'api_key' → X-API-Key: <key>
        'basic'   → Basic username:password

    Required .env variables (set whichever you need):
        API_TOKEN=your_token
        API_KEY=your_key
        API_USERNAME=your_username
        API_PASSWORD=your_password

    Example:
        df = get_with_auth('https://api.example.com/data', auth_type='bearer')
    """
    headers = {}
    auth = None

    if auth_type == "bearer":
        token = os.getenv("API_TOKEN")
        if not token:
            raise ValueError("API_TOKEN not found in .env file")
        headers["Authorization"] = f"Bearer {token}"

    elif auth_type == "api_key":
        key = os.getenv("API_KEY")
        if not key:
            raise ValueError("API_KEY not found in .env file")
        headers["X-API-Key"] = key

    elif auth_type == "basic":
        username = os.getenv("API_USERNAME")
        password = os.getenv("API_PASSWORD")
        if not username or not password:
            raise ValueError("API_USERNAME or API_PASSWORD not found in .env")
        auth = (username, password)

    response = requests.get(url, headers=headers, params=params, auth=auth, timeout=30)
    response.raise_for_status()

    data = response.json()
    if isinstance(data, list):
        return pd.DataFrame(data)
    return pd.DataFrame(data.get("results", data.get("data", [data])))


# ══════════════════════════════════════════════════════════════
# 3. PAGINATED APIs
# ══════════════════════════════════════════════════════════════


def get_paginated(
    url,
    headers=None,
    params=None,
    page_param="page",
    results_key="results",
    max_pages=100,
    delay=0.5,
):
    """
    Pull ALL pages from a paginated API automatically.
    Most APIs return 100-1000 records per page — this loops
    through all pages and combines them into one DataFrame.

    params:
        page_param   → name of the page parameter ('page', 'offset', 'cursor')
        results_key  → JSON key that holds the records ('results', 'data', 'items')
        max_pages    → safety limit to prevent infinite loops
        delay        → seconds to wait between requests (respect rate limits)

    Example:
        df = get_paginated(
            url='https://api.example.com/orders',
            headers={'Authorization': 'Bearer your_token'},
            params={'per_page': 100},
            results_key='orders'
        )
    """
    if params is None:
        params = {}
    if headers is None:
        headers = {}

    all_records = []
    page = 1

    print(f"Pulling paginated data from: {url}")

    while page <= max_pages:
        params[page_param] = page
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        records = data.get(results_key, [])

        if not records:
            print(f"No more records at page {page} — done")
            break

        all_records.extend(records)
        print(
            f"  Page {page}: {len(records)} records "
            f"(total so far: {len(all_records):,})"
        )

        # Stop if fewer records than expected (last page)
        expected = params.get("per_page", params.get("limit", 100))
        if len(records) < expected:
            break

        page += 1
        time.sleep(delay)  # respect rate limits

    df = pd.DataFrame(all_records)
    print(f"✅ Total extracted: {len(df):,} rows")
    return df


# ══════════════════════════════════════════════════════════════
# 4. WEB SCRAPING
# ══════════════════════════════════════════════════════════════


def scrape_table(url, table_index=0, headers=None):
    """
    Scrape an HTML table from a webpage into a DataFrame.
    Use when data is in a table on a website.

    table_index: which table on the page (0 = first, 1 = second...)

    Example:
        df = scrape_table('https://example.com/stats')
        df = scrape_table('https://example.com/stats', table_index=1)
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise ImportError("Run: pip install beautifulsoup4 lxml")

    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0"}

    print(f"Scraping table from: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    # Try pandas read_html first (fastest)
    try:
        tables = pd.read_html(response.text)
        df = tables[table_index]
        print(f"✅ Scraped table with {len(df):,} rows, {len(df.columns)} columns")
        return df
    except Exception:
        pass

    # Fall back to BeautifulSoup
    soup = BeautifulSoup(response.text, "lxml")
    tables = soup.find_all("table")

    if not tables:
        raise ValueError(f"No tables found on {url}")

    table = tables[table_index]
    rows = []
    headers_row = [th.get_text(strip=True) for th in table.find_all("th")]

    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            rows.append(cells)

    df = pd.DataFrame(rows, columns=headers_row if headers_row else None)
    print(f"✅ Scraped {len(df):,} rows")
    return df


def scrape_links(url, pattern=None, headers=None):
    """
    Scrape all links from a webpage.
    Optionally filter by URL pattern.

    Example — get all links:
        links = scrape_links('https://example.com')

    Example — get only PDF links:
        links = scrape_links('https://example.com', pattern='.pdf')

    Example — get only links containing 'data':
        links = scrape_links('https://example.com', pattern='data')
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise ImportError("Run: pip install beautifulsoup4 lxml")

    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, "lxml")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if pattern is None or pattern in href:
            links.append({"text": text, "url": href})

    df = pd.DataFrame(links)
    print(f"✅ Found {len(df):,} links")
    return df


def scrape_text(url, tag="p", css_class=None, headers=None):
    """
    Scrape text content from a webpage.
    Use for articles, descriptions, or any text content.

    Example — scrape all paragraphs:
        text = scrape_text('https://example.com/article')

    Example — scrape specific class:
        text = scrape_text('https://example.com', tag='div', css_class='content')
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise ImportError("Run: pip install beautifulsoup4 lxml")

    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=30)
    soup = BeautifulSoup(response.text, "lxml")

    elements = soup.find_all(tag, class_=css_class)
    text_list = [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]

    print(f"✅ Scraped {len(text_list)} text elements")
    return text_list


# ══════════════════════════════════════════════════════════════
# 5. RESPONSE VALIDATION
# ══════════════════════════════════════════════════════════════


def check_response(response):
    """
    Check API response status and print helpful error messages.

    Status codes:
        200 → Success
        400 → Bad request (check your params)
        401 → Unauthorized (check your API key)
        403 → Forbidden (no permission)
        404 → Not found (check your URL)
        429 → Rate limited (too many requests)
        500 → Server error (API is down)
    """
    status_messages = {
        200: "✅ Success",
        400: "❌ Bad request — check your parameters",
        401: "❌ Unauthorized — check your API key",
        403: "❌ Forbidden — you don't have permission",
        404: "❌ Not found — check your URL",
        429: "❌ Rate limited — too many requests, add a delay",
        500: "❌ Server error — the API is having issues",
    }

    status = response.status_code
    message = status_messages.get(status, f"Status code: {status}")
    print(f"Response: {message}")
    return status == 200


# ══════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ══════════════════════════════════════════════════════════════
"""
SITUATION                              FUNCTION
────────────────────────────────────────────────────────────
Pull JSON from a public API            get_json(url)
Pull CSV from a URL                    get_csv(url)
Pull from API requiring login          get_with_auth(url)
Pull all pages from paginated API      get_paginated(url)
Scrape a table from a website          scrape_table(url)
Get all links from a webpage           scrape_links(url)
Get text content from a webpage        scrape_text(url)
 
AUTHENTICATION TYPES
────────────────────────────────────────────────────────────
No auth needed                         get_json(url)
API key in header                      get_json(url, api_key='key')
Bearer token                           get_with_auth(url, 'bearer')
Basic username/password                get_with_auth(url, 'basic')
 
COMMON API RESPONSE STRUCTURES
────────────────────────────────────────────────────────────
{'results': [...]}                     get_json handles automatically
{'data': [...]}                        get_json handles automatically
{'items': [...]}                       get_json handles automatically
[{...}, {...}]  (list at root)         get_json handles automatically
"""
