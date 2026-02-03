# Security Policy

## Reporting Security Issues

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in:
- Feed content or sources
- Validation bypasses
- Malicious feed submissions
- Any other security concern

Please report it privately:

1. **GitHub:** Open a security advisory at https://github.com/rsh3khar/worldstream-feeds/security/advisories/new
2. **Subject:** `[SECURITY] Worldstream Feeds - [Brief Description]`
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a detailed response within 7 days.

---

## Security Measures

All feeds are protected by multiple security layers:

### 1. Automated Validation
- YAML syntax validation
- URL format and accessibility checks
- Private IP blocking (SSRF protection)
- Malicious pattern detection
- Duplicate detection

### 2. Manual Review
- Human verification of all submissions
- Source legitimacy checks
- Content quality review
- Typosquatting detection

### 3. Backend Protection
- Input sanitization (XSS, injection protection)
- Feed content parsing with `defusedxml` (XXE protection)
- Request timeouts and size limits
- Runtime monitoring and health checks

### 4. Continuous Monitoring
- Feed uptime tracking
- Auto-disable failing feeds
- Suspicious activity detection
- Error rate monitoring

---

## What We Protect Against

- **Injection Attacks:** XSS, SQL injection, command injection
- **SSRF:** Server-side request forgery to internal networks
- **XXE:** XML external entity attacks
- **DoS:** Resource exhaustion, slow HTTP attacks
- **Social Engineering:** Typosquatting, impersonation
- **Data Integrity:** Feed hijacking, supply chain attacks

---

## Safe Contribution Guidelines

When submitting feeds:

✅ **Do:**
- Use official RSS feed URLs
- Verify feed is from legitimate source
- Test feed accessibility before submitting
- Report suspicious feeds you encounter

❌ **Don't:**
- Submit feeds to private IPs or localhost
- Use URL shorteners or redirects
- Submit feeds with embedded scripts
- Attempt to bypass validation

---

## Security Updates

Security updates are handled through:
- Immediate validation script updates
- Backend security patches (auto-deployed)
- Community notifications for critical issues

---

## Responsible Disclosure

We follow responsible disclosure principles:
- 90-day disclosure deadline
- Credit given to reporters (unless anonymous requested)
- Coordinated public disclosure
- Security advisories published

Thank you for helping keep Worldstream secure! 🔒
