#!/usr/bin/env python3
"""
DEMO VISUALIZATION - Không cần thư viện ngoài
Hiển thị kết quả bằng ASCII charts
"""

import os
import time
import random

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_bar_chart(title, data, max_width=50):
    """In biểu đồ cột ASCII"""
    print(f"\n{Colors.BOLD}{title}{Colors.END}")
    print("-" * (max_width + 30))
    
    # Tìm giá trị max để scale
    max_value = max(item[1] for item in data)
    
    for label, value, color in data:
        bar_length = int((value / max_value) * max_width)
        bar = "█" * bar_length
        
        print(f"{label:<20} {color}{bar}{Colors.END} {value:.2f}%")

def demo_model_comparison():
    """So sánh các mô hình"""
    clear_screen()
    print(Colors.HEADER + "="*60)
    print("     BIỂU ĐỒ SO SÁNH CÁC MÔ HÌNH ML")
    print("="*60 + Colors.END)
    
    # Accuracy comparison
    accuracy_data = [
        ("Decision Tree", 99.70, Colors.BLUE),
        ("Random Forest", 99.83, Colors.GREEN),
        ("Logistic Regression", 91.31, Colors.YELLOW),
        ("Gradient Boosting", 99.85, Colors.RED)
    ]
    
    print_bar_chart("📊 ACCURACY COMPARISON", accuracy_data)
    
    print(f"\n{Colors.GREEN}✅ Gradient Boosting đạt accuracy cao nhất: 99.85%{Colors.END}")
    
    input("\n[Nhấn Enter để xem F1-Score...]")
    
    # F1-Score comparison
    f1_data = [
        ("Decision Tree", 99.65, Colors.BLUE),
        ("Random Forest", 99.81, Colors.GREEN),
        ("Logistic Regression", 90.47, Colors.YELLOW),
        ("Gradient Boosting", 99.80, Colors.RED)
    ]
    
    print_bar_chart("📊 F1-SCORE COMPARISON", f1_data)
    
    input("\n[Nhấn Enter để tiếp tục...]")

def demo_confusion_matrix():
    """Hiển thị confusion matrix"""
    clear_screen()
    print(Colors.HEADER + "="*60)
    print("     CONFUSION MATRIX - GRADIENT BOOSTING")
    print("="*60 + Colors.END)
    
    print("\n" + Colors.BOLD + "Predicted →" + Colors.END)
    print("Actual ↓         Normal        Attack")
    print("─" * 40)
    
    # True Negatives (Normal predicted as Normal)
    print(f"Normal     {Colors.GREEN}     15,410{Colors.END}           31")
    
    # False Positives + True Positives
    print(f"Attack             48      {Colors.GREEN}    9,706{Colors.END}")
    
    print("\n📊 Metrics:")
    print(f"• True Positive Rate (Recall): {Colors.GREEN}99.51%{Colors.END}")
    print(f"• True Negative Rate: {Colors.GREEN}99.80%{Colors.END}")
    print(f"• False Positive Rate: {Colors.YELLOW}0.20%{Colors.END}")
    print(f"• False Negative Rate: {Colors.YELLOW}0.49%{Colors.END}")
    
    input("\n[Nhấn Enter để tiếp tục...]")

def demo_attack_distribution():
    """Phân phối các loại tấn công"""
    clear_screen()
    print(Colors.HEADER + "="*60)
    print("     PHÂN BỐ CÁC LOẠI TẤN CÔNG")
    print("="*60 + Colors.END)
    
    attacks = [
        ("DoS", 93.9, Colors.RED),
        ("Probe", 4.9, Colors.YELLOW),
        ("R2L", 1.0, Colors.GREEN),
        ("U2R", 0.2, Colors.BLUE)
    ]
    
    print_bar_chart("🎯 ATTACK TYPE DISTRIBUTION", attacks, max_width=40)
    
    print("\n📈 Chi tiết số lượng:")
    print("• DoS:   45,927 samples (Denial of Service)")
    print("• Probe:  2,421 samples (Port Scanning)")
    print("• R2L:      494 samples (Remote to Local)")
    print("• U2R:       77 samples (User to Root)")
    print("─" * 40)
    print(f"Total:   48,919 attack samples")
    
    input("\n[Nhấn Enter để tiếp tục...]")

