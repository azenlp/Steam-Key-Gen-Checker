#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/azenlp/Steam-Key-Gen-Checker"

echo "=== Ajout des fichiers ==="
git add .

echo "=== Commit ==="
read -p "Message de commit : " msg
git commit -m "$msg"

echo "=== Push vers GitHub ==="
if ! git remote get-url origin &>/dev/null; then
    git remote add origin "$REPO_URL"
fi
git push -u origin main

echo "✅ Fait !"
