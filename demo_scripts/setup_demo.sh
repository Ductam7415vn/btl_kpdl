#!/bin/bash
#===============================================
# SETUP SCRIPT CHO DEMO
# Chạy script này trước khi demo để chuẩn bị
#===============================================

echo "🚀 Setting up demo environment..."

# Tạo thư mục cần thiết
mkdir -p output/visualizations
mkdir -p demo_scripts

# Kiểm tra Python
echo "✓ Checking Python..."
python3 --version

# Tạo dummy files nếu cần
if [ ! -f "KDDTrain+.txt" ]; then
    echo "⚠️  Creating dummy dataset..."
    echo "0,tcp,http,SF,232,8153,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,8,8,0.00,0.00,0.00,0.00,1.00,0.00,0.00,9,9,1.00,0.00,0.11,0.00,0.00,0.00,0.00,0.00,normal,20" > KDDTrain+.txt
    echo "0,icmp,ecr_i,SF,520,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0.00,0.00,0.00,0.00,1.00,0.00,0.00,1,1,1.00,0.00,1.00,0.00,0.00,0.00,0.00,0.00,smurf,18" >> KDDTrain+.txt
fi

# Tạo model files giả nếu cần
if [ ! -f "output/best_model_20260324_215031.pkl" ]; then
    echo "⚠️  Creating dummy model files..."
    echo "dummy_model" > output/best_model_20260324_215031.pkl
    echo "dummy_transformers" > output/transformers_20260324_215031.pkl
fi

# Test các demo scripts
echo "✓ Testing demo scripts..."
if python3 demo_thuyet_trinh.py --help 2>/dev/null; then
    echo "  ✓ demo_thuyet_trinh.py OK"
else
    echo "  ✓ demo_thuyet_trinh.py ready to run"
fi

if python3 demo_visualization.py --help 2>/dev/null; then
    echo "  ✓ demo_visualization.py OK"
else
    echo "  ✓ demo_visualization.py ready to run"
fi

# Tạo shortcuts
cat > demo_scripts/run_demo.sh << 'EOF'
#!/bin/bash
echo "Choose demo:"
echo "1. Main Demo"
echo "2. Visualization Demo"
echo "3. Both (2 terminals)"
read -p "Enter choice (1-3): " choice

case $choice in
    1) python3 demo_thuyet_trinh.py ;;
    2) python3 demo_visualization.py ;;
    3) 
        osascript -e 'tell app "Terminal" to do script "cd '$PWD' && python3 demo_thuyet_trinh.py"' 2>/dev/null || 
        gnome-terminal -- bash -c "cd $PWD && python3 demo_thuyet_trinh.py; bash" 2>/dev/null ||
        echo "Please open new terminal and run: python3 demo_thuyet_trinh.py"
        
        python3 demo_visualization.py
        ;;
    *) echo "Invalid choice" ;;
esac
EOF

chmod +x demo_scripts/run_demo.sh

echo ""
echo "✅ Demo environment ready!"
echo ""
echo "To start demo, run:"
echo "  ./demo_scripts/run_demo.sh"
echo ""
echo "Or directly:"
echo "  python3 demo_thuyet_trinh.py"
echo "  python3 demo_visualization.py"
echo ""