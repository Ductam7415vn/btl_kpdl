#!/bin/bash
#=================================================
# SETUP GITHUB CHO PROJECT
# Chạy script này nếu chưa setup git repository
#=================================================

echo "🔧 GitHub Setup Script"
echo "====================="

# Kiểm tra xem đã có git repo chưa
if [ -d .git ]; then
    echo "✅ Git repository already initialized"
    
    # Kiểm tra remote
    if git remote -v | grep -q origin; then
        echo "✅ Remote 'origin' already exists:"
        git remote -v
    else
        echo "❌ No remote repository set"
        echo ""
        echo "Please enter your GitHub repository URL:"
        echo "Example: https://github.com/yourusername/BTL_KPDL.git"
        read -p "GitHub URL: " github_url
        
        if [ ! -z "$github_url" ]; then
            git remote add origin "$github_url"
            echo "✅ Remote added successfully"
        fi
    fi
else
    echo "📦 Initializing new git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Configure user info if needed
if [ -z "$(git config user.name)" ]; then
    echo ""
    echo "📝 Git user configuration needed"
    read -p "Enter your name: " user_name
    read -p "Enter your email: " user_email
    
    git config user.name "$user_name"
    git config user.email "$user_email"
    echo "✅ User configured"
fi

# Tạo .gitignore nếu chưa có
if [ ! -f .gitignore ]; then
    echo ""
    echo "📄 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# Jupyter Notebook
.ipynb_checkpoints

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
temp/
cache/
EOF
    echo "✅ .gitignore created"
fi

echo ""
echo "🎯 Next steps:"
echo "1. Make sure you have a GitHub repository created"
echo "2. Run: chmod +x push_to_github.sh"
echo "3. Run: ./push_to_github.sh"
echo ""
echo "Or manually:"
echo "  git add ."
echo "  git commit -m 'Initial commit'"
echo "  git push -u origin main"
echo ""
echo "✨ Setup complete!"