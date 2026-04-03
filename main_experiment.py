#!/usr/bin/env python3
"""
================================================================================
HỆ THỐNG PHÁT HIỆN XÂM NHẬP MẠNG SỬ DỤNG MACHINE LEARNING
================================================================================
File: main_experiment.py
Author: Đức Tâm
Created: 24/03/2026
Description: File chính để thực nghiệm và đánh giá hệ thống IDS

Đây là file triển khai hoàn chỉnh cho đồ án, bao gồm:
1. Load và tiền xử lý dữ liệu NSL-KDD
2. Huấn luyện 4 mô hình ML (Decision Tree, Random Forest, Logistic Regression, Gradient Boosting)
3. Đánh giá và so sánh hiệu năng
4. Visualization kết quả
5. Lưu mô hình tốt nhất để deployment
================================================================================
"""

import os
import sys
import argparse
import warnings
import time
import numpy as np
import pandas as pd
from datetime import datetime
import joblib

# Import các thư viện sklearn cần thiết
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve
)

# Import module tự viết
try:
    from nsl_kdd_preprocessing import NSLKDDPreprocessor
    from visualization import (
        plot_model_comparison, plot_confusion_matrices,
        plot_roc_curves, plot_feature_importance
    )
except ImportError:
    print("ERROR: Không thể import các module cần thiết.")
    print("Đảm bảo bạn có các file: nsl_kdd_preprocessing.py và visualization.py")
    sys.exit(1)

# Tắt warnings để output gọn gàng hơn
warnings.filterwarnings('ignore')

# ================================================================================
# CÁC HẰNG SỐ VÀ CẤU HÌNH
# ================================================================================

# Đường dẫn tới file dữ liệu
DATA_PATH = "KDDTrain+.txt"

# Tạo timestamp cho các file output
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Thư mục lưu kết quả
OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"✅ Đã tạo thư mục output: {OUTPUT_DIR}")

# Cấu hình cho việc huấn luyện
RANDOM_STATE = 42  # Seed để đảm bảo kết quả có thể tái lập
TEST_SIZE = 0.2   # Tỷ lệ chia train/test (80/20)
CV_FOLDS = 5      # Số fold cho cross-validation

# Cấu hình tối ưu cho Apple Silicon (M1/M2/M3)
# Giúp tránh warning và tối ưu hiệu năng
os.environ['LOKY_MAX_CPU_COUNT'] = '4'

# Sampling ratio - có thể giảm xuống nếu máy yếu
SAMPLE_FRACTION = 0.6  # Sử dụng 60% dữ liệu để train nhanh hơn
MODEL_MODE = 'standard'


def parse_arguments():
    """
    Parse command-line arguments để runtime config khớp với tài liệu thực nghiệm.
    """
    parser = argparse.ArgumentParser(
        description="Chạy thực nghiệm IDS trên bộ dữ liệu NSL-KDD."
    )
    parser.add_argument(
        '--sample-fraction',
        type=float,
        default=SAMPLE_FRACTION,
        help="Tỷ lệ dữ liệu được lấy mẫu để train/evaluate (0 < x <= 1)."
    )
    parser.add_argument(
        '--cv-folds',
        type=int,
        default=CV_FOLDS,
        help="Số fold cho cross-validation (>= 2)."
    )
    parser.add_argument(
        '--test-size',
        type=float,
        default=TEST_SIZE,
        help="Tỷ lệ tập test trong train/test split (0 < x < 1)."
    )
    parser.add_argument(
        '--random-state',
        type=int,
        default=RANDOM_STATE,
        help="Seed để tái lập kết quả."
    )
    parser.add_argument(
        '--mode',
        choices=['standard', 'fast'],
        default=MODEL_MODE,
        help="Preset cấu hình mô hình: standard cho báo cáo, fast cho máy yếu."
    )
    return parser.parse_args()


