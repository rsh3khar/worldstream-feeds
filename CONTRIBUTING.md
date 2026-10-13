# Contributing to Worldstream Community Feeds

Thank you for considering contributing! This document provides guidelines for adding RSS feeds to Worldstream.

---

## 📋 Table of Contents

- [Should My Feed Be Global or Regional?](#should-my-feed-be-global-or-regional)
- [Feed Requirements](#feed-requirements)
- [How to Add a Feed](#how-to-add-a-feed)
- [Field Descriptions](#field-descriptions)
- [Validation](#validation)
- [Review Process](#review-process)
- [Troubleshooting](#troubleshooting)

---

## Should My Feed Be Global or Regional?

### Global Feeds

**Add to `global` section if:**
- Content is internationally relevant
- English-language
- Appeals to worldwide audience
- Not tied to specific geography

**Examples:**
- ✅ TechCrunch (tech news worldwide)
- ✅ Reuters (international news)
- ✅ Nature (global scientific research)
- ✅ Hacker News (tech community)

### Regional Feeds

**Add to `regional/<region>` section if:**
- Content is country/region-specific
- Local news, culture, or sports
- Language-specific (Hindi, Japanese, etc.)
- Primarily interesting to that region

**Examples:**
- ✅ NPR → `regional/us` (US national radio)
- ✅ BBC UK → `regional/uk` (UK-specific news)
- ✅ Times of India → `regional/india`
- ✅ ESPN Cricket → `regional/india` (cricket-focused)

**Rule of Thumb:** If someone outside your country would find it interesting, it's probably global. If it's mainly for locals, it's regional.

---

## Feed Requirements

### ✅ Must Have

1. **Active RSS/Atom Feed**
   - News and topic feeds: updated at least weekly
   - Blogs: a post at least monthly
   - Valid XML format
   - Reliable hosting

2. **English Content** (or specify language)
   - Primarily English-language
   - Non-English feeds go under the matching `regional/<region>` section and should be established
     outlets in that region's language; give the publication name in English with the original in
     brackets, for example `Sankei Shimbun (産経新聞)`

3. **Quality Source**
   - Reputable publisher
   - Original content (not pure aggregator)
   - Consistent quality

4. **Category Fit**
   - Clearly fits: tech, news, sports, entertainment, science, gaming, markets, or blogs
   - Blogs are individually written personal or engineering blogs, not company marketing
   - Not miscellaneous/random

### ❌ Must NOT Have

1. **Paywalled Content**
   - Most articles shouldn't be paywalled
   - Some paywalled articles OK (e.g., NYT)
   - Fully paywalled → reject

2. **Adult/NSFW Content**
   - No explicit content
   - Family-friendly only

3. **Spam/Low Quality**
   - No clickbait farms
   - No auto-generated content: sources whose output is mainly produced by AI or other
     automation are not accepted, whatever review process is described
   - No pure aggregators or rewrites of other outlets' reporting (that don't add value)
   - No state-agency feeds or an organisation's own publication

4. **Duplicates**
   - Check if feed already exists
   - Different URL but same source → duplicate

---

## How to Add a Feed

### Step 1: Fork the Repository

Click "Fork" button on GitHub.

### Step 2: Edit `feeds.yaml`

Add your feed under the appropriate section:

```yaml
global:
  tech:
    - id: "yourblog"  # Unique ID (alphanumeric + dash/underscore)
      name: "Your Tech Blog"  # Display name
      url: "https://yourblog.com/feed.xml"  # Full RSS feed URL
      domain: "yourblog.com"  # Domain only (no https://)
      description: "Weekly insights on AI and robotics"  # 1-2 sentences
      contributor: "your-github-username"  # Your GitHub username
      added_at: "2025-02-03"  # Today's date (YYYY-MM-DD)
```

**For regional feeds:**
```yaml
regional:
  us:
    tech:
      - id: "valley-news"
        name: "Silicon Valley News"
        url: "https://svnews.com/rss"
        domain: "svnews.com"
        description: "Daily tech news from Silicon Valley"
        contributor: "username"
        added_at: "2025-02-03"
```

### Step 3: Test Your Feed

Before submitting:

1. **Verify URL works:**
   ```bash
   curl -I https://yourblog.com/feed.xml
   # Should return HTTP 200
   ```

2. **Check XML is valid:**
   - Open URL in browser
   - Should display XML or render as feed

3. **Validate locally** (optional):
   ```bash
   pip install pyyaml requests
   python scripts/validate_feeds.py
   ```

### Step 4: Submit Pull Request

1. Commit your changes:
   ```bash
   git add feeds.yaml
   git commit -m "Add: Your Tech Blog (tech)"
   ```

2. Push to your fork:
   ```bash
   git push origin main
   ```

3. Create Pull Request with title:
   - Format: `Add: [Feed Name] (category)`
   - Example: `Add: Silicon Valley News (tech)`

---

## Field Descriptions

### `id` (required)
- **Format:** Lowercase alphanumeric + dash/underscore
- **Example:** `"techcrunch"`, `"nyt-tech"`, `"bbc_sport"`
- **Rules:**
  - Must be unique across all feeds
  - Max 50 characters
  - No spaces or special characters

### `name` (required)
- **Format:** Display name of the feed
- **Example:** `"TechCrunch"`, `"BBC World News"`
- **Rules:**
  - Max 100 characters
  - Use official source name
  - No HTML or special formatting

### `url` (required)
- **Format:** Full RSS/Atom feed URL
- **Example:** `"https://techcrunch.com/feed/"`
- **Rules:**
  - Must start with `http://` or `https://`
  - Must be publicly accessible
  - Max 2000 characters

### `domain` (required)
- **Format:** Domain name only (no protocol)
- **Example:** `"techcrunch.com"`, `"bbc.co.uk"`
- **Rules:**
  - Must match the domain in `url`
  - Lowercase only
  - Max 100 characters

### `description` (required)
- **Format:** 1-2 sentence description
- **Example:** `"Technology news and startup coverage from Silicon Valley"`
- **Rules:**
  - Max 500 characters
  - Describe content, not source
  - No marketing language

### `contributor` (required)
- **Format:** Your GitHub username
- **Example:** `"octocat"`
- **Rules:**
  - Your GitHub username (not display name)
  - Max 50 characters

### `added_at` (required)
- **Format:** Date in YYYY-MM-DD
- **Example:** `"2025-02-03"`
- **Rules:**
  - Today's date
  - ISO 8601 format

---

## Validation

All PRs are automatically validated:

### Automated Checks ✅
- YAML syntax valid
- Required fields present
- No duplicate IDs or URLs
- Domain matches URL
- URL is accessible (HTTP 200)
- No private IPs (security)
- No malicious patterns (security)

### Manual Review ✅
- Feed quality
- Source legitimacy
- Category appropriateness
- Not spam/clickbait
- Not typosquatting

---

## Review Process

1. **Automatic Validation** (< 1 minute)
   - GitHub Actions runs validation script
   - Must pass before human review

2. **Manual Review** (1-3 days)
   - Maintainer checks feed quality
   - May request changes or suggest different category

3. **Merge**
   - PR merged to `main`
   - Feed goes live within 1 hour (automatic)

### Common Rejection Reasons

- ❌ Feed is inaccessible/dead
- ❌ Duplicate of existing feed
- ❌ Wrong category
- ❌ Low quality/spam
- ❌ Paywalled content
- ❌ Not English (in global section)

---

## Troubleshooting

### "URL not accessible" Error

**Cause:** Feed URL returns error
**Fix:**
- Check URL in browser
- Verify it's RSS/Atom (not HTML page)
- Try `curl -I <url>` to test

### "Duplicate URL" Error

**Cause:** Feed already exists
**Fix:**
- Search `feeds.yaml` for your domain
- If similar feed exists, yours may be redundant

### "Invalid domain" Error

**Cause:** Domain doesn't match URL
**Fix:**
```yaml
# ❌ Wrong
url: "https://feeds.feedburner.com/example"
domain: "example.com"

# ✅ Correct
url: "https://feeds.feedburner.com/example"
domain: "feedburner.com"
```

### "Invalid ID format" Error

**Cause:** ID has spaces or special characters
**Fix:**
```yaml
# ❌ Wrong
id: "My Blog!"

# ✅ Correct
id: "my-blog"
```

---

## Questions?

- **Not sure which category?** Ask in the PR comments
- **Regional vs global unclear?** Ask in the PR comments
- **Feed issues?** Open an issue

Thank you for contributing! 🎉
