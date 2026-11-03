#!/usr/bin/env bash
# Create a NEW public GitHub repository, then push the local Inertia source to it.
# Requires an authenticated GitHub CLI and Git. Does not overwrite an existing repo.
set -euo pipefail
cd "$(dirname "$0")"
owner="${1:-Ace-Alch}"
repo="${2:-Inertia-Control-Studio}"
full="$owner/$repo"
for tool in git gh; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Missing required tool: $tool" >&2
    exit 1
  fi
done
if ! gh auth status >/dev/null 2>&1; then
  echo 'Sign in first: gh auth login' >&2
  exit 1
fi
if gh repo view "$full" >/dev/null 2>&1; then
  echo "Repository $full already exists. Stop here to avoid overwriting it." >&2
  exit 1
fi
if [[ ! -d .git ]]; then
  git init -b main
fi
git add --all
if ! git diff --cached --quiet; then
  git commit -m "Initial release: Inertia Control Studio 4.1"
fi
if ! git rev-parse HEAD >/dev/null 2>&1; then
  echo 'No local commit exists; repository was not created.' >&2
  exit 1
fi
if git remote get-url origin >/dev/null 2>&1; then
  echo 'An origin remote already exists. Stop here to avoid using the wrong repository.' >&2
  exit 1
fi
gh repo create "$full" \
  --public \
  --description 'Offline nonlinear pendulum dynamics, controller design and optimization laboratory' \
  --source . --remote origin --push
printf '{"build_type":"workflow"}' | gh api -X POST "repos/$full/pages" --input - >/dev/null || {
  echo 'GitHub Pages could not be enabled automatically. Open Settings > Pages and select GitHub Actions.' >&2
}
gh workflow run pages.yml --repo "$full" || {
  echo 'Workflow could not be started yet. Run Publish Inertia demo in the Actions tab.' >&2
}
echo "Repository: https://github.com/$full"
echo 'Check GitHub > Actions for the published Pages URL.'
