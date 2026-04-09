# 🚨 PUSH CODE NGAY BÂY GIỜ - 3 BƯỚC ĐƠN GIẢN

## Bước 1: Tạo repo trên GitHub (2 phút)

1. Mở: https://github.com/new
2. Đặt tên: `BTL_KPDL`
3. **KHÔNG CHỌN** "Add README"
4. Click "Create repository"
5. **COPY LINK** hiện ra (dạng: `https://github.com/YOUR_NAME/BTL_KPDL.git`)

## Bước 2: Mở Terminal (1 phút)

**Trên macOS:**
- Nhấn `Cmd + Space`
- Gõ "Terminal"
- Enter

## Bước 3: Copy & Paste (2 phút)

Paste **TOÀN BỘ** đoạn sau vào Terminal và Enter:

```bash
cd /Users/ductampro/Desktop/BTL_KPDL && \
chmod +x auto_push.sh && \
./auto_push.sh
```

**Script sẽ hỏi bạn:**
1. Tên của bạn → Gõ tên và Enter
2. Email → Gõ email và Enter  
3. GitHub URL → Paste link từ Bước 1 và Enter

## 🎯 NẾU GẶP LỖI

### Lỗi "Authentication failed"

**Cách fix:**
1. Vào: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Chọn "repo" checkbox
4. Click "Generate token"
5. **COPY TOKEN** (chỉ hiện 1 lần!)
6. Khi Terminal hỏi password, **PASTE TOKEN** (không phải password GitHub)

### Vẫn không được?

Copy và paste từng dòng này:

```bash
cd /Users/ductampro/Desktop/BTL_KPDL
```

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "BTL KPDL Complete"
```

```bash
git remote add origin [PASTE_LINK_GITHUB_CỦA_BẠN]
```

```bash
git push -u origin main --force
```

---

## ✅ KIỂM TRA KẾT QUẢ

Vào link GitHub của bạn để xem code đã lên chưa!

**Cần giúp? Chụp màn hình lỗi!**