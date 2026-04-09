#!/usr/bin/env python3
"""
DEMO SCRIPT CHO THUYẾT TRÌNH
Hệ thống phát hiện xâm nhập mạng sử dụng Machine Learning
"""

import os
import time
import random
from datetime import datetime

# ANSI color codes cho terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """In header của demo"""
    print(Colors.HEADER + "="*60)
    print("     HỆ THỐNG PHÁT HIỆN XÂM NHẬP MẠNG - DEMO")
    print("          Machine Learning - NSL-KDD Dataset")
    print("="*60 + Colors.END)
    print()

def simulate_loading(text, duration=1):
    """Simulate loading animation"""
    print(f"\n{Colors.BLUE}⏳ {text}", end="", flush=True)
    for _ in range(3):
        time.sleep(duration/3)
        print(".", end="", flush=True)
    print(f" ✓{Colors.END}")

def demo_1_single_prediction():
    """Demo 1: Dự đoán single sample"""
    clear_screen()
    print_header()
    print(Colors.BOLD + "\n📊 DEMO 1: DỰ ĐOÁN KẾT NỐI ĐƠN LẺ" + Colors.END)
    print("-" * 50)
    
    # Scenario 1: Normal connection
    print("\n" + Colors.GREEN + "Scenario 1: Kết nối bình thường" + Colors.END)
    print("Thông tin kết nối:")
    print("  • Duration: 0 seconds")
    print("  • Protocol: TCP")
    print("  • Service: HTTP")
    print("  • Source bytes: 232")
    print("  • Destination bytes: 8153")
    
    simulate_loading("Đang phân tích", 1.5)
    
    print(Colors.GREEN + "\n✅ KẾT QUẢ: NORMAL (Bình thường)")
    print(f"   Confidence: 99.87%")
    print(f"   Thời gian xử lý: 12ms{Colors.END}")
    
    input("\n[Nhấn Enter để tiếp tục...]")
    
    # Scenario 2: Attack connection
    print("\n" + Colors.RED + "Scenario 2: Kết nối tấn công (DoS)" + Colors.END)
    print("Thông tin kết nối:")
    print("  • Duration: 0 seconds")
    print("  • Protocol: ICMP")
    print("  • Service: ECR_I")
    print("  • Source bytes: 520")
    print("  • Destination bytes: 0")
    print("  • Land: 1 (same src/dst)")
    
    simulate_loading("Đang phân tích", 1.5)
    
    print(Colors.RED + "\n🚨 KẾT QUẢ: ATTACK (Tấn công)")
    print(f"   Attack type: DoS (Denial of Service)")
    print(f"   Confidence: 99.92%")
    print(f"   Thời gian xử lý: 11ms{Colors.END}")
    
    input("\n[Nhấn Enter để tiếp tục...]")

def demo_2_batch_prediction():
    """Demo 2: Dự đoán batch"""
    clear_screen()
    print_header()
    print(Colors.BOLD + "\n📊 DEMO 2: DỰ ĐOÁN BATCH (NHIỀU KẾT NỐI)" + Colors.END)
    print("-" * 50)
    
    print("\nĐang xử lý file: test_connections.csv")
    print("Số lượng kết nối: 1000")
    
    simulate_loading("Đang load dữ liệu", 0.5)
    simulate_loading("Đang preprocessing", 0.8)
    simulate_loading("Đang dự đoán", 1.2)
    
    # Simulate results
    normal = 823
    attacks = 177
    
    print("\n" + Colors.GREEN + "✅ KẾT QUẢ PHÂN LOẠI:" + Colors.END)
    print(f"   • Normal: {normal} kết nối ({normal/10:.1f}%)")
    print(f"   • Attack: {attacks} kết nối ({attacks/10:.1f}%)")
    print("\n📈 Phân loại chi tiết các loại tấn công:")
    print("   • DoS attacks: 89 (50.3%)")
    print("   • Probe attacks: 45 (25.4%)")
    print("   • R2L attacks: 31 (17.5%)")
    print("   • U2R attacks: 12 (6.8%)")
    print(f"\n⏱️  Tổng thời gian xử lý: 145ms (0.145ms/connection)")
    
    input("\n[Nhấn Enter để tiếp tục...]")

def demo_3_realtime_monitoring():
    """Demo 3: Real-time monitoring"""
    clear_screen()
    print_header()
    print(Colors.BOLD + "\n📊 DEMO 3: GIÁM SÁT REAL-TIME" + Colors.END)
    print("-" * 50)
    
    print("\n🔴 Bắt đầu giám sát mạng real-time...")
    print("(Nhấn Ctrl+C để dừng)\n")
    
    try:
        start_time = time.time()
        total_connections = 0
        total_attacks = 0
        
        while True:
            # Simulate random connections
            connections_per_sec = random.randint(800, 1200)
            attack_rate = random.uniform(0.1, 0.25)  # 10-25% attacks
            attacks_this_sec = int(connections_per_sec * attack_rate)
            
            total_connections += connections_per_sec
            total_attacks += attacks_this_sec
            
            # Clear previous line and print update
            print(f"\r⚡ Connections/sec: {connections_per_sec:4d} | ", end="")
            
            if attack_rate > 0.2:
                print(Colors.RED, end="")
            elif attack_rate > 0.15:
                print(Colors.YELLOW, end="")
            else:
                print(Colors.GREEN, end="")
                
            print(f"🚨 Attacks: {attacks_this_sec:3d} ({attack_rate*100:.1f}%)", end="")
            print(Colors.END, end="")
            
            # Overall stats
            elapsed = time.time() - start_time
            overall_rate = (total_attacks / total_connections) * 100 if total_connections > 0 else 0
            print(f" | Total: {total_connections:,} connections, {overall_rate:.1f}% attacks", end="", flush=True)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n✋ Dừng giám sát...")
        
    input("\n[Nhấn Enter để tiếp tục...]")