def apply_runtime_config(args):
    """
    Áp dụng cấu hình runtime từ CLI lên các hằng số toàn cục.
    """
    global SAMPLE_FRACTION, CV_FOLDS, TEST_SIZE, RANDOM_STATE, MODEL_MODE

    if not 0 < args.sample_fraction <= 1:
        raise ValueError("--sample-fraction phải nằm trong khoảng (0, 1].")
    if args.cv_folds < 2:
        raise ValueError("--cv-folds phải lớn hơn hoặc bằng 2.")
    if not 0 < args.test_size < 1:
        raise ValueError("--test-size phải nằm trong khoảng (0, 1).")

    SAMPLE_FRACTION = args.sample_fraction
    CV_FOLDS = args.cv_folds
    TEST_SIZE = args.test_size
    RANDOM_STATE = args.random_state
    MODEL_MODE = args.mode


def print_experiment_header():
    """
    In cấu hình thực nghiệm hiện tại ra terminal.
    """
    print("=" * 80)
    print("🚀 BẮT ĐẦU THỰC NGHIỆM HỆ THỐNG PHÁT HIỆN XÂM NHẬP MẠNG")
    print("=" * 80)
    print(f"📅 Timestamp: {TIMESTAMP}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"🎲 Random state: {RANDOM_STATE}")
    print(f"📊 Test size: {TEST_SIZE * 100}%")
    print(f"🔄 Cross-validation folds: {CV_FOLDS}")
    print(f"📉 Sample fraction: {SAMPLE_FRACTION * 100}%")
    print(f"⚙️  Model mode: {MODEL_MODE}")
    print("=" * 80)

# ================================================================================
# BƯỚC 1: LOAD VÀ TIỀN XỬ LÝ DỮ LIỆU
# ================================================================================

def load_and_preprocess_data():
    """
    Load và tiền xử lý dữ liệu NSL-KDD
    
    Quá trình bao gồm:
    1. Load dữ liệu từ file
    2. Xử lý missing values và duplicates
    3. Encoding categorical features
    4. Chuẩn hóa dữ liệu
    5. Chia train/test set
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test, preprocessor, feature_names)
    """
    print("\n" + "="*80)
    print("📥 BƯỚC 1: LOAD VÀ TIỀN XỬ LÝ DỮ LIỆU")
    print("="*80)
    
    # Kiểm tra file dữ liệu có tồn tại không
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"❌ Không tìm thấy file dữ liệu: {DATA_PATH}\n"
            f"Vui lòng download từ: https://www.unb.ca/cic/datasets/nsl.html"
        )
    
    print(f"✅ Tìm thấy file dữ liệu: {DATA_PATH}")
    
    # Khởi tạo preprocessor
    preprocessor = NSLKDDPreprocessor(
        encoding_method='label',     # Sử dụng Label Encoding cho categorical features
        scaling_method='standard'     # Sử dụng StandardScaler để chuẩn hóa
    )
    
    # Load dữ liệu
    print("\n📊 Loading dữ liệu...")
    start_time = time.time()
    df = preprocessor.load_data(DATA_PATH)
    print(f"✅ Load xong trong {time.time() - start_time:.2f} giây")
    print(f"📏 Kích thước dataset: {df.shape}")
    
    # Hiển thị thông tin cơ bản về dataset
    print("\n📋 Thông tin dataset:")
    print(f"- Số mẫu: {len(df):,}")
    print(f"- Số features: {df.shape[1] - 1}")  # Trừ cột label
    print(f"- Phân phối nhãn:")
    label_counts = df['label'].value_counts()
    for label, count in label_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  • {label}: {count:,} ({percentage:.2f}%)")
    
    # Clean data (xử lý missing values, duplicates)
    print("\n🧹 Cleaning data...")
    df_clean = preprocessor.clean_data(df)
    print(f"✅ Đã xóa {len(df) - len(df_clean):,} dòng duplicate")
    
    # Sampling data nếu cần (để chạy nhanh hơn)
    if SAMPLE_FRACTION < 1.0:
        print(f"\n📉 Sampling {SAMPLE_FRACTION*100}% dữ liệu để tăng tốc...")
        df_clean = df_clean.sample(
            frac=SAMPLE_FRACTION,
            random_state=RANDOM_STATE,
            stratify=df_clean['label']  # Đảm bảo tỷ lệ nhãn được giữ nguyên
        )
        print(f"✅ Kích thước sau sampling: {df_clean.shape}")
    
    # Transform labels (chuyển thành binary: normal/attack)
    print("\n🔄 Transforming labels...")
    df_clean = preprocessor.transform_labels(df_clean)
    
    # Tách features và labels
    X = df_clean.drop('label', axis=1)
    y = df_clean['label']
    
    # Lưu tên các features để sử dụng sau
    feature_names = X.columns.tolist()
    print(f"✅ Số features: {len(feature_names)}")
    
    # Encode categorical features
    print("\n🔢 Encoding categorical features...")
    X_encoded = preprocessor.encode_categorical_features(X)
    
    # Chia train/test set
    print(f"\n✂️ Chia train/test với tỷ lệ {100-TEST_SIZE*100}/{TEST_SIZE*100}...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y  # Đảm bảo tỷ lệ nhãn trong train/test giống nhau
    )
    
    print(f"✅ Train set: {X_train.shape}")
    print(f"✅ Test set: {X_test.shape}")
    
    # Chuẩn hóa dữ liệu
    print("\n📊 Normalizing features...")
    X_train_scaled, X_test_scaled = preprocessor.normalize_features(X_train, X_test)
    
    # Lưu preprocessed data
    output_file = os.path.join(OUTPUT_DIR, f"processed_data_{TIMESTAMP}.csv")
    df_processed = pd.DataFrame(X_train_scaled, columns=feature_names)
    df_processed['label'] = y_train.values
    df_processed.to_csv(output_file, index=False)
    print(f"\n💾 Đã lưu processed data: {output_file}")
    
    # Lưu transformers để sử dụng cho prediction sau này
    transformers = {
        'scaler': preprocessor.scaler,
        'label_encoders': preprocessor.label_encoders
    }
    transformers_file = os.path.join(OUTPUT_DIR, f"transformers_{TIMESTAMP}.pkl")
    joblib.dump(transformers, transformers_file)
    print(f"💾 Đã lưu transformers: {transformers_file}")
    
    print("\n✅ HOÀN THÀNH BƯỚC TIỀN XỬ LÝ DỮ LIỆU!")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, preprocessor, feature_names

