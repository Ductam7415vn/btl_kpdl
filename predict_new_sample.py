"""
=============================================================================
MODULE DỰ ĐOÁN MẪU MỚI - NETWORK INTRUSION DETECTION
=============================================================================
Tác giả: Data Science & Security Expert
Mô tả: Module này cung cấp các hàm để dự đoán mẫu mới sử dụng model đã train
       và các transformer đã lưu từ quá trình tiền xử lý.
=============================================================================
"""

import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime


class NetworkIntrusionPredictor:
    """
    Class để dự đoán xâm nhập mạng cho mẫu mới.
    """
    
    def __init__(self, model_path, transformers_path):
        """
        Khởi tạo predictor với model và transformers đã lưu.
        
        Parameters:
        -----------
        model_path : str
            Đường dẫn đến file model (.pkl)
        transformers_path : str
            Đường dẫn đến file transformers (.pkl)
        """
        print("🔄 Đang load model và transformers...")
        
        # Load model
        self.model = joblib.load(model_path)
        print(f"✓ Đã load model từ: {model_path}")
        
        # Load transformers (scaler và encoders)
        transformers = joblib.load(transformers_path)
        self.scaler = transformers['scaler']
        self.encoders = transformers['encoders']
        print(f"✓ Đã load transformers từ: {transformers_path}")
        
        # Danh sách tên cột (41 features)
        self.feature_names = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 
            'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
            'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
            'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
            'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login',
            'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate',
            'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
            'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
            'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
            'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
        ]
        
        # Các cột categorical
        self.categorical_columns = ['protocol_type', 'service', 'flag']
        
        print(f"✓ Predictor sẵn sàng!")
    
    
    def preprocess_sample(self, sample_dict):
        """
        Tiền xử lý một mẫu dữ liệu mới.
        
        Parameters:
        -----------
        sample_dict : dict
            Dictionary chứa giá trị của 41 features
            
        Returns:
        --------
        numpy.ndarray
            Mẫu đã được tiền xử lý
        """
        # Tạo DataFrame từ dict
        df = pd.DataFrame([sample_dict])
        
        # Đảm bảo có đủ các cột và đúng thứ tự
        df = df.reindex(columns=self.feature_names, fill_value=0)
        
        # Encode các cột categorical
        for col in self.categorical_columns:
            if col in self.encoders:
                try:
                    # Xử lý trường hợp giá trị mới không có trong training
                    if df[col].iloc[0] in self.encoders[col].classes_:
                        df[col] = self.encoders[col].transform(df[col])
                    else:
                        # Gán giá trị mặc định nếu không tìm thấy
                        print(f"⚠ Giá trị '{df[col].iloc[0]}' của '{col}' không có trong training data.")
                        print(f"  Sử dụng giá trị mặc định.")
                        df[col] = 0
                except:
                    df[col] = 0
        
        # Chuẩn hóa dữ liệu
        df_scaled = self.scaler.transform(df)
        
        return df_scaled
    
    
    def predict(self, sample_dict):
        """
        Dự đoán một mẫu mới.
        
        Parameters:
        -----------
        sample_dict : dict
            Dictionary chứa giá trị của 41 features
            
        Returns:
        --------
        dict: Kết quả dự đoán bao gồm label và probability
        """
        # Tiền xử lý mẫu
        sample_processed = self.preprocess_sample(sample_dict)
        
        # Dự đoán
        prediction = self.model.predict(sample_processed)[0]
        
        # Lấy probability nếu model hỗ trợ
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(sample_processed)[0]
            normal_proba = proba[0]
            attack_proba = proba[1]
        else:
            normal_proba = 1.0 if prediction == 0 else 0.0
            attack_proba = 1.0 if prediction == 1 else 0.0
        
        # Tạo kết quả
        result = {
            'prediction': int(prediction),
            'label': 'Normal' if prediction == 0 else 'Attack',
            'confidence': {
                'normal': float(normal_proba),
                'attack': float(attack_proba)
            },
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return result
    
    
    def predict_batch(self, samples_list):
        """
        Dự đoán nhiều mẫu cùng lúc.
        
        Parameters:
        -----------
        samples_list : list of dict
            Danh sách các mẫu cần dự đoán
            
        Returns:
        --------
        list: Danh sách kết quả dự đoán
        """
        results = []
        
        for i, sample in enumerate(samples_list):
            try:
                result = self.predict(sample)
                result['sample_id'] = i
                results.append(result)
            except Exception as e:
                print(f"✗ Lỗi khi xử lý mẫu {i}: {str(e)}")
                results.append({
                    'sample_id': i,
                    'error': str(e)
                })
        
        return results


def create_sample_connection():
    """
    Tạo một mẫu kết nối mạng ví dụ để test.
    
    Returns:
    --------
    dict: Mẫu kết nối với 41 features
    """
    # Mẫu normal connection
    normal_sample = {
        'duration': 0,
        'protocol_type': 'tcp',
        'service': 'http',
        'flag': 'SF',
        'src_bytes': 180,
        'dst_bytes': 5450,
        'land': 0,
        'wrong_fragment': 0,
        'urgent': 0,
        'hot': 0,
        'num_failed_logins': 0,
        'logged_in': 1,
        'num_compromised': 0,
        'root_shell': 0,
        'su_attempted': 0,
        'num_root': 0,
        'num_file_creations': 0,
        'num_shells': 0,
        'num_access_files': 0,
        'num_outbound_cmds': 0,
        'is_host_login': 0,
        'is_guest_login': 0,
        'count': 8,
        'srv_count': 8,
        'serror_rate': 0.0,
        'srv_serror_rate': 0.0,
        'rerror_rate': 0.0,
        'srv_rerror_rate': 0.0,
        'same_srv_rate': 1.0,
        'diff_srv_rate': 0.0,
        'srv_diff_host_rate': 0.0,
        'dst_host_count': 9,
        'dst_host_srv_count': 9,
        'dst_host_same_srv_rate': 1.0,
        'dst_host_diff_srv_rate': 0.0,
        'dst_host_same_src_port_rate': 0.11,
        'dst_host_srv_diff_host_rate': 0.0,
        'dst_host_serror_rate': 0.0,
        'dst_host_srv_serror_rate': 0.0,
        'dst_host_rerror_rate': 0.0,
        'dst_host_srv_rerror_rate': 0.0
    }
    
    return normal_sample


def create_attack_sample():
    """
    Tạo một mẫu tấn công mạng ví dụ để test.
    
    Returns:
    --------
    dict: Mẫu tấn công với 41 features
    """
    # Mẫu attack (Neptune - DoS attack)
    attack_sample = {
        'duration': 0,
        'protocol_type': 'tcp',
        'service': 'private',
        'flag': 'S0',
        'src_bytes': 0,
        'dst_bytes': 0,
        'land': 0,
        'wrong_fragment': 0,
        'urgent': 0,
        'hot': 0,
        'num_failed_logins': 0,
        'logged_in': 0,
        'num_compromised': 0,
        'root_shell': 0,
        'su_attempted': 0,
        'num_root': 0,
        'num_file_creations': 0,
        'num_shells': 0,
        'num_access_files': 0,
        'num_outbound_cmds': 0,
        'is_host_login': 0,
        'is_guest_login': 0,
        'count': 255,
        'srv_count': 1,
        'serror_rate': 1.0,
        'srv_serror_rate': 1.0,
        'rerror_rate': 0.0,
        'srv_rerror_rate': 0.0,
        'same_srv_rate': 0.0,
        'diff_srv_rate': 0.0,
        'srv_diff_host_rate': 0.0,
        'dst_host_count': 255,
        'dst_host_srv_count': 255,
        'dst_host_same_srv_rate': 1.0,
        'dst_host_diff_srv_rate': 0.0,
        'dst_host_same_src_port_rate': 1.0,
        'dst_host_srv_diff_host_rate': 0.0,
        'dst_host_serror_rate': 1.0,
        'dst_host_srv_serror_rate': 1.0,
        'dst_host_rerror_rate': 0.0,
        'dst_host_srv_rerror_rate': 0.0
    }
    
    return attack_sample


def demo_prediction():
    """
    Demo sử dụng predictor với các mẫu test.
    """
    print("\n" + "="*70)
    print("DEMO DỰ ĐOÁN MẪU MỚI")
    print("="*70)
    
    # Đường dẫn đến model và transformers (cập nhật theo file thực tế)
    model_path = "output/best_model_*.pkl"  # Thay * bằng timestamp thực tế
    transformers_path = "output/transformers_*.pkl"  # Thay * bằng timestamp thực tế
    
    # Kiểm tra file tồn tại
    import glob
    model_files = glob.glob("output/best_model_*.pkl")
    transformer_files = glob.glob("output/transformers_*.pkl")
    
    if not model_files or not transformer_files:
        print("✗ Không tìm thấy model hoặc transformers!")
        print("  Vui lòng chạy training trước.")
        return
    
    # Sử dụng file mới nhất
    model_path = sorted(model_files)[-1]
    transformers_path = sorted(transformer_files)[-1]
    
    # Khởi tạo predictor
    predictor = NetworkIntrusionPredictor(model_path, transformers_path)
    
    # Test với mẫu normal
    print("\n" + "-"*70)
    print("TEST 1: Mẫu Normal Connection")
    print("-"*70)
    normal_sample = create_sample_connection()
    result = predictor.predict(normal_sample)
    print(f"🔍 Kết quả dự đoán:")
    print(f"   • Label: {result['label']}")
    print(f"   • Confidence Normal: {result['confidence']['normal']:.2%}")
    print(f"   • Confidence Attack: {result['confidence']['attack']:.2%}")
    
    # Test với mẫu attack
    print("\n" + "-"*70)
    print("TEST 2: Mẫu Attack Connection")
    print("-"*70)
    attack_sample = create_attack_sample()
    result = predictor.predict(attack_sample)
    print(f"🔍 Kết quả dự đoán:")
    print(f"   • Label: {result['label']}")
    print(f"   • Confidence Normal: {result['confidence']['normal']:.2%}")
    print(f"   • Confidence Attack: {result['confidence']['attack']:.2%}")
    
    # Test batch prediction
    print("\n" + "-"*70)
    print("TEST 3: Batch Prediction")
    print("-"*70)
    samples = [normal_sample, attack_sample, normal_sample]
    results = predictor.predict_batch(samples)
    
    for result in results:
        if 'error' not in result:
            print(f"Sample {result['sample_id']}: {result['label']} "
                  f"(confidence: {max(result['confidence'].values()):.2%})")
    
    print("\n✓ Demo hoàn tất!")


if __name__ == "__main__":
    # Chạy demo
    demo_prediction()