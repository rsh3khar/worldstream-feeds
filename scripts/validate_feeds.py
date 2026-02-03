#!/usr/bin/env python3
"""Validate community feeds for security and correctness.

This script will be used in the worldstream-feeds repo for PR validation.
Copy to worldstream-feeds/scripts/validate_feeds.py
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml
    import requests
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install pyyaml requests")
    sys.exit(1)

# Import security validation from backend (copy these functions to validate script)
# For standalone use, duplicate the validation logic

# Security constants
MAX_STRING_LENGTH = {
    'id': 50,
    'name': 100,
    'domain': 100,
    'description': 500,
    'url': 2000,
    'contributor': 50,
}

ALLOWED_PATTERNS = {
    'id': r'^[a-z0-9_-]+$',
    'domain': r'^[a-z0-9.-]+$',
    'contributor': r'^[a-zA-Z0-9_-]+$',
}

BLOCKED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '::1']
PRIVATE_IP_PREFIXES = ['10.', '172.16.', '192.168.', '169.254.']


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_url_format(url: str) -> Tuple[bool, str]:
    """Validate URL format and security."""
    from urllib.parse import urlparse

    try:
        if len(url) > MAX_STRING_LENGTH['url']:
            return False, "URL too long"

        parsed = urlparse(url)

        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False, f"Invalid scheme: {parsed.scheme}"

        # Get hostname
        hostname = parsed.netloc.split(':')[0].lower()

        # Block localhost
        if hostname in BLOCKED_HOSTS:
            return False, "Localhost not allowed"

        # Check for private IPs
        for prefix in PRIVATE_IP_PREFIXES:
            if hostname.startswith(prefix):
                return False, f"Private IP not allowed: {hostname}"

        # Check for suspicious patterns
        if '..' in parsed.path or '%2e%2e' in url.lower():
            return False, "Path traversal pattern detected"

        # Check for header injection
        if any(char in url for char in ['\r', '\n']):
            return False, "Newline characters not allowed"

        return True, "OK"

    except Exception as e:
        return False, f"Parse error: {str(e)}"


def validate_url_accessible(url: str, timeout: int = 10) -> Tuple[bool, str]:
    """Check if URL is accessible."""
    try:
        resp = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={'User-Agent': 'Worldstream-FeedValidator/1.0'}
        )

        if resp.status_code == 405:  # HEAD not allowed
            resp = requests.get(
                url,
                timeout=timeout,
                stream=True,
                allow_redirects=True,
                headers={'User-Agent': 'Worldstream-FeedValidator/1.0'}
            )
            resp.close()

        if 200 <= resp.status_code < 300:
            return True, "OK"
        else:
            return False, f"HTTP {resp.status_code}"

    except requests.exceptions.Timeout:
        return False, "Request timeout"
    except requests.exceptions.TooManyRedirects:
        return False, "Too many redirects"
    except requests.exceptions.ConnectionError as e:
        return False, f"Connection error: {str(e)[:100]}"
    except Exception as e:
        return False, f"Error: {str(e)[:100]}"


def validate_string_field(value: str, field_name: str) -> List[str]:
    """Validate a string field."""
    errors = []

    # Length check
    max_len = MAX_STRING_LENGTH.get(field_name, 200)
    if len(value) > max_len:
        errors.append(f"  {field_name}: too long ({len(value)} > {max_len})")

    # Pattern check
    if field_name in ALLOWED_PATTERNS:
        if not re.match(ALLOWED_PATTERNS[field_name], value):
            errors.append(
                f"  {field_name}: invalid format (expected {ALLOWED_PATTERNS[field_name]})"
            )

    # Empty check for critical fields
    if field_name in ['id', 'name', 'url', 'domain'] and not value.strip():
        errors.append(f"  {field_name}: cannot be empty")

    # Check for suspicious characters
    if any(ord(c) < 32 for c in value if c not in '\n\t'):
        errors.append(f"  {field_name}: contains control characters")

    return errors


def validate_feed(feed: Dict, feed_number: int) -> List[str]:
    """Validate a single feed entry."""
    errors = []
    feed_name = feed.get('name', f'Feed #{feed_number}')

    # Check required fields
    required = ['id', 'name', 'url', 'domain', 'description']
    for field in required:
        if field not in feed:
            errors.append(f"  Missing required field: {field}")

    if errors:
        return errors  # Don't continue if missing fields

    # Validate string fields
    for field in ['id', 'name', 'domain', 'description', 'url', 'contributor']:
        if field in feed:
            if not isinstance(feed[field], str):
                errors.append(f"  {field}: must be a string")
            else:
                errors.extend(validate_string_field(feed[field], field))

    # Validate URL format
    valid, error = validate_url_format(feed['url'])
    if not valid:
        errors.append(f"  URL validation failed: {error}")

    # Validate domain matches URL
    from urllib.parse import urlparse
    try:
        url_domain = urlparse(feed['url']).netloc.split(':')[0].lower()
        feed_domain = feed['domain'].lower()
        if feed_domain != url_domain and not url_domain.endswith('.' + feed_domain):
            errors.append(f"  Domain mismatch: domain={feed_domain}, url_domain={url_domain}")
    except Exception as e:
        errors.append(f"  Domain validation error: {e}")

    return errors


def validate_feeds_file(filepath: str, check_accessibility: bool = True) -> int:
    """Validate feeds.yaml file.

    Returns:
        0 if valid, 1 if errors found
    """
    print(f"🔍 Validating {filepath}...")
    print()

    # Load YAML
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 1

    if not isinstance(data, dict):
        print("❌ Feeds data must be a dictionary")
        return 1

    # Check structure
    if 'global' not in data or 'regional' not in data:
        print("❌ Missing 'global' or 'regional' section")
        return 1

    errors = []
    warnings = []
    seen_ids = set()
    seen_urls = set()
    seen_domains = {}  # domain -> list of feed names
    total_feeds = 0

    # Validate global feeds
    print("📋 Validating global feeds...")
    for category, feeds in data.get('global', {}).items():
        if not isinstance(feeds, list):
            errors.append(f"Global category '{category}' must be a list")
            continue

        for i, feed in enumerate(feeds, 1):
            total_feeds += 1
            feed_errors = validate_feed(feed, i)
            if feed_errors:
                errors.append(f"Global/{category}/{feed.get('name', f'Feed {i}')}:")
                errors.extend(feed_errors)
                continue

            # Deduplication checks
            feed_id = feed['id']
            feed_url = feed['url']
            feed_domain = feed['domain']
            feed_name = feed['name']

            if feed_id in seen_ids:
                errors.append(f"Duplicate feed ID: {feed_id} ({feed_name})")
            seen_ids.add(feed_id)

            if feed_url in seen_urls:
                errors.append(f"Duplicate feed URL: {feed_url} ({feed_name})")
            seen_urls.add(feed_url)

            if feed_domain in seen_domains:
                warnings.append(
                    f"Domain {feed_domain} used by multiple feeds: "
                    f"{seen_domains[feed_domain]} and {feed_name}"
                )
            else:
                seen_domains[feed_domain] = feed_name

    # Validate regional feeds
    print("🌍 Validating regional feeds...")
    for region, categories in data.get('regional', {}).items():
        if not isinstance(categories, dict):
            errors.append(f"Regional section '{region}' must be a dictionary")
            continue

        for category, feeds in categories.items():
            if not isinstance(feeds, list):
                errors.append(f"Regional category '{region}/{category}' must be a list")
                continue

            for i, feed in enumerate(feeds, 1):
                total_feeds += 1
                feed_errors = validate_feed(feed, i)
                if feed_errors:
                    errors.append(f"Regional/{region}/{category}/{feed.get('name', f'Feed {i}')}:")
                    errors.extend(feed_errors)
                    continue

                # Deduplication checks
                feed_id = feed['id']
                feed_url = feed['url']
                feed_name = feed['name']

                if feed_id in seen_ids:
                    errors.append(f"Duplicate feed ID: {feed_id} ({feed_name})")
                seen_ids.add(feed_id)

                if feed_url in seen_urls:
                    errors.append(f"Duplicate feed URL: {feed_url} ({feed_name})")
                seen_urls.add(feed_url)

    print(f"✓ Validated {total_feeds} feeds")
    print()

    # Check URL accessibility (optional, slower)
    if check_accessibility and not errors:
        print("🌐 Checking URL accessibility (this may take a while)...")
        inaccessible = []

        all_feeds = []
        for feeds in data.get('global', {}).values():
            all_feeds.extend(feeds)
        for region_data in data.get('regional', {}).values():
            for feeds in region_data.values():
                all_feeds.extend(feeds)

        for feed in all_feeds:
            valid, error = validate_url_accessible(feed['url'])
            if not valid:
                inaccessible.append(f"  {feed['name']}: {error}")

        if inaccessible:
            warnings.append("Some URLs are not accessible:")
            warnings.extend(inaccessible)

        print(f"✓ Checked {len(all_feeds)} URLs")
        print()

    # Print results
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
        print()

    if errors:
        print("❌ VALIDATION FAILED:")
        for error in errors:
            print(f"  {error}")
        print()
        return 1
    else:
        print("✅ All validations passed!")
        print()
        return 0


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Validate community feeds')
    parser.add_argument('filepath', nargs='?', default='feeds.yaml', help='Path to feeds.yaml')
    parser.add_argument('--skip-accessibility', action='store_true', help='Skip URL accessibility checks')
    args = parser.parse_args()

    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    exit_code = validate_feeds_file(
        str(filepath),
        check_accessibility=not args.skip_accessibility
    )

    sys.exit(exit_code)
