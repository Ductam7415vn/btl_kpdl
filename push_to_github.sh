#!/bin/bash
#=================================================
# SCRIPT PUSH CODE LÊN GITHUB
# Chạy script này để commit và push tất cả thay đổi
#=================================================

echo "🚀 Preparing to push to GitHub..."
echo "================================"

# Di chuyển vào thư mục project
cd /Users/ductampro/Desktop/BTL_KPDL

# Kiểm tra git status
echo "📊 Current git status:"
git status

# Thêm tất cả files mới
echo -e "\n📁 Adding all files..."
git add .

# Hiển thị những gì sẽ được commit
echo -e "\n📋 Files to be committed:"
git status --short

# Commit với message
echo -e "\n💬 Creating commit..."
git commit -m "Update: Complete BTL KPDL - Network Intrusion Detection System

- Added complete report (BAO_CAO_BTL_KPDL.md)
- Added presentation script (KICH_BAN_THUYET_TRINH.md)
- Added demo scripts and guides
- Added supplementary materials (20+ pages)
- Fixed accuracy metrics in documentation
- Created comprehensive demo instructions

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push lên remote
echo -e "\n📤 Pushing to GitHub..."
git push origin main

# Kiểm tra kết quả
if [ $? -eq 0 ]; then
    echo -e "\n✅ Successfully pushed to GitHub!"
    echo "🔗 Check your repository on GitHub"
else
    echo -e "\n❌ Push failed. Possible issues:"
    echo "1. No remote repository set up"
    echo "2. Authentication needed"
    echo "3. Network connection issues"
    echo ""
    echo "To fix:"
    echo "1. Set up remote: git remote add origin YOUR_GITHUB_URL"
    echo "2. Configure credentials: git config --global user.name 'Your Name'"
    echo "3. Try: git push -u origin main"
fi

echo -e "\n📊 Final status:"
git status

echo -e "\n✨ Done!"