# ================================================================================
# BƯỚC 2: ĐỊNH NGHĨA CÁC MÔ HÌNH
# ================================================================================

def get_models(model_mode='standard'):
    """
    Định nghĩa và cấu hình 4 mô hình ML
    
    Mỗi mô hình được điều chỉnh hyperparameters phù hợp với bài toán IDS.
    
    Returns:
        dict: Dictionary chứa các mô hình {tên: model}
    """
    print("\n" + "="*80)
    print("🤖 BƯỚC 2: KHỞI TẠO CÁC MÔ HÌNH MACHINE LEARNING")
    print("="*80)
    
    models = {}
    
    if model_mode == 'fast':
        model_configs = {
            'Decision Tree': DecisionTreeClassifier(
                max_depth=18,
                min_samples_split=10,
                min_samples_leaf=4,
                random_state=RANDOM_STATE
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=30,
                max_depth=18,
                min_samples_split=10,
                min_samples_leaf=4,
                n_jobs=-1,
                random_state=RANDOM_STATE
            ),
            'Logistic Regression': LogisticRegression(
                solver='saga',
                max_iter=250,
                n_jobs=-1,
                random_state=RANDOM_STATE
            ),
            'Hist Gradient Boosting': HistGradientBoostingClassifier(
                max_iter=60,
                max_depth=8,
                learning_rate=0.1,
                random_state=RANDOM_STATE
            )
        }
    else:
        model_configs = {
            'Decision Tree': DecisionTreeClassifier(
                max_depth=24,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=RANDOM_STATE
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=60,
                max_depth=24,
                min_samples_split=5,
                min_samples_leaf=2,
                n_jobs=-1,
                random_state=RANDOM_STATE
            ),
            'Logistic Regression': LogisticRegression(
                solver='saga',
                max_iter=400,
                n_jobs=-1,
                random_state=RANDOM_STATE
            ),
            'Hist Gradient Boosting': HistGradientBoostingClassifier(
                max_iter=100,
                max_depth=12,
                learning_rate=0.1,
                random_state=RANDOM_STATE
            )
        }

    # 1. Decision Tree
    # - max_depth=24: Cho phép cây đủ sâu để nắm bắt patterns phức tạp
    # - min_samples_split=5: Tránh overfitting với các node quá nhỏ
    print("\n1️⃣ Decision Tree Classifier")
    print("   - Ưu điểm: Dễ hiểu, không cần chuẩn hóa dữ liệu")
    print("   - Nhược điểm: Dễ overfitting, không ổn định")
    models['Decision Tree'] = model_configs['Decision Tree']
    
    # 2. Random Forest
    # - n_estimators=60: Số lượng cây trong forest (cân bằng giữa hiệu năng và tốc độ)
    # - n_jobs=-1: Sử dụng tất cả CPU cores để train song song
    print("\n2️⃣ Random Forest Classifier")
    print("   - Ưu điểm: Giảm overfitting, feature importance")
    print("   - Nhược điểm: Tốn RAM và thời gian training")
    models['Random Forest'] = model_configs['Random Forest']
    
    # 3. Logistic Regression
    # - solver='saga': Phù hợp với dataset lớn và hỗ trợ L1/L2 regularization
    # - max_iter=400: Đủ iterations để converge
    print("\n3️⃣ Logistic Regression")
    print("   - Ưu điểm: Nhanh, cung cấp xác suất")
    print("   - Nhược điểm: Giả định quan hệ tuyến tính")
    models['Logistic Regression'] = model_configs['Logistic Regression']
    
    # 4. Histogram Gradient Boosting
    # - max_iter=100: Số boosting stages
    # - learning_rate=0.1: Tốc độ học
    # Đây thường là mô hình cho kết quả tốt nhất!
    print("\n4️⃣ Histogram Gradient Boosting Classifier")
    print("   - Ưu điểm: Hiệu suất cao, xử lý missing values tốt")
    print("   - Nhược điểm: Phức tạp, khó giải thích")
    models['Hist Gradient Boosting'] = model_configs['Hist Gradient Boosting']
    
    print(f"\n✅ Đã khởi tạo {len(models)} mô hình")
    
    return models

