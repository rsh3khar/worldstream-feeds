# Worldstream Community Feeds

Community-curated RSS feeds for [Worldstream](https://worldstream.io) - a real-time global news stream.

## 🌍 How It Works

Worldstream uses a two-tier feed system to deliver relevant content:

### Global Feeds
- Shown to **all users worldwide**
- Examples: Reuters, BBC World, TechCrunch, Hacker News
- Serves as baseline content when regional feeds are sparse
- **Priority: Filler** (shown 15% of the time in regional streams)

### Regional Feeds
- Shown **primarily to users in that region**
- Examples: NPR (US), Times of India (India), BBC UK (UK)
- **Priority: Primary** (shown 85% of the time in regional streams)

**Example:** A user viewing the US stream sees:
- 85% US regional feeds (NPR, ESPN, Politico, etc.)
- 15% global feeds (BBC, Reuters, Guardian, etc.)

---

## 📊 Current Stats

- **Global Feeds:** ~50 feeds across 7 categories
- **Regional Feeds:** ~30 feeds across 5 regions
- **Categories:** tech, news, sports, entertainment, science, gaming, markets
- **Regions:** us, uk, india, japan, china

---

## 🤝 Contributing

We welcome high-quality RSS feed contributions! See **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed guidelines.

### Quick Start

1. **Fork this repo**
2. **Choose:** Global or Regional?
   - **Global**: Internationally relevant, English-language sources
   - **Regional**: Country-specific news, culture, or language
3. **Edit `feeds.yaml`** - add your feed under the appropriate section
4. **Submit a Pull Request**

**Example:**
```yaml
global:
  tech:
    - id: "yourblog"
      name: "Your Tech Blog"
      url: "https://yourblog.com/feed.xml"
      domain: "yourblog.com"
      description: "Weekly insights on AI and robotics"
      contributor: "your-github-username"
      added_at: "2025-02-03"
```

---

## ✅ Feed Requirements

### Must Have
- ✅ Active RSS/Atom feed (updated regularly)
- ✅ English content (or specify language)
- ✅ Reliable hosting (no frequent downtime)
- ✅ Fits a category (news, tech, sports, etc.)

### Must NOT
- ❌ Paywalled content (most articles locked)
- ❌ Adult/NSFW content
- ❌ Spam or low-quality aggregators
- ❌ Duplicate sources already in the list

---

## 🔍 Validation

All PRs are automatically validated for:
- Valid YAML syntax
- Required fields present (id, name, url, domain, description)
- No duplicate feeds
- URL accessibility
- Security checks (no private IPs, malicious patterns)

Manual review checks:
- Feed quality and relevance
- Source legitimacy
- Typosquatting/impersonation

---

## 📂 Feed Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **tech** | Technology, startups, gadgets | TechCrunch, Hacker News, Ars Technica |
| **news** | General news, current events | BBC, Reuters, Guardian |
| **sports** | Sports coverage, scores | ESPN, BBC Sport |
| **entertainment** | Movies, TV, music, culture | Variety, Rolling Stone |
| **science** | Research, discoveries | Nature, ScienceDaily |
| **gaming** | Video games, esports | IGN, GameSpot |
| **markets** | Finance, crypto, stocks | MarketWatch, CoinDesk |

---

## 🌐 Supported Regions

- **us** - United States
- **uk** - United Kingdom
- **india** - India
- **japan** - Japan
- **china** - China

Want to add a new region? Open an issue!

---

## 🔒 Security

We take security seriously. All feeds are:
- Validated for malicious patterns
- Checked against private IPs (SSRF protection)
- Sanitized for XSS and injection attacks
- Monitored for uptime and performance

See [Security Policy](https://github.com/rsh3khar/worldstream-backend/blob/main/docs/COMMUNITY_FEEDS_SECURITY.md) for details.

---

## 📝 License

Feed URLs are facts and not subject to copyright. This repository structure and documentation are MIT licensed.

---

## 🙋 Questions?

- **Bug Report:** Open an issue
- **Feature Request:** Open an issue
- **Security Issue:** See [SECURITY.md](SECURITY.md)
- **General Question:** Tag @rsh3khar in an issue

---

## 🚀 Live Site

See these feeds in action at **[worldstream.io](https://worldstream.io)**