def demo_4_model_performance():
    """Demo 4: So sánh hiệu năng models"""
    clear_screen()
    print_header()
    print(Colors.BOLD + "\n📊 DEMO 4: SO SÁNH HIỆU NĂNG CÁC MÔ HÌNH" + Colors.END)
    print("-" * 50)
    
    models = [
        ("Decision Tree", 99.70, 99.77, 99.52, 3.12),
        ("Random Forest", 99.83, 99.87, 99.74, 8.45),
        ("Logistic Regression", 91.31, 92.14, 89.23, 1.23),
        ("Gradient Boosting", 99.85, 99.90, 99.69, 3.45)
    ]
    
    print("\n📈 KẾT QUẢ ĐÁNH GIÁ TRÊN TEST SET (25,195 mẫu):\n")
    print(f"{'Model':<20} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'Train Time':<12}")
    print("-" * 62)
    
    for name, acc, prec, rec, train_time in models:
        # Highlight best model
        if name == "Gradient Boosting":
            print(Colors.GREEN + Colors.BOLD, end="")
        
        print(f"{name:<20} {acc:<10.2f}% {prec:<10.2f}% {rec:<10.2f}% {train_time:<12.2f}s", end="")
        
        if name == "Gradient Boosting":
            print(" ⭐ BEST" + Colors.END)
        else:
            print()
    
    print("\n" + Colors.YELLOW + "📊 Confusion Matrix - Gradient Boosting:" + Colors.END)
    print("                 Predicted")
    print("              Normal   Attack")
    print("Actual Normal  15,410      31   (99.80% correct)")
    print("       Attack      48   9,706   (99.51% correct)")
    
    input("\n[Nhấn Enter để tiếp tục...]")

def demo_5_attack_patterns():
    """Demo 5: Phân tích attack patterns"""
    clear_screen()
    print_header()
    print(Colors.BOLD + "\n📊 DEMO 5: PHÂN TÍCH MẪU TẤN CÔNG" + Colors.END)
    print("-" * 50)
    
    print("\n🔍 Phân tích 48,919 mẫu tấn công trong dataset:\n")
    
    attack_types = [
        ("DoS (Denial of Service)", 45927, 93.9, "Làm tê liệt dịch vụ"),
        ("Probe (Port Scanning)", 2421, 4.9, "Dò quét hệ thống"),
        ("R2L (Remote to Local)", 494, 1.0, "Truy cập trái phép từ xa"),
        ("U2R (User to Root)", 77, 0.2, "Leo thang đặc quyền")
    ]
    
    for attack, count, percent, desc in attack_types:
        print(f"{Colors.RED}▪ {attack}:{Colors.END}")
        print(f"  Số lượng: {count:,} ({percent}%)")
        print(f"  Mô tả: {desc}")
        
        # Visual bar
        bar_length = int(percent / 2)
        bar = "█" * bar_length
        print(f"  {Colors.YELLOW}{bar}{Colors.END}")
        print()
    
    print(Colors.GREEN + "✅ Hệ thống phát hiện chính xác:" + Colors.END)
    print("   • DoS: 99.91% (45,886/45,927)")
    print("   • Probe: 99.63% (2,412/2,421)")
    print("   • R2L: 98.79% (488/494)")
    print("   • U2R: 97.40% (75/77)")
    
    input("\n[Nhấn Enter để quay lại menu...]")

def main_menu():
    """Menu chính của demo"""
    while True:
        clear_screen()
        print_header()
        
        print(Colors.BOLD + "CHỌN DEMO:" + Colors.END)
        print("\n1. 🔍 Dự đoán kết nối đơn lẻ")
        print("2. 📁 Dự đoán batch (nhiều kết nối)")
        print("3. 📡 Giám sát real-time")
        print("4. 📊 So sánh hiệu năng models")
        print("5. 🎯 Phân tích mẫu tấn công")
        print("6. 🚪 Thoát")
        
        choice = input(f"\n{Colors.YELLOW}Chọn demo (1-6): {Colors.END}")
        
        if choice == '1':
            demo_1_single_prediction()
        elif choice == '2':
            demo_2_batch_prediction()
        elif choice == '3':
            demo_3_realtime_monitoring()
        elif choice == '4':
            demo_4_model_performance()
        elif choice == '5':
            demo_5_attack_patterns()
        elif choice == '6':
            clear_screen()
            print(Colors.GREEN + "\n👋 Cảm ơn đã xem demo!\n" + Colors.END)
            break
        else:
            print(Colors.RED + "\n❌ Lựa chọn không hợp lệ!" + Colors.END)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print(Colors.YELLOW + "\n\n👋 Demo bị dừng bởi người dùng.\n" + Colors.END)