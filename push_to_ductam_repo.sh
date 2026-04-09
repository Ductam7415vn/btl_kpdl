#!/bin/bash
#=================================================
# PUSH TO DUCTAM7415VN REPO
# Specific script for your repository
#=================================================

echo "🚀 PUSHING TO YOUR GITHUB REPOSITORY"
echo "===================================="
echo "Repository: https://github.com/Ductam7415vn/btl_kpdl.git"
echo ""

# Initialize git if needed
if [ ! -d .git ]; then
    echo "📦 Initializing git..."
    git init
fi

# Configure user
echo "⚙️  Configuring git user..."
git config user.name "Ductam7415vn"
git config user.email "ductam@email.com"

# Prepare README
echo "📄 Preparing README..."
cp README_GITHUB.md README.md 2>/dev/null || echo "Using existing README"

# Add all files
echo "📁 Adding all files..."
git add -A

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git status --short

# Create commit
echo ""
echo "💬 Creating commit..."
git commit -m "Complete BTL KPDL - Hệ thống phát hiện xâm nhập mạng

🎯 Features:
- Network Intrusion Detection System using Machine Learning
- Dataset: NSL-KDD (125,973 samples)
- 4 ML algorithms comparison
- Best accuracy: 99.85% (Histogram Gradient Boosting)
- Full Vietnamese documentation (60+ pages)
- Complete demo scripts for presentation

📊 Results:
- Decision Tree: 99.76%
- Random Forest: 99.83%
- Logistic Regression: 95.44%
- Gradient Boosting: 99.85%

📁 Includes:
- Source code (Python)
- Training scripts
- Prediction demo
- Visualization tools
- Presentation materials
- Detailed report

Author: Duc Tam
Course: Khai phá dữ liệu" || echo "ℹ️  Already up to date"

# Add remote if not exists
if ! git remote | grep -q origin; then
    echo ""
    echo "🔗 Adding remote repository..."
    git remote add origin https://github.com/Ductam7415vn/btl_kpdl.git
else
    echo "🔗 Remote already configured"
fi

# Create main branch
git branch -M main 2>/dev/null

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
echo "This may ask for your GitHub credentials..."
echo ""

# Force push to override any conflicts
if git push -u origin main --force; then
    echo ""
    echo "✅ SUCCESS! Code has been pushed to GitHub!"
    echo ""
    echo "🔗 View your repository at:"
    echo "   https://github.com/Ductam7415vn/btl_kpdl"
    echo ""
    echo "📊 Repository now contains:"
    echo "   - Complete source code"
    echo "   - Documentation (60+ pages)" 
    echo "   - Demo scripts"
    echo "   - Experiment results"
    echo ""
else
    echo ""
    echo "❌ Push failed! Please try these steps:"
    echo ""
    echo "1. Create a Personal Access Token:"
    echo "   - Go to: https://github.com/settings/tokens"
    echo "   - Click 'Generate new token (classic)'"
    echo "   - Select 'repo' scope"
    echo "   - Copy the token"
    echo ""
    echo "2. Run this command:"
    echo "   git push -u origin main --force"
    echo ""
    echo "3. When asked for password, paste the TOKEN (not your GitHub password)"
    echo ""
    echo "Alternative: Try with your username in the URL:"
    echo "   git remote set-url origin https://Ductam7415vn@github.com/Ductam7415vn/btl_kpdl.git"
    echo "   git push -u origin main --force"
fi