# ================================================================================
# BƯỚC 3: TRAINING VÀ EVALUATION
# ================================================================================

def train_and_evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    """
    Train một mô hình và đánh giá hiệu năng
    
    Args:
        model: Mô hình sklearn
        X_train, X_test: Features đã chuẩn hóa
        y_train, y_test: Labels
        model_name: Tên mô hình (để hiển thị)
        
    Returns:
        dict: Kết quả đánh giá bao gồm các metrics và thời gian
    """
    print(f"\n{'='*60}")
    print(f"🎯 Training {model_name}...")
    print(f"{'='*60}")
    
    # Training
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    print(f"✅ Training hoàn thành trong {training_time:.2f} giây")
    
    # Prediction
    start_time = time.time()
    y_pred = model.predict(X_test)
    y_pred_proba = None
    
    # Lấy probability nếu model hỗ trợ (cho ROC-AUC)
    if hasattr(model, 'predict_proba'):
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    else:
        # Với một số model không có predict_proba, dùng decision_function
        if hasattr(model, 'decision_function'):
            y_pred_proba = model.decision_function(X_test)
    
    prediction_time = time.time() - start_time
    
    # Tính các metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # ROC-AUC (chỉ tính nếu có probability)
    roc_auc = None
    if y_pred_proba is not None:
        try:
            roc_auc = roc_auc_score(y_test, y_pred_proba)
        except:
            pass
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # In kết quả
    print(f"\n📊 KẾT QUẢ ĐÁNH GIÁ {model_name.upper()}:")
    print(f"   - Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   - Precision: {precision:.4f}")
    print(f"   - Recall:    {recall:.4f}")
    print(f"   - F1-Score:  {f1:.4f}")
    if roc_auc:
        print(f"   - ROC-AUC:   {roc_auc:.4f}")
    
    print(f"\n⏱️  Thời gian:")
    print(f"   - Training:   {training_time:.2f}s")
    print(f"   - Prediction: {prediction_time:.3f}s")
    
    print(f"\n📊 Confusion Matrix:")
    print(f"   TN: {cm[0][0]:,}  FP: {cm[0][1]:,}")
    print(f"   FN: {cm[1][0]:,}  TP: {cm[1][1]:,}")
    
    # Cross-validation (để kiểm tra độ ổn định)
    print(f"\n🔄 Cross-validation ({CV_FOLDS} folds)...")
    cv_scores = cross_val_score(
        model, X_train, y_train, 
        cv=CV_FOLDS, scoring='accuracy', n_jobs=-1
    )
    print(f"   - CV Mean: {cv_scores.mean():.4f}")
    print(f"   - CV Std:  {cv_scores.std():.4f}")
    
    # Tổng hợp kết quả
    results = {
        'model': model,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm,
        'training_time': training_time,
        'prediction_time': prediction_time,
        'cv_scores': cv_scores,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }
    
    return results

def train_all_models(models, X_train, X_test, y_train, y_test):
    """
    Train và đánh giá tất cả các mô hình
    
    Returns:
        dict: Kết quả của tất cả mô hình
    """
    print("\n" + "="*80)
    print("🚀 BƯỚC 3: TRAINING VÀ EVALUATION TẤT CẢ MÔ HÌNH")
    print("="*80)
    
    all_results = {}
    
    for name, model in models.items():
        results = train_and_evaluate_model(
            model, X_train, X_test, y_train, y_test, name
        )
        all_results[name] = results
    
    return all_results

# ================================================================================
# BƯỚC 4: SO SÁNH VÀ CHỌN MÔ HÌNH TỐT NHẤT
# ================================================================================

def compare_and_select_best_model(results):
    """
    So sánh các mô hình và chọn mô hình tốt nhất
    
    Args:
        results: Dictionary chứa kết quả của các mô hình
        
    Returns:
        tuple: (best_model_name, best_model_results)
    """
    print("\n" + "="*80)
    print("📊 BƯỚC 4: SO SÁNH VÀ CHỌN MÔ HÌNH TỐT NHẤT")
    print("="*80)
    
    # Tạo DataFrame để dễ so sánh
    comparison_data = []
    for name, result in results.items():
        comparison_data.append({
            'Model': name,
            'Accuracy': result['accuracy'],
            'Precision': result['precision'],
            'Recall': result['recall'],
            'F1-Score': result['f1_score'],
            'ROC-AUC': result['roc_auc'] if result['roc_auc'] else 0,
            'Training Time': result['training_time'],
            'CV Mean': result['cv_mean']
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    df_comparison = df_comparison.sort_values('Accuracy', ascending=False)
    
    print("\n📊 BẢNG SO SÁNH HIỆU NĂNG:")
    print(df_comparison.to_string(index=False, float_format='%.4f'))
    
    # Chọn model tốt nhất dựa trên accuracy
    best_model_name = df_comparison.iloc[0]['Model']
    best_accuracy = df_comparison.iloc[0]['Accuracy']
    
    print(f"\n🏆 MÔ HÌNH TỐT NHẤT: {best_model_name}")
    print(f"   - Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")
    
    # Phân tích chi tiết model tốt nhất
    best_results = results[best_model_name]
    cm = best_results['confusion_matrix']
    
    print(f"\n📊 PHÂN TÍCH CHI TIẾT {best_model_name.upper()}:")
    print(f"   - True Negatives:  {cm[0][0]:,} (Normal đúng)")
    print(f"   - False Positives: {cm[0][1]:,} (Báo nhầm Attack)")
    print(f"   - False Negatives: {cm[1][0]:,} (Bỏ sót Attack)")
    print(f"   - True Positives:  {cm[1][1]:,} (Attack đúng)")
    
    # Tính False Positive Rate và False Negative Rate
    fpr = cm[0][1] / (cm[0][0] + cm[0][1])  # FP / (TN + FP)
    fnr = cm[1][0] / (cm[1][0] + cm[1][1])  # FN / (FN + TP)
    
    print(f"\n📈 CÁC CHỈ SỐ QUAN TRỌNG:")
    print(f"   - False Positive Rate: {fpr:.4f} ({fpr*100:.2f}%)")
    print(f"   - False Negative Rate: {fnr:.4f} ({fnr*100:.2f}%)")
    
    return best_model_name, best_results

# ================================================================================
# BƯỚC 5: VISUALIZATION
# ================================================================================

def visualize_results(results, X_test, y_test, feature_names):
    """
    Tạo các biểu đồ visualization
    """
    print("\n" + "="*80)
    print("📊 BƯỚC 5: VISUALIZATION KẾT QUẢ")
    print("="*80)
    
    viz_dir = os.path.join(OUTPUT_DIR, "visualizations")
    if not os.path.exists(viz_dir):
        os.makedirs(viz_dir)
        print(f"✅ Đã tạo thư mục visualizations: {viz_dir}")
    
    try:
        # 1. So sánh hiệu năng các mô hình
        print("\n📊 Vẽ biểu đồ so sánh hiệu năng...")
        comparison_path = os.path.join(viz_dir, "model_comparison.png")
        plot_model_comparison(results, save_path=comparison_path)
        print(f"✅ Đã lưu: {comparison_path}")
        
        # 2. Confusion Matrices
        print("\n📊 Vẽ confusion matrices...")
        confusion_path = os.path.join(viz_dir, "confusion_matrices.png")
        plot_confusion_matrices(results, y_test, save_path=confusion_path)
        print(f"✅ Đã lưu: {confusion_path}")
        
        # 3. ROC Curves
        print("\n📊 Vẽ ROC curves...")
        roc_path = os.path.join(viz_dir, "roc_curves.png")
        plot_roc_curves(results, X_test, y_test, save_path=roc_path)
        print(f"✅ Đã lưu: {roc_path}")
        
        # 4. Feature Importance (chỉ cho tree-based models)
        print("\n📊 Vẽ feature importance...")
        for name, result in results.items():
            model = result['model']
            if hasattr(model, 'feature_importances_'):
                feature_file = f"feature_importance_{name.lower().replace(' ', '_')}.png"
                feature_path = os.path.join(viz_dir, feature_file)
                plot_feature_importance(
                    model,
                    feature_names,
                    save_path=feature_path
                )
                print(f"✅ Đã lưu: {feature_path}")
        
        print(f"\n✅ Tất cả visualizations đã được lưu trong: {viz_dir}")
        
    except Exception as e:
        print(f"⚠️  Lỗi khi tạo visualization: {str(e)}")
        print("Có thể do thiếu thư viện matplotlib. Chạy: pip install matplotlib seaborn")

# ================================================================================
# BƯỚC 6: LƯU MÔ HÌNH VÀ KẾT QUẢ
# ================================================================================

def save_model_and_results(best_model_name, best_results, all_results):
    """
    Lưu mô hình tốt nhất và kết quả đánh giá
    """
    print("\n" + "="*80)
    print("💾 BƯỚC 6: LƯU MÔ HÌNH VÀ KẾT QUẢ")
    print("="*80)
    
    # 1. Lưu mô hình tốt nhất
    best_model = best_results['model']
    model_file = os.path.join(OUTPUT_DIR, f"best_model_{TIMESTAMP}.pkl")
    joblib.dump(best_model, model_file)
    print(f"✅ Đã lưu mô hình tốt nhất ({best_model_name}): {model_file}")
    
    # 2. Lưu kết quả evaluation dạng text
    results_file = os.path.join(OUTPUT_DIR, f"evaluation_results_{TIMESTAMP}.txt")
    with open(results_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("KẾT QUẢ ĐÁNH GIÁ HỆ THỐNG PHÁT HIỆN XÂM NHẬP MẠNG\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Timestamp: {TIMESTAMP}\n")
        f.write(f"Best Model: {best_model_name}\n\n")
        
        # Kết quả chi tiết từng mô hình
        for name, result in all_results.items():
            f.write(f"\n{'='*60}\n")
            f.write(f"MODEL: {name}\n")
            f.write(f"{'='*60}\n")
            f.write(f"Accuracy:  {result['accuracy']:.4f}\n")
            f.write(f"Precision: {result['precision']:.4f}\n")
            f.write(f"Recall:    {result['recall']:.4f}\n")
            f.write(f"F1-Score:  {result['f1_score']:.4f}\n")
            if result['roc_auc']:
                f.write(f"ROC-AUC:   {result['roc_auc']:.4f}\n")
            f.write(f"Training Time: {result['training_time']:.2f}s\n")
            f.write(f"CV Mean: {result['cv_mean']:.4f} (±{result['cv_std']:.4f})\n")
            
            cm = result['confusion_matrix']
            f.write(f"\nConfusion Matrix:\n")
            f.write(f"TN: {cm[0][0]}  FP: {cm[0][1]}\n")
            f.write(f"FN: {cm[1][0]}  TP: {cm[1][1]}\n")
    
    print(f"✅ Đã lưu kết quả evaluation: {results_file}")
    
    # 3. Tạo báo cáo summary
    summary_file = os.path.join(OUTPUT_DIR, f"summary_{TIMESTAMP}.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("SUMMARY - HỆ THỐNG PHÁT HIỆN XÂM NHẬP MẠNG\n")
        f.write("="*50 + "\n\n")
        f.write(f"Mô hình tốt nhất: {best_model_name}\n")
        f.write(f"Độ chính xác: {best_results['accuracy']*100:.2f}%\n")
        f.write(f"Thời gian training: {best_results['training_time']:.2f}s\n")
        f.write(f"\nSử dụng model đã lưu:\n")
        f.write(f"- Model: {model_file}\n")
        f.write(f"- Transformers: transformers_{TIMESTAMP}.pkl\n")
        f.write(f"\nĐể predict sample mới, chạy:\n")
        f.write(f"python predict_new_sample.py\n")
    
    print(f"✅ Đã lưu summary: {summary_file}")

# ================================================================================
# HÀM MAIN - ĐIỀU KHIỂN TOÀN BỘ QUÁ TRÌNH
# ================================================================================

def main():
    """
    Hàm chính điều khiển toàn bộ quy trình thực nghiệm
    """
    try:
        # Ghi nhận thời gian bắt đầu
        total_start_time = time.time()
        
        # BƯỚC 1: Load và tiền xử lý dữ liệu
        X_train, X_test, y_train, y_test, preprocessor, feature_names = load_and_preprocess_data()
        
        # BƯỚC 2: Khởi tạo các mô hình
        models = get_models(model_mode=MODEL_MODE)
        
        # BƯỚC 3: Training và evaluation
        all_results = train_all_models(models, X_train, X_test, y_train, y_test)
        
        # BƯỚC 4: So sánh và chọn mô hình tốt nhất
        best_model_name, best_results = compare_and_select_best_model(all_results)
        
        # BƯỚC 5: Visualization
        visualize_results(all_results, X_test, y_test, feature_names)
        
        # BƯỚC 6: Lưu kết quả
        save_model_and_results(best_model_name, best_results, all_results)
        
        # Tổng kết
        total_time = time.time() - total_start_time
        print("\n" + "="*80)
        print("✅ HOÀN THÀNH TOÀN BỘ QUÁ TRÌNH THỰC NGHIỆM!")
        print("="*80)
        print(f"⏱️  Tổng thời gian: {total_time:.2f} giây ({total_time/60:.2f} phút)")
        print(f"🏆 Mô hình tốt nhất: {best_model_name} - Accuracy: {best_results['accuracy']*100:.2f}%")
        print(f"📁 Kết quả được lưu trong: {OUTPUT_DIR}")
        print("\n🎉 Chúc mừng bạn đã hoàn thành thực nghiệm!")
        
    except Exception as e:
        print(f"\n❌ LỖI: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# ================================================================================
# CHẠY CHƯƠNG TRÌNH
# ================================================================================

if __name__ == "__main__":
    """
    Entry point của chương trình.
    
    Để chạy:
        python main_experiment.py
        
    Yêu cầu:
        - Python 3.8+
        - Các thư viện trong requirements.txt
        - File dữ liệu KDDTrain+.txt
        - Modules: nsl_kdd_preprocessing.py, visualization.py
    """
    args = parse_arguments()
    apply_runtime_config(args)
    print_experiment_header()
    main()
