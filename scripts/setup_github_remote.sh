#!/usr/bin/env bash
set -euo pipefail

//# Create a GitHub repo (optionally via token) and set as remote for this local repo.
//# Usage: export GITHUB_USERNAME="your-username"; export GITHUB_TOKEN="your-personal-access-token"; \
//#        ./scripts/setup_github_remote.sh [repo-name] [--private|--public]
//# If GITHUB_TOKEN is not set, this will skip API creation and only set the remote using the repo-name.

REPO_NAME="${1:-$(basename "$PWD")}"
MODE="${2:---private}"
PRIVATE=true
if [[ "$MODE" == "--public" ]]; then PRIVATE=false; fi

if [[ -z "${GITHUB_USERNAME:-}" ]]; then
  echo "Error: GITHUB_USERNAME is not set. Export it: export GITHUB_USERNAME=\"your-username\""
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: This script must be run from inside a git repository."
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  echo "A remote named 'origin' already exists. Please remove it or rename it before running this script."
  echo "Existing remote: $(git remote get-url origin)"
  exit 1
fi

if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  echo "Attempting to create GitHub repository '${REPO_NAME}' under user '${GITHUB_USERNAME}' via API..."
  curl -sS -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
       -H "Accept: application/vnd.github+json" \
       -d "{\"name\":\"${REPO_NAME}\",\"private\":${PRIVATE}}" \
       "https://api.github.com/user/repos" >/tmp/gh_repo_response.json || true
  if [[ -s /tmp/gh_repo_response.json ]]; then
    if grep -q '"html_url"' /tmp/gh_repo_response.json; then
      HTML_URL=$(grep -o '"html_url":\s*"[^"]*"' /tmp/gh_repo_response.json | head -n1 | sed -E 's/.*\"([^\"]+)\".*/\1/')
      echo "GitHub repo created: ${HTML_URL}"
    else
      echo "GitHub API response did not include an HTML URL. See /tmp/gh_repo_response.json for details."
    fi
  else
    echo "GitHub API call failed or returned no content."
  fi
fi

REMOTE_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
echo "Setting remote origin to ${REMOTE_URL}"
git remote add origin "${REMOTE_URL}"
git branch -M main
git push -u origin main