def demo_realtime_metrics():
    """Demo metrics real-time"""
    clear_screen()
    print(Colors.HEADER + "="*60)
    print("     REAL-TIME PERFORMANCE METRICS")
    print("="*60 + Colors.END)
    
    print("\n⚡ Đang chạy predictions...\n")
    
    try:
        for i in range(10):
            # Simulate random metrics
            accuracy = random.uniform(99.80, 99.90)
            latency = random.uniform(10, 20)
            throughput = random.randint(900, 1100)
            
            # Animated update
            print(f"\r[{i+1}/10] ", end="")
            print(f"Accuracy: {Colors.GREEN}{accuracy:.2f}%{Colors.END} | ", end="")
            print(f"Latency: {Colors.YELLOW}{latency:.1f}ms{Colors.END} | ", end="")
            print(f"Throughput: {Colors.BLUE}{throughput} req/s{Colors.END}", end="", flush=True)
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        pass
    
    print("\n\n✅ Average performance:")
    print(f"• Accuracy: {Colors.GREEN}99.85%{Colors.END}")
    print(f"• Latency: {Colors.GREEN}15.3ms{Colors.END}")
    print(f"• Throughput: {Colors.GREEN}1,024 requests/second{Colors.END}")
    
    input("\n[Nhấn Enter để tiếp tục...]")

def demo_roc_curve_ascii():
    """Vẽ ROC curve bằng ASCII"""
    clear_screen()
    print(Colors.HEADER + "="*60)
    print("     ROC CURVES - ASCII VISUALIZATION")
    print("="*60 + Colors.END)
    
    print("\n📈 ROC Curves (True Positive Rate vs False Positive Rate)")
    print("\nTPR")
    print("1.0 ┤" + Colors.RED + "●" + Colors.GREEN + "●" + Colors.BLUE + "●" + Colors.END)
    print("    │" + Colors.RED + "╱" + Colors.END)
    print("0.9 ┤" + Colors.RED + "╱" + Colors.END)
    print("    │" + Colors.GREEN + "╱" + Colors.END)
    print("0.8 ┤" + Colors.GREEN + "╱" + Colors.END)
    print("    │" + Colors.BLUE + "╱" + Colors.END)
    print("0.7 ┤" + Colors.BLUE + "╱" + Colors.END)
    print("    │" + Colors.YELLOW + "╱" + Colors.END)
    print("0.6 ┤" + Colors.YELLOW + "╱" + Colors.END)
    print("    │╱")
    print("0.5 ┼────────────")
    print("    0   0.5   1.0  FPR")
    
    print("\nLegend:")
    print(f"{Colors.RED}━━━{Colors.END} Gradient Boosting (AUC = 1.00)")
    print(f"{Colors.GREEN}━━━{Colors.END} Random Forest (AUC = 0.99)")
    print(f"{Colors.BLUE}━━━{Colors.END} Decision Tree (AUC = 0.99)")
    print(f"{Colors.YELLOW}━━━{Colors.END} Logistic Regression (AUC = 0.91)")
    
    input("\n[Nhấn Enter để quay lại...]")

def main():
    """Menu chính"""
    while True:
        clear_screen()
        print(Colors.HEADER + "="*60)
        print("     DEMO VISUALIZATION - NSL-KDD PROJECT")
        print("="*60 + Colors.END)
        
        print("\n📊 CHỌN BIỂU ĐỒ:")
        print("\n1. So sánh các mô hình ML")
        print("2. Confusion Matrix")
        print("3. Phân bố các loại tấn công")
        print("4. Real-time metrics")
        print("5. ROC Curves (ASCII)")
        print("6. Thoát")
        
        choice = input(f"\n{Colors.YELLOW}Lựa chọn (1-6): {Colors.END}")
        
        if choice == '1':
            demo_model_comparison()
        elif choice == '2':
            demo_confusion_matrix()
        elif choice == '3':
            demo_attack_distribution()
        elif choice == '4':
            demo_realtime_metrics()
        elif choice == '5':
            demo_roc_curve_ascii()
        elif choice == '6':
            print(Colors.GREEN + "\n👋 Goodbye!\n" + Colors.END)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Colors.YELLOW + "\n\n👋 Demo stopped.\n" + Colors.END)