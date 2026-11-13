#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

# 1. Auto-detect newest matching zip in ~/Downloads
LATEST_ZIP=$(ls -t "$HOME/Downloads"/digital-theology-papers*.zip 2>/dev/null | head -n 1 || true)

if [ -n "$LATEST_ZIP" ]; then
  echo "→ 偵測到更新檔：$LATEST_ZIP"
  unzip -o "$LATEST_ZIP" -d "$REPO_DIR"
fi

# 2. Rebuild papers.json and llms.txt locally (same mechanism as GitHub Actions)
if [ -f "scripts/build_index.py" ]; then
  python3 scripts/build_index.py
fi

# 3. Check for changes and push to GitHub (triggers Cloudflare Pages)
if [ -n "$(git status --porcelain)" ]; then
  MSG="${1:-Publish update: $(date '+%Y-%m-%d %H:%M')}"
  git add .
  git commit -m "$MSG"
  git push origin main
  echo "✓ 已推送至 GitHub！約 30 秒後即可在 https://papers.wordandspirit.com 查看更新。"
else
  echo "✓ 倉庫已是最新狀態，沒有需要推送的變更。"
fi
