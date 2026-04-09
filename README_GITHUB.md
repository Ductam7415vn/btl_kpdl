# 🛡️ Network Intrusion Detection System using Machine Learning

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Giới thiệu

Đây là bài tập lớn môn **Khai phá dữ liệu** về xây dựng hệ thống phát hiện xâm nhập mạng (IDS) sử dụng Machine Learning. Dự án sử dụng bộ dữ liệu NSL-KDD và so sánh 4 thuật toán ML khác nhau.

### 🎯 Kết quả đạt được
- **Accuracy cao nhất**: 99.85% (Histogram Gradient Boosting)
- **Training time**: 1.84 giây
- **Prediction speed**: 15ms/connection

## 🚀 Quick Start

### 1. Clone repository
```bash
git clone https://github.com/yourusername/BTL_KPDL.git
cd BTL_KPDL
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Download dataset
Download NSL-KDD dataset và đặt file `KDDTrain+.txt` vào thư mục root.

### 4. Chạy experiment
```bash
python main_experiment.py
```

### 5. Demo prediction
```bash
python predict_new_sample.py
```

## 📁 Cấu trúc thư mục

```
BTL_KPDL/
├── main_experiment.py          # File chính để training
├── predict_new_sample.py       # Demo prediction
├── nsl_kdd_preprocessing.py    # Xử lý dữ liệu
├── visualization.py            # Vẽ biểu đồ
├── demo_thuyet_trinh.py       # Demo cho presentation
├── demo_visualization.py       # Demo visualization
├── BAO_CAO_BTL_KPDL.md        # Báo cáo chi tiết (60+ trang)
├── KICH_BAN_THUYET_TRINH.md   # Kịch bản thuyết trình
├── output/                     # Kết quả training
│   ├── best_model_*.pkl
│   ├── evaluation_results_*.txt
│   └── visualizations/
└── demo_scripts/              # Scripts hỗ trợ demo
```

## 📊 Kết quả thực nghiệm

| Model | Accuracy | Precision | Recall | F1-Score | Training Time |
|-------|----------|-----------|---------|----------|---------------|
| Decision Tree | 99.76% | 99.76% | 99.76% | 99.76% | 0.24s |
| Random Forest | 99.83% | 99.83% | 99.83% | 99.83% | 0.37s |
| Logistic Regression | 95.44% | 95.44% | 95.44% | 95.43% | 7.28s |
| **Gradient Boosting** | **99.85%** | **99.85%** | **99.85%** | **99.85%** | **1.84s** |

## 🎮 Demo Instructions

### Demo nhanh (không cần ML libraries)
```bash
python demo_thuyet_trinh.py
```

### Demo đầy đủ
```bash
# Terminal 1
python demo_thuyet_trinh.py

# Terminal 2  
python demo_visualization.py
```

### Emergency demo (khi mọi thứ fail)
```bash
python demo_scripts/emergency_demo.py
```

## 📚 Tài liệu

- [Báo cáo chi tiết](BAO_CAO_BTL_KPDL.md) - 60+ trang
- [Kịch bản thuyết trình](KICH_BAN_THUYET_TRINH.md)
- [Hướng dẫn demo đầy đủ](HUONG_DAN_DEMO_DAY_DU.md)

## 🔧 Yêu cầu hệ thống

- Python 3.8+
- RAM: 4GB minimum
- OS: Windows/Linux/macOS

## 📧 Liên hệ

- Tác giả: Đức Tâm
- Email: [your-email]
- Course: Khai phá dữ liệu

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NSL-KDD dataset creators
- scikit-learn community
- Thầy/cô giảng viên môn Khai phá dữ liệu

---

**Note**: Đây là project học tập, không sử dụng cho production environment.