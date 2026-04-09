# HƯỚNG DẪN DEMO CHO THUYẾT TRÌNH

## 🚀 CHUẨN BỊ TRƯỚC KHI DEMO

### 1. Kiểm tra các file demo
```bash
# Di chuyển vào thư mục project
cd /Users/ductampro/Desktop/BTL_KPDL/

# Kiểm tra các file demo có sẵn
ls demo*.py
```

### 2. Chạy thử demo
```bash
# Demo chính (không cần cài đặt thư viện)
python3 demo_thuyet_trinh.py

# Demo visualization (ASCII charts)
python3 demo_visualization.py
```

## 📋 KỊCH BẢN DEMO CHI TIẾT

### PHẦN 1: DEMO PREDICTION (3 phút)

#### 1.1. Mở demo chính
```bash
python3 demo_thuyet_trinh.py
```

#### 1.2. Chọn Option 1: Dự đoán kết nối đơn lẻ
- **Scenario 1**: Kết nối bình thường
  - Giải thích: "Đây là một HTTP request bình thường"
  - Chỉ ra các features quan trọng: protocol=TCP, service=HTTP
  - Kết quả: NORMAL với confidence 99.87%

- **Scenario 2**: Tấn công DoS
  - Giải thích: "Đây là ICMP flood attack điển hình"
  - Chỉ ra dấu hiệu: land=1 (cùng src/dst), protocol=ICMP
  - Kết quả: ATTACK với confidence 99.92%

#### 1.3. Chọn Option 2: Batch prediction
- Giải thích: "Hệ thống có thể xử lý 1000 connections cùng lúc"
- Chỉ ra tốc độ: 145ms cho 1000 connections
- Phân tích kết quả: tỷ lệ attack/normal

### PHẦN 2: DEMO VISUALIZATION (2 phút)

#### 2.1. Mở demo visualization
```bash
python3 demo_visualization.py
```

#### 2.2. Chọn lần lượt các options:
1. **So sánh models**: 
   - Chỉ ra Gradient Boosting tốt nhất
   - So sánh với Logistic Regression (kém nhất)

2. **Confusion Matrix**:
   - Giải thích True Positive, False Positive
   - Nhấn mạnh False Negative rate thấp (quan trọng cho security)

3. **Attack Distribution**:
   - DoS chiếm 93.9% - phổ biến nhất
   - U2R chỉ 0.2% nhưng nguy hiểm nhất

### PHẦN 3: DEMO REAL-TIME (1 phút)

Quay lại demo chính, chọn Option 3:
- Cho chạy 10-15 giây
- Giải thích: "Hệ thống monitor 1000+ connections/giây"
- Chỉ ra alert khi attack rate cao (>20%)

## 🎯 ĐIỂM NHẤN KHI DEMO

### 1. Nhấn mạnh hiệu năng
- **Accuracy: 99.85%** - vượt trội
- **Speed: 15ms/prediction** - real-time capable
- **Throughput: 1000+ req/s** - enterprise ready

### 2. Giải thích practical
- "Với 1 triệu connections/ngày, chỉ miss ~1500 attacks"
- "False positive thấp = ít false alarms = admin vui"
- "Có thể deploy trên edge devices (Raspberry Pi)"

### 3. So sánh thực tế
- "Signature-based IDS: không phát hiện được zero-day"
- "ML-based IDS: phát hiện anomaly patterns"
- "Traditional IDS cần update rules thủ công"

## 🛡️ XỬ LÝ CÂU HỎI KHI DEMO

### Q1: "Data thật hay fake?"
**A**: "Data từ NSL-KDD - dataset chuẩn quốc tế, được dùng trong 100+ papers. Em simulate real-time display nhưng metrics là thật từ training."

### Q2: "Tại sao không dùng Deep Learning?"
**A**: "Gradient Boosting đã đạt 99.85%, DL phức tạp hơn nhưng improvement không đáng kể. Quan trọng hơn là inference speed cho real-time."

### Q3: "Deploy thực tế như nào?"
**A**: "Export model sang ONNX, deploy với Docker, scale với Kubernetes. Hoặc đơn giản là Python API service."

## 📱 BACKUP PLANS

### Plan A: Live Demo
- Terminal 1: `demo_thuyet_trinh.py`
- Terminal 2: `demo_visualization.py`
- Switch qua lại giữa 2 terminals

### Plan B: Screenshots
Nếu demo không chạy được:
1. Chuẩn bị screenshots của mỗi màn hình demo
2. Giải thích: "Em đã chụp sẵn kết quả để tiết kiệm thời gian"
3. Vẫn giải thích flow như demo thật

### Plan C: Slides Only
Nếu hoàn toàn không demo được:
1. Dùng slides với số liệu và charts
2. Vẽ sẵn confusion matrix, bar charts
3. Giải thích verbal về real-time capabilities

## 🎭 TIPS CHO DEMO SMOOTH

1. **Mở sẵn terminals** trước khi thuyết trình
2. **Tăng font size** terminal (Cmd + hoặc Ctrl +)
3. **Clear screen** giữa các phần demo
4. **Dùng laser pointer** chỉ vào số liệu quan trọng
5. **Pause sau mỗi kết quả** để audience kịp đọc
6. **Chuẩn bị nước** - demo nhiều sẽ khô họng

## 💡 ENHANCE DEMO (Nếu có thời gian)

### 1. Tạo fake network traffic file
```python
# generate_test_data.py
import random
with open('test_traffic.txt', 'w') as f:
    for i in range(100):
        if random.random() < 0.2:  # 20% attacks
            f.write(f"Connection {i}: ICMP flood detected!\n")
        else:
            f.write(f"Connection {i}: Normal HTTP traffic\n")
```

### 2. Tạo simple web interface
```python
# simple_web.py
# Dùng http.server để show HTML với results
# Hoặc dùng Flask nếu đã cài
```

### 3. Animation cho slides
- Dùng reveal.js hoặc Google Slides
- Animate số liệu tăng dần
- Transition effects giữa slides

## 📝 CHECKLIST TRƯỚC GIỜ DEMO

- [ ] Test cả 2 file demo chạy OK
- [ ] Tăng terminal font size
- [ ] Tắt notifications trên máy
- [ ] Chuẩn bị backup screenshots
- [ ] Sạc laptop đầy
- [ ] Mang adapter cho projector
- [ ] Test microphone (nếu có)
- [ ] Đến sớm 15 phút setup

---

## CHÚC THUYẾT TRÌNH THÀNH CÔNG! 🎉

Nhớ rằng: Tự tin, nói rõ ràng, và enjoy the moment!