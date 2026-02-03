# Setup Guide: Creating worldstream-feeds Repository

This guide shows how to create the public worldstream-feeds GitHub repository.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `worldstream-feeds`
3. Description: `Community-curated RSS feeds for Worldstream`
4. Visibility: **Public**
5. ✅ Add README file: **No** (we have our own)
6. ✅ Add .gitignore: **No**
7. ✅ Choose a license: **MIT License**
8. Click "Create repository"

---

## Step 2: Push Template Files

From this directory (`worldstream-feeds-template/`):

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: Community feeds structure"

# Add remote
git remote add origin git@github.com:rsh3khar/worldstream-feeds.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 3: Configure GitHub Settings

### Enable GitHub Actions
1. Go to repository Settings → Actions → General
2. Allow all actions and reusable workflows
3. Save

### Branch Protection (Optional but Recommended)
1. Go to Settings → Branches
2. Add branch protection rule for `main`:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass (select "validate")
   - ✅ Require branches to be up to date
3. Save changes

### Topics/Tags
Add repository topics:
- `rss`
- `feeds`
- `community`
- `curation`
- `news-aggregator`

---

## Step 4: Test Validation

Create a test PR to verify GitHub Actions work:

1. Create a new branch:
   ```bash
   git checkout -b test-validation
   ```

2. Make a small change to `feeds.yaml`

3. Commit and push:
   ```bash
   git add feeds.yaml
   git commit -m "Test: Validation workflow"
   git push origin test-validation
   ```

4. Create PR on GitHub

5. Verify GitHub Actions run successfully

6. Close/delete test PR

---

## Step 5: Update Backend Configuration

In `worldstream-backend/infra/community_feeds.py`, verify:

```python
GITHUB_RAW_URL = "https://raw.githubusercontent.com/rsh3khar/worldstream-feeds/main/feeds.yaml"
GITHUB_API_URL = "https://api.github.com/repos/rsh3khar/worldstream-feeds/commits"
```

---

## Step 6: First Deployment

1. **Backend:** Deploy with community feeds integration
   ```bash
   # Backend will automatically fetch feeds.yaml on startup
   # and poll hourly for updates
   ```

2. **Test endpoint:**
   ```bash
   curl https://worldstream-api.mokachika.com/api/sources
   ```

3. **Verify admin dashboard:**
   - Go to `/admin/health`
   - Check that community feeds appear in health tracking

---

## Step 7: Announce

1. Update Worldstream website with `/sources` page
2. Add link in footer: "RSS Sources"
3. Tweet/announce community contributions are open
4. Share contribution guidelines

---

## Maintenance

### Weekly
- Review and merge PRs
- Check feed health in `/admin/health`
- Remove consistently failing feeds

### Monthly
- Audit feed quality
- Update categories if needed
- Security review

---

## Troubleshooting

### Validation Fails on PR
- Check GitHub Actions logs
- Run `python scripts/validate_feeds.py` locally
- Verify feed URL is accessible

### Feeds Not Updating Backend
- Check backend logs for fetch errors
- Verify GitHub API rate limits not exceeded
- Manually trigger refresh: `POST /admin/refresh-feeds` (if implemented)

---

## Next Steps

Once repository is live:
- [ ] Create first community contribution PR (as example)
- [ ] Add "Suggest a Feed" button in frontend
- [ ] Set up GitHub issue templates
- [ ] Create Discord/community channel for discussions
- [ ] Monitor feed health and quality

---

Repository is now ready for community contributions! 🎉
