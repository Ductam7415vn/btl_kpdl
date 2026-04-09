# 📤 HƯỚNG DẪN PUSH CODE LÊN GITHUB

## Bước 1: Tạo repository trên GitHub

1. Vào https://github.com
2. Click nút **"New"** hoặc **"+"** → **"New repository"**
3. Đặt tên: `BTL_KPDL` hoặc `Network-Intrusion-Detection`
4. Description: "Network Intrusion Detection System using Machine Learning"
5. Chọn **Public** (hoặc Private nếu muốn)
6. **KHÔNG** chọn "Initialize with README"
7. Click **"Create repository"**

## Bước 2: Setup git local

Mở Terminal và chạy:

```bash
cd /Users/ductampro/Desktop/BTL_KPDL

# Nếu chưa có git
git init

# Config user info (thay bằng info của bạn)
git config user.name "Duc Tam"
git config user.email "your-email@example.com"

# Thêm remote (thay YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/BTL_KPDL.git
```

## Bước 3: Chuẩn bị files

```bash
# Copy README cho GitHub
cp README_GITHUB.md README.md

# Xem những file sẽ được push
git status

# Thêm tất cả files
git add .

# Hoặc thêm từng file cụ thể
git add *.py
git add *.md
git add requirements.txt
git add -r output/
git add -r demo_scripts/
```

## Bước 4: Commit và Push

### Option 1: Dùng script có sẵn
```bash
chmod +x push_to_github.sh
./push_to_github.sh
```

### Option 2: Manual commands
```bash
# Commit
git commit -m "Complete BTL KPDL - Network Intrusion Detection System

- Machine Learning based IDS using NSL-KDD dataset
- 4 algorithms comparison: DT, RF, LR, GB
- Best accuracy: 99.85% (Gradient Boosting)
- Complete documentation and demo scripts"

# Push
git push -u origin main

# Nếu lỗi "main" branch, thử:
git push -u origin master
```

## Bước 5: Xử lý lỗi thường gặp

### Lỗi 1: Authentication failed
```bash
# Dùng Personal Access Token
# 1. Vào GitHub Settings → Developer settings → Personal access tokens
# 2. Generate new token với quyền "repo"
# 3. Copy token
# 4. Khi push, dùng token thay password

# Hoặc dùng SSH
git remote set-url origin git@github.com:YOUR_USERNAME/BTL_KPDL.git
```

### Lỗi 2: Large files
```bash
# Nếu có file > 100MB
git rm --cached large_file.pkl
echo "large_file.pkl" >> .gitignore
git add .gitignore
git commit -m "Remove large file"
```

### Lỗi 3: Permission denied
```bash
# Trên macOS
chmod -R 755 .
chmod +x *.sh
```

## Bước 6: Verify trên GitHub

1. Vào https://github.com/YOUR_USERNAME/BTL_KPDL
2. Check xem tất cả files đã lên chưa
3. Click vào README.md xem hiển thị đúng không

## 📝 Quick Commands (Copy & Paste)

```bash
# One-liner setup và push (thay YOUR_USERNAME)
cd /Users/ductampro/Desktop/BTL_KPDL && \
git init && \
git add . && \
git commit -m "Initial commit: Complete BTL KPDL Project" && \
git branch -M main && \
git remote add origin https://github.com/YOUR_USERNAME/BTL_KPDL.git && \
git push -u origin main
```

## 🎯 Final Checklist

- [ ] Created GitHub repository
- [ ] Configured git username/email
- [ ] Added all files
- [ ] Created meaningful commit message
- [ ] Successfully pushed to GitHub
- [ ] Verified on github.com

## 💡 Tips

1. **Commit thường xuyên**: Đừng đợi đến cuối mới commit
2. **Meaningful messages**: Viết commit message rõ ràng
3. **Use .gitignore**: Tránh push files không cần thiết
4. **Keep it organized**: Maintain cấu trúc thư mục clean

Good luck! 🚀