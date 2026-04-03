"""
=============================================================================
MODULE TRỰC QUAN HÓA CHO DỰ ÁN NETWORK INTRUSION DETECTION
=============================================================================
Tác giả: Data Science & Security Expert
Mô tả: Module này cung cấp các hàm vẽ biểu đồ và trực quan hóa kết quả
       cho dự án phát hiện xâm nhập mạng NSL-KDD.
=============================================================================
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
import warnings

warnings.filterwarnings('ignore')

# Cấu hình style cho biểu đồ
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Cấu hình font cho tiếng Việt
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def plot_model_comparison(results, save_path=None):
    """
    Vẽ biểu đồ so sánh hiệu suất các mô hình.
    
    Parameters:
    -----------
    results : dict
        Dictionary chứa kết quả đánh giá từ train_and_evaluate
    save_path : str, optional
        Đường dẫn lưu biểu đồ
    """
    # Chuẩn bị dữ liệu
    models = list(results.keys())
    metrics_names = ['accuracy', 'precision', 'recall', 'f1_score']
    
    # Tạo DataFrame để vẽ
    data = []
    for model in models:
        for metric in metrics_names:
            data.append({
                'Model': model,
                'Metric': metric.replace('_', ' ').title(),
                'Score': results[model][metric]
            })
    
    df = pd.DataFrame(data)
    
    # Vẽ biểu đồ
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Subplot 1: Grouped Bar Chart
    df_pivot = df.pivot(index='Model', columns='Metric', values='Score')
    df_pivot.plot(kind='bar', ax=ax1)
    ax1.set_title('So sánh hiệu suất các mô hình', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Mô hình', fontsize=12)
    ax1.set_ylabel('Điểm số', fontsize=12)
    ax1.set_ylim(0.9, 1.0)
    ax1.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(axis='y', alpha=0.3)
    
    # Thêm giá trị trên các cột
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%.4f', fontsize=8)
    
    # Subplot 2: Heatmap
    pivot_table = df_pivot.T
    sns.heatmap(pivot_table, annot=True, fmt='.4f', cmap='YlGn', 
                cbar_kws={'label': 'Score'}, ax=ax2)
    ax2.set_title('Heatmap hiệu suất', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Mô hình', fontsize=12)
    ax2.set_ylabel('Metrics', fontsize=12)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Đã lưu biểu đồ so sánh tại: {save_path}")
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def plot_confusion_matrices(results, y_test, save_path=None):
    """
    Vẽ confusion matrix cho tất cả các mô hình.
    
    Parameters:
    -----------
    results : dict
        Dictionary chứa kết quả đánh giá
    y_test : array-like
        Nhãn thực tế của test set
    save_path : str, optional
        Đường dẫn lưu biểu đồ
    """
    n_models = len(results)
    n_cols = 2
    n_rows = (n_models + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 6*n_rows))
    if n_models == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for idx, (name, metrics) in enumerate(results.items()):
        cm = metrics['confusion_matrix']
        
        # Vẽ confusion matrix
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   ax=axes[idx], cbar_kws={'label': 'Count'})
        axes[idx].set_title(f'Confusion Matrix - {name}', fontsize=14, fontweight='bold')
        axes[idx].set_xlabel('Dự đoán', fontsize=12)
        axes[idx].set_ylabel('Thực tế', fontsize=12)
        axes[idx].set_xticklabels(['Normal', 'Attack'])
        axes[idx].set_yticklabels(['Normal', 'Attack'])
        
        # Thêm thông tin accuracy
        accuracy = metrics['accuracy']
        axes[idx].text(0.5, -0.15, f'Accuracy: {accuracy:.4f}', 
                      ha='center', transform=axes[idx].transAxes, fontsize=11)
    
    # Ẩn các subplot thừa
    for idx in range(n_models, len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle('Confusion Matrices của các mô hình', fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Đã lưu confusion matrices tại: {save_path}")
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def plot_roc_curves(results, X_test, y_test, save_path=None):
    """
    Vẽ ROC curves cho tất cả các mô hình.
    
    Parameters:
    -----------
    results : dict
        Dictionary chứa kết quả và model
    X_test : array-like
        Features của test set
    y_test : array-like
        Nhãn thực tế của test set
    save_path : str, optional
        Đường dẫn lưu biểu đồ
    """
    plt.figure(figsize=(10, 8))
    
    for name, metrics in results.items():
        model = metrics['model']
        
        # Kiểm tra model có hỗ trợ predict_proba không
        if hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            roc_auc = auc(fpr, tpr)
            
            plt.plot(fpr, tpr, linewidth=2, 
                    label=f'{name} (AUC = {roc_auc:.4f})')
    
    # Vẽ đường baseline
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Baseline (AUC = 0.5)')
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=14)
    plt.ylabel('True Positive Rate', fontsize=14)
    plt.title('ROC Curves - So sánh các mô hình', fontsize=16, fontweight='bold')
    plt.legend(loc="lower right", fontsize=12)
    plt.grid(alpha=0.3)
    
    fig = plt.gcf()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Đã lưu ROC curves tại: {save_path}")
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def plot_feature_importance(model, feature_names, top_n=20, save_path=None):
    """
    Vẽ biểu đồ feature importance (dành cho tree-based models).
    
    Parameters:
    -----------
    model : sklearn model
        Model đã train (phải có attribute feature_importances_)
    feature_names : list
        Danh sách tên features
    top_n : int
        Số lượng features quan trọng nhất cần hiển thị
    save_path : str, optional
        Đường dẫn lưu biểu đồ
    """
    if not hasattr(model, 'feature_importances_'):
        print("Model không hỗ trợ feature importance!")
        return
    
    # Lấy feature importance
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    # Tạo DataFrame
    df_importance = pd.DataFrame({
        'feature': [feature_names[i] for i in indices],
        'importance': importances[indices]
    })
    
    # Vẽ biểu đồ
    plt.figure(figsize=(12, 8))
    
    bars = plt.barh(df_importance['feature'], df_importance['importance'])
    
    # Tô màu gradient cho bars
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(bars)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    plt.xlabel('Importance Score', fontsize=14)
    plt.ylabel('Features', fontsize=14)
    plt.title(f'Top {top_n} Features quan trọng nhất', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Thêm giá trị trên bars
    for i, v in enumerate(df_importance['importance']):
        plt.text(v + 0.001, i, f'{v:.4f}', va='center', fontsize=10)
    
    plt.tight_layout()
    
    fig = plt.gcf()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Đã lưu feature importance tại: {save_path}")
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def plot_training_time_comparison(results, save_path=None):
    """
    So sánh thời gian huấn luyện của các mô hình.
    
    Parameters:
    -----------
    results : dict
        Dictionary chứa kết quả đánh giá
    save_path : str, optional
        Đường dẫn lưu biểu đồ
    """
    models = []
    train_times = []
    predict_times = []
    
    for name, metrics in results.items():
        models.append(name)
        train_times.append(metrics.get('train_time', metrics.get('training_time', 0.0)))
        predict_times.append(metrics.get('predict_time', metrics.get('prediction_time', 0.0)))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Thời gian training
    bars1 = ax1.bar(models, train_times, color='skyblue', edgecolor='navy', alpha=0.7)
    ax1.set_xlabel('Mô hình', fontsize=12)
    ax1.set_ylabel('Thời gian (giây)', fontsize=12)
    ax1.set_title('Thời gian huấn luyện', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Thêm giá trị trên bars
    for bar, time in zip(bars1, train_times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{time:.2f}s', ha='center', va='bottom', fontsize=10)
    
    # Thời gian prediction
    bars2 = ax2.bar(models, predict_times, color='lightcoral', edgecolor='darkred', alpha=0.7)
    ax2.set_xlabel('Mô hình', fontsize=12)
    ax2.set_ylabel('Thời gian (giây)', fontsize=12)
    ax2.set_title('Thời gian dự đoán', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Thêm giá trị trên bars
    for bar, time in zip(bars2, predict_times):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{time:.4f}s', ha='center', va='bottom', fontsize=10)
    
    plt.suptitle('So sánh thời gian xử lý', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Đã lưu biểu đồ thời gian tại: {save_path}")
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)


def create_all_visualizations(results, X_test, y_test, feature_names, 
                            best_model=None, output_dir='output/visualizations'):
    """
    Tạo tất cả các visualization và lưu vào thư mục.
    
    Parameters:
    -----------
    results : dict
        Dictionary chứa kết quả đánh giá
    X_test : array-like
        Features của test set
    y_test : array-like
        Nhãn thực tế
    feature_names : list
        Danh sách tên features
    best_model : sklearn model
        Model tốt nhất (cho feature importance)
    output_dir : str
        Thư mục lưu các biểu đồ
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*70)
    print("TẠO CÁC BIỂU ĐỒ TRỰC QUAN")
    print("="*70)
    
    # 1. So sánh hiệu suất
    print("\n[1/5] Vẽ biểu đồ so sánh hiệu suất...")
    plot_model_comparison(results, f"{output_dir}/model_comparison.png")
    
    # 2. Confusion matrices
    print("\n[2/5] Vẽ confusion matrices...")
    plot_confusion_matrices(results, y_test, f"{output_dir}/confusion_matrices.png")
    
    # 3. ROC curves
    print("\n[3/5] Vẽ ROC curves...")
    plot_roc_curves(results, X_test, y_test, f"{output_dir}/roc_curves.png")
    
    # 4. Thời gian training
    print("\n[4/5] Vẽ biểu đồ thời gian...")
    plot_training_time_comparison(results, f"{output_dir}/training_time.png")
    
    # 5. Feature importance (nếu có best model)
    if best_model:
        print("\n[5/5] Vẽ feature importance...")
        plot_feature_importance(best_model, feature_names, top_n=20, 
                              save_path=f"{output_dir}/feature_importance.png")
    
    print(f"\n✓ Hoàn tất! Tất cả biểu đồ đã được lưu tại: {output_dir}/")
    
    
if __name__ == "__main__":
    print("Module visualization đã sẵn sàng sử dụng!")
    print("Import module này trong script chính để sử dụng các hàm visualization.")
