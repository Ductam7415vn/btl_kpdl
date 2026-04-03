# Network Intrusion Detection System using Machine Learning

## 📋 Giới thiệu

Dự án này xây dựng một hệ thống phát hiện xâm nhập mạng (Network Intrusion Detection System - NIDS) sử dụng Machine Learning với bộ dữ liệu NSL-KDD. Hệ thống có khả năng phân loại lưu lượng mạng thành hai nhóm: **Normal** (bình thường) và **Attack** (tấn công).

### 🎯 Mục tiêu
- Phát hiện các hoạt động bất thường trong lưu lượng mạng
- Đạt độ chính xác cao trong việc phân loại
- Cung cấp công cụ dự đoán cho các mẫu mới
- Trực quan hóa kết quả một cách trực quan

### 📊 Kết quả đạt được
- **Độ chính xác tốt nhất**: 99.85% (Histogram Gradient Boosting)
- **F1-Score**: 0.9985
- **ROC-AUC**: 1.0000

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- macOS (tối ưu cho Apple Silicon M1/M2/M3) hoặc Linux/Windows
- RAM: 8GB+ được khuyến nghị

### Cài đặt dependencies

```bash
# Clone repository
git clone <repository-url>
cd BTL_KPDL

# Tạo môi trường ảo (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### File requirements.txt
```
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
joblib>=1.0.0
```

## 📁 Cấu trúc Project

```
BTL_KPDL/
│
├── KDDTrain+.txt              # Dữ liệu training NSL-KDD
├── nsl_kdd_preprocessing.py   # Script chính xử lý và training
├── visualization.py           # Module trực quan hóa
├── predict_new_sample.py      # Module dự đoán mẫu mới
├── README.md                  # Documentation
│
└── output/                    # Thư mục output (tự động tạo)
    ├── best_model_*.pkl       # Model đã train
    ├── transformers_*.pkl     # Scaler và encoders
    ├── processed_data_*.csv   # Dữ liệu đã xử lý
    ├── evaluation_results_*.txt # Kết quả đánh giá
    └── visualizations/        # Các biểu đồ
```

## 🔧 Sử dụng

### 1. Training Model

Chạy script chính để tiền xử lý dữ liệu và huấn luyện model:

```bash
python nsl_kdd_preprocessing.py
```

Script sẽ tự động:
- Load và làm sạch dữ liệu
- Encoding các features categorical
- Chuẩn hóa dữ liệu
- Huấn luyện 4 mô hình ML
- Thực hiện cross-validation
- Lưu model tốt nhất và kết quả
- Tạo các biểu đồ trực quan

### 2. Dự đoán mẫu mới

```python
from predict_new_sample import NetworkIntrusionPredictor

# Load predictor
predictor = NetworkIntrusionPredictor(
    model_path='output/best_model_*.pkl',
    transformers_path='output/transformers_*.pkl'
)

# Dự đoán một mẫu
sample = {
    'duration': 0,
    'protocol_type': 'tcp',
    'service': 'http',
    # ... (41 features)
}

result = predictor.predict(sample)
print(f"Dự đoán: {result['label']}")
print(f"Độ tin cậy: {result['confidence']}")
```

### 3. Chạy demo

```bash
python predict_new_sample.py
```

## 📊 Chi tiết về dữ liệu

### NSL-KDD Dataset
- **Tổng số mẫu**: 125,973
- **Số features**: 41
- **Phân phối**:
  - Normal: 67,343 (53.46%)
  - Attack: 58,630 (46.54%)

### 4 nhóm features chính:
1. **Basic Features (1-9)**: Đặc trưng cơ bản của kết nối TCP
2. **Content Features (10-22)**: Đặc trưng nội dung
3. **Time-based Features (23-31)**: Đặc trưng theo thời gian
4. **Host-based Features (32-41)**: Đặc trưng theo host

## 🤖 Các mô hình sử dụng

1. **Decision Tree**
   - Accuracy: 99.76%
   - Ưu điểm: Nhanh, dễ giải thích

2. **Random Forest**
   - Accuracy: 99.83%
   - Ưu điểm: Ổn định, ít overfitting

3. **Logistic Regression**
   - Accuracy: 95.44%
   - Ưu điểm: Đơn giản, nhanh

4. **Histogram Gradient Boosting** ⭐ (Tốt nhất)
   - Accuracy: 99.85%
   - Ưu điểm: Hiệu suất cao, xử lý tốt dữ liệu lớn

## 📈 Kết quả Cross-Validation

Cross-validation được thực hiện với 5-fold để đánh giá độ ổn định của model:
- Đảm bảo model không bị overfitting
- Đánh giá hiệu suất trên nhiều tập dữ liệu con
- Kết quả ổn định qua các fold

## 🎨 Trực quan hóa

Module visualization tạo ra các biểu đồ:
- So sánh hiệu suất các model
- Confusion matrices
- ROC curves
- Feature importance
- Thời gian training

## ⚙️ Tùy chỉnh

### Thay đổi tham số trong `nsl_kdd_preprocessing.py`:

```python
# Phương pháp encoding
ENCODING_METHOD = 'label'  # hoặc 'onehot'

# Phương pháp chuẩn hóa
SCALING_METHOD = 'standard'  # hoặc 'minmax'

# Chế độ model
ML_MODEL_MODE = 'fast'  # hoặc 'full'

# Tỷ lệ dữ liệu cho ML
ML_SAMPLE_FRACTION = 0.6  # 1.0 để dùng toàn bộ
```

## 🔍 Troubleshooting

### Lỗi memory
- Giảm `ML_SAMPLE_FRACTION` xuống 0.3-0.5
- Sử dụng mode 'fast' thay vì 'full'

### Lỗi import module
- Đảm bảo tất cả file .py trong cùng thư mục
- Kiểm tra đã cài đủ dependencies

### Warning trên macOS
- Script đã được tối ưu cho Apple Silicon
- Các warning về multiprocessing đã được xử lý

## 👥 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📝 License

Project này được phát triển cho mục đích học tập và nghiên cứu.

## 🙏 Acknowledgments

- Dataset: NSL-KDD từ Canadian Institute for Cybersecurity
- Scikit-learn team cho các thuật toán ML
- Matplotlib/Seaborn cho visualization tools

---
**Lưu ý**: Project này chỉ dành cho mục đích học tập. Không sử dụng cho các hoạt động bất hợp pháp.