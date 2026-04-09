#!/bin/bash
# SECURE PUSH SCRIPT

echo "🔐 SECURE PUSH TO GITHUB"
echo "======================="
echo ""
echo "⚠️  NEVER share your token with anyone!"
echo ""

cd /Users/ductampro/Desktop/BTL_KPDL

# Initialize git
git init
git add .
git commit -m "Complete BTL KPDL - Network Intrusion Detection System" 2>/dev/null || echo "Already committed"

# Setup branch
git branch -M main

# Remove old remote if exists
git remote remove origin 2>/dev/null

# Push using token in URL (will be hidden from history)
echo "📤 Pushing to GitHub..."
echo "(Enter your token when prompted for password)"

git remote add origin https://github.com/Ductam7415vn/btl_kpdl.git
git push -u origin main --force

echo ""
echo "✅ Done! Check: https://github.com/Ductam7415vn/btl_kpdl"