#!/bin/bash
#=================================================
# AUTO PUSH TO GITHUB
# Script này sẽ tự động push code lên GitHub
#=================================================

echo "🚀 AUTO PUSH TO GITHUB SCRIPT"
echo "============================="
echo ""

# Kiểm tra xem đã có git chưa
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
fi

# Setup user nếu chưa có
if [ -z "$(git config user.name)" ]; then
    echo ""
    echo "📝 Please enter your information:"
    read -p "Your name: " user_name
    read -p "Your email: " user_email
    
    git config user.name "$user_name"
    git config user.email "$user_email"
fi

# Copy README
echo ""
echo "📄 Preparing README..."
cp README_GITHUB.md README.md 2>/dev/null || echo "⚠️  README_GITHUB.md not found"

# Add all files
echo ""
echo "📁 Adding files..."
git add .

# Create commit
echo ""
echo "💬 Creating commit..."
git commit -m "Complete BTL KPDL - Network Intrusion Detection System

Features:
- Machine Learning based IDS using NSL-KDD dataset  
- 4 algorithms: Decision Tree, Random Forest, Logistic Regression, Gradient Boosting
- Best accuracy: 99.85% (Histogram Gradient Boosting)
- Processing speed: 15ms per connection
- Complete Vietnamese documentation (60+ pages)
- Demo scripts for presentation
- Ready for production deployment

Dataset: NSL-KDD with 125,973 samples
Author: Duc Tam
Course: Khai phá dữ liệu" || echo "ℹ️  No changes to commit"

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "🔗 No remote repository found!"
    echo ""
    echo "Please enter your GitHub repository URL"
    echo "Format: https://github.com/USERNAME/REPOSITORY.git"
    echo ""
    echo "Example: https://github.com/ductampro/BTL_KPDL.git"
    echo ""
    read -p "GitHub URL: " github_url
    
    if [ ! -z "$github_url" ]; then
        git remote add origin "$github_url"
        echo "✅ Remote added"
    else
        echo "❌ No URL provided. Exiting..."
        exit 1
    fi
fi

# Show remote
echo ""
echo "📡 Remote repository:"
git remote -v

# Push
echo ""
echo "📤 Pushing to GitHub..."
echo ""

# Try main branch first
if git push -u origin main 2>/dev/null; then
    echo "✅ Successfully pushed to main branch!"
else
    # If main fails, try master
    echo "⚠️  Main branch failed, trying master..."
    git branch -M main 2>/dev/null
    
    if git push -u origin main 2>/dev/null; then
        echo "✅ Successfully pushed to main branch!"
    else
        # Try master branch
        if git push -u origin master 2>/dev/null; then
            echo "✅ Successfully pushed to master branch!"
        else
            echo ""
            echo "❌ Push failed! Possible reasons:"
            echo ""
            echo "1. Authentication required"
            echo "   → Use Personal Access Token instead of password"
            echo "   → Go to: GitHub Settings > Developer settings > Personal access tokens"
            echo ""
            echo "2. Repository doesn't exist"  
            echo "   → Create repository on GitHub first"
            echo ""
            echo "3. Try manual push:"
            echo "   git push -u origin main --force"
            echo ""
            exit 1
        fi
    fi
fi

echo ""
echo "🎉 SUCCESS! Your code is now on GitHub!"
echo ""
echo "📌 Next steps:"
echo "1. Check your repository at: $(git remote get-url origin | sed 's/\.git$//')"
echo "2. Add collaborators if needed"
echo "3. Create releases for versions"
echo ""
echo "✨ Well done!"