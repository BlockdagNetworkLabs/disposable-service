#!/bin/bash
set -e

echo "🚀 Starting domain update process..."

# Skip git pull in CI environment (GitHub Actions handles checkout)
if [ -z "$GITHUB_ACTIONS" ]; then
  echo "📥 Pulling latest changes..."
  git pull -q -f
fi

tmpfile=$(mktemp)

# Sync dependencies using uv
echo "📦 Installing dependencies..."
(cd disposable && uv sync --quiet)

# Run domain generation
# The Python script now preserves old domains automatically
echo "🔍 Fetching domains from sources..."
uv --project disposable run python ./disposable/.generate --dedicated-strict --source-map --dns-verify 2>$tmpfile

# Check if there are any changes
if git diff --quiet domains*.txt domains*.json 2>/dev/null; then
  echo "ℹ️  No changes detected"
  rm "$tmpfile"
  exit 0
fi

# Show what changed
echo ""
echo "📊 Changes detected:"
git diff --stat domains*.txt domains*.json | head -20

# Stage all domain files
git add domains.txt domains.json domains_legacy.txt \
    domains_mx.txt domains_mx.json \
    domains_sha1.json domains_sha1.txt \
    domains_source_map.txt \
    domains_strict.json domains_strict.txt \
    domains_strict_sha1.json domains_strict_sha1.txt \
    domains_strict_source_map.txt \
    domains_strict_mx.json domains_strict_mx.txt

# Commit with detailed message
commit_msg="Update domains

$(head -n 100 $tmpfile)"

git commit -m "$commit_msg" || {
  echo "⚠️  No changes to commit"
  rm "$tmpfile"
  exit 0
}

rm "$tmpfile"

# Push in GitHub Actions or local environment
if [ -n "$GITHUB_ACTIONS" ]; then
  echo "⬆️  Pushing changes to GitHub..."
  git push -q
  echo "✅ Successfully pushed to GitHub"
else
  echo "✅ Changes committed locally"
  echo "💡 Run 'git push' to push to remote"
fi
