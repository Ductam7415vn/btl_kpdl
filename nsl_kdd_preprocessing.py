"""
=============================================================================
TIỀN XỬ LÝ DỮ LIỆU NSL-KDD CHO BÀI TOÁN NETWORK INTRUSION DETECTION
=============================================================================
Tác giả: Data Science & Security Expert
Mô tả: Script này thực hiện các bước tiền xử lý dữ liệu NSL-KDD/KDD99
       để chuẩn bị cho các mô hình Machine Learning phát hiện xâm nhập mạng.

Tối ưu hóa cho: Apple Silicon (M1/M2/M3)
=============================================================================
"""

# =============================================================================
# PHẦN 1: IMPORT CÁC THƯ VIỆN CẦN THIẾT
# =============================================================================

import os
import numpy as np
import pandas as pd

# Cần set trước khi import sklearn/joblib để tránh warning loky trên macOS.
_LOGICAL_CORES = os.cpu_count() or 1
# Đặt nhỏ hơn số core logic để joblib không gọi nhánh dò physical cores.
os.environ.setdefault('LOKY_MAX_CPU_COUNT', str(max(1, _LOGICAL_CORES - 1)))

from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
from sklearn.model_selection import cross_val_score, StratifiedKFold
import warnings
import time

# Tắt các cảnh báo không cần thiết để output sạch hơn
warnings.filterwarnings('ignore')

# Cấu hình pandas để hiển thị đầy đủ dữ liệu khi in
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("=" * 70)
print("TIỀN XỬ LÝ DỮ LIỆU NSL-KDD - NETWORK INTRUSION DETECTION")
print("=" * 70)


# =============================================================================
# PHẦN 2: ĐỊNH NGHĨA TÊN CÁC CỘT (41 FEATURES + LABEL)
# =============================================================================
"""
Bộ dữ liệu NSL-KDD có 41 thuộc tính (features) được chia thành 4 nhóm:
1. Basic Features (1-9): Các đặc trưng cơ bản của kết nối TCP
2. Content Features (10-22): Đặc trưng nội dung trong kết nối
3. Time-based Traffic Features (23-31): Đặc trưng lưu lượng theo thời gian
4. Host-based Traffic Features (32-41): Đặc trưng lưu lượng theo host
"""

# Danh sách đầy đủ 41 tên cột theo chuẩn NSL-KDD
column_names = [
    # === BASIC FEATURES (Đặc trưng cơ bản của kết nối TCP) ===
    'duration',           # 1. Thời gian kết nối (giây)
    'protocol_type',      # 2. Loại giao thức (tcp, udp, icmp)
    'service',            # 3. Dịch vụ mạng (http, ftp, smtp, ...)
    'flag',               # 4. Trạng thái kết nối (SF, S0, REJ, ...)
    'src_bytes',          # 5. Số bytes từ nguồn đến đích
    'dst_bytes',          # 6. Số bytes từ đích đến nguồn
    'land',               # 7. 1 nếu src/dst host và port giống nhau
    'wrong_fragment',     # 8. Số fragment lỗi
    'urgent',             # 9. Số gói tin urgent

    # === CONTENT FEATURES (Đặc trưng nội dung) ===
    'hot',                # 10. Số chỉ số "hot"
    'num_failed_logins',  # 11. Số lần đăng nhập thất bại
    'logged_in',          # 12. 1 nếu đăng nhập thành công
    'num_compromised',    # 13. Số điều kiện bị xâm phạm
    'root_shell',         # 14. 1 nếu có root shell
    'su_attempted',       # 15. 1 nếu lệnh "su root" được thử
    'num_root',           # 16. Số truy cập root
    'num_file_creations', # 17. Số thao tác tạo file
    'num_shells',         # 18. Số shell prompts
    'num_access_files',   # 19. Số thao tác truy cập file điều khiển
    'num_outbound_cmds',  # 20. Số lệnh outbound trong phiên ftp
    'is_host_login',      # 21. 1 nếu login thuộc host list
    'is_guest_login',     # 22. 1 nếu login là guest

    # === TIME-BASED TRAFFIC FEATURES (Đặc trưng theo thời gian - 2 giây) ===
    'count',              # 23. Số kết nối đến cùng host trong 2s
    'srv_count',          # 24. Số kết nối đến cùng service trong 2s
    'serror_rate',        # 25. Tỷ lệ kết nối có lỗi SYN
    'srv_serror_rate',    # 26. Tỷ lệ lỗi SYN theo service
    'rerror_rate',        # 27. Tỷ lệ kết nối có lỗi REJ
    'srv_rerror_rate',    # 28. Tỷ lệ lỗi REJ theo service
    'same_srv_rate',      # 29. Tỷ lệ kết nối đến cùng service
    'diff_srv_rate',      # 30. Tỷ lệ kết nối đến khác service
    'srv_diff_host_rate', # 31. Tỷ lệ kết nối đến khác host

    # === HOST-BASED TRAFFIC FEATURES (Đặc trưng theo host - 100 kết nối) ===
    'dst_host_count',              # 32. Số kết nối đến cùng dst host
    'dst_host_srv_count',          # 33. Số kết nối đến cùng service
    'dst_host_same_srv_rate',      # 34. Tỷ lệ cùng service
    'dst_host_diff_srv_rate',      # 35. Tỷ lệ khác service
    'dst_host_same_src_port_rate', # 36. Tỷ lệ cùng src port
    'dst_host_srv_diff_host_rate', # 37. Tỷ lệ khác host theo service
    'dst_host_serror_rate',        # 38. Tỷ lệ lỗi SYN theo dst host
    'dst_host_srv_serror_rate',    # 39. Tỷ lệ lỗi SYN theo service
    'dst_host_rerror_rate',        # 40. Tỷ lệ lỗi REJ theo dst host
    'dst_host_srv_rerror_rate',    # 41. Tỷ lệ lỗi REJ theo service

    # === LABEL (Nhãn phân loại) ===
    'label'               # Nhãn: normal hoặc loại tấn công
]

# Lưu ý: Một số phiên bản NSL-KDD có thêm cột 'difficulty_level' ở cuối
# Chúng ta sẽ xử lý trường hợp này trong phần load dữ liệu


# =============================================================================
# PHẦN 3: LOAD DỮ LIỆU TỪ FILE
# =============================================================================
"""
Hàm này đọc file dữ liệu KDD và xử lý các trường hợp đặc biệt:
- File không có header
- File có thể có thêm cột difficulty_level
- Xử lý dấu '.' ở cuối label trong một số phiên bản
"""

def load_kdd_data(file_path):
    """
    Đọc và load dữ liệu NSL-KDD từ file.

    Parameters:
    -----------
    file_path : str
        Đường dẫn đến file dữ liệu (txt hoặc csv)

    Returns:
    --------
    pandas.DataFrame
        DataFrame chứa dữ liệu đã được load với tên cột đúng
    """
    print("\n" + "-" * 70)
    print("BƯỚC 1: LOAD DỮ LIỆU")
    print("-" * 70)

    try:
        # Đọc dữ liệu thô trước để xử lý chắc chắn các trường hợp:
        # - KDD99: 42 cột (41 features + label)
        # - NSL-KDD: 43 cột (thêm difficulty_level)
        raw_df = pd.read_csv(
            file_path,
            header=None,      # File gốc không có header
            low_memory=False  # Tắt low_memory để tránh cảnh báo dtype
        )

        expected_cols = len(column_names)  # 42 cột: 41 features + label
        raw_col_count = raw_df.shape[1]

        if raw_col_count < expected_cols:
            raise ValueError(
                f"Số cột không hợp lệ: {raw_col_count}. "
                f"File cần tối thiểu {expected_cols} cột theo chuẩn KDD."
            )

        if raw_col_count == expected_cols:
            # Trường hợp chuẩn KDD99: giữ nguyên 42 cột
            df = raw_df.copy()
        elif raw_col_count == expected_cols + 1:
            # Trường hợp NSL-KDD: cột cuối là difficulty_level, loại bỏ
            print("⚠ Phát hiện cột 'difficulty_level' (NSL-KDD), tiến hành loại bỏ...")
            df = raw_df.iloc[:, :expected_cols].copy()
        else:
            # Trường hợp có nhiều cột phụ hơn dự kiến: chỉ giữ 42 cột đầu
            print(
                f"⚠ Phát hiện {raw_col_count} cột (nhiều hơn chuẩn), "
                f"chỉ giữ {expected_cols} cột đầu tiên."
            )
            df = raw_df.iloc[:, :expected_cols].copy()

        # Gán tên cột chuẩn cho DataFrame sau khi đã cắt đúng số cột
        df.columns = column_names

        # Xử lý trường hợp label có dấu '.' ở cuối (ví dụ: 'normal.')
        df['label'] = df['label'].astype(str).str.replace('.', '', regex=False).str.strip()

        print(f"✓ Load thành công từ: {file_path}")
        print(f"✓ Kích thước dữ liệu gốc: {raw_df.shape[0]:,} dòng x {raw_df.shape[1]} cột")
        print(f"✓ Kích thước dữ liệu sau chuẩn hóa cột: {df.shape[0]:,} dòng x {df.shape[1]} cột")

        return df

    except FileNotFoundError:
        print(f"✗ Lỗi: Không tìm thấy file '{file_path}'")
        print("  Vui lòng kiểm tra đường dẫn file.")
        return None
    except Exception as e:
        print(f"✗ Lỗi khi đọc file: {str(e)}")
        return None


# =============================================================================
# PHẦN 4: LÀM SẠCH DỮ LIỆU
# =============================================================================
"""
Bước này thực hiện:
1. Loại bỏ các bản ghi trùng lặp (duplicates)
2. Xử lý các giá trị rỗng/thiếu (missing values)
3. Kiểm tra và báo cáo chất lượng dữ liệu
"""

def clean_data(df):
    """
    Làm sạch dữ liệu bằng cách loại bỏ duplicates và xử lý missing values.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame cần làm sạch

    Returns:
    --------
    pandas.DataFrame
        DataFrame đã được làm sạch
    """
    print("\n" + "-" * 70)
    print("BƯỚC 2: LÀM SẠCH DỮ LIỆU")
    print("-" * 70)

    original_shape = df.shape

    # --- 2.1: Kiểm tra và xử lý Missing Values ---
    print("\n[2.1] Kiểm tra Missing Values:")
    missing_count = df.isnull().sum().sum()

    if missing_count > 0:
        print(f"  • Tổng số giá trị rỗng: {missing_count:,}")

        # Hiển thị chi tiết các cột có missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        for col in missing_cols:
            null_count = df[col].isnull().sum()
            print(f"    - {col}: {null_count:,} giá trị rỗng")

        # Xử lý missing values
        # Với dữ liệu số: điền bằng median (ít bị ảnh hưởng bởi outliers)
        # Với dữ liệu categorical: điền bằng mode (giá trị phổ biến nhất)
        for col in missing_cols:
            if df[col].dtype in ['int64', 'float64']:
                df[col] = df[col].fillna(df[col].median())
                print(f"    → Điền {col} bằng median")
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
                print(f"    → Điền {col} bằng mode")
    else:
        print("  ✓ Không có giá trị rỗng trong dữ liệu")

    # --- 2.2: Loại bỏ Duplicates ---
    print("\n[2.2] Kiểm tra và loại bỏ bản ghi trùng lặp:")
    duplicates_count = df.duplicated().sum()

    if duplicates_count > 0:
        print(f"  • Số bản ghi trùng lặp: {duplicates_count:,}")
        df = df.drop_duplicates(keep='first')  # Giữ lại bản ghi đầu tiên
        print(f"  ✓ Đã loại bỏ {duplicates_count:,} bản ghi trùng lặp")
    else:
        print("  ✓ Không có bản ghi trùng lặp")

    # --- 2.3: Báo cáo kết quả ---
    print("\n[2.3] Kết quả làm sạch dữ liệu:")
    print(f"  • Kích thước trước: {original_shape[0]:,} dòng x {original_shape[1]} cột")
    print(f"  • Kích thước sau:  {df.shape[0]:,} dòng x {df.shape[1]} cột")
    print(f"  • Số dòng đã loại bỏ: {original_shape[0] - df.shape[0]:,}")

    return df


# =============================================================================
# PHẦN 5: CHUYỂN ĐỔI NHÃN (BINARY CLASSIFICATION)
# =============================================================================
"""
Trong bài toán phát hiện xâm nhập mạng, ta có 2 cách phân loại:
1. Binary Classification: Normal (0) vs Attack (1)
2. Multi-class Classification: Phân loại từng loại tấn công cụ thể

Script này sử dụng Binary Classification để đơn giản hóa bài toán.
"""

# Danh sách các loại tấn công trong NSL-KDD (để tham khảo)
ATTACK_TYPES = {
    # DoS (Denial of Service) - Tấn công từ chối dịch vụ
    'dos': ['back', 'land', 'neptune', 'pod', 'smurf', 'teardrop',
            'apache2', 'udpstorm', 'processtable', 'mailbomb'],

    # Probe - Tấn công thăm dò
    'probe': ['satan', 'ipsweep', 'nmap', 'portsweep', 'mscan', 'saint'],

    # R2L (Remote to Local) - Tấn công từ xa vào local
    'r2l': ['guess_passwd', 'ftp_write', 'imap', 'phf', 'multihop',
            'warezmaster', 'warezclient', 'spy', 'xlock', 'xsnoop',
            'snmpguess', 'snmpgetattack', 'httptunnel', 'sendmail', 'named'],

    # U2R (User to Root) - Tấn công leo thang đặc quyền
    'u2r': ['buffer_overflow', 'loadmodule', 'rootkit', 'perl', 'sqlattack',
            'xterm', 'ps', 'httptunnel', 'worm']
}

def convert_to_binary_labels(df):
    """
    Chuyển đổi nhãn thành dạng nhị phân (Binary Classification).
    - 'normal' → 0 (Lưu lượng bình thường)
    - Tất cả loại tấn công khác → 1 (Tấn công)

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame chứa cột 'label'

    Returns:
    --------
    pandas.DataFrame
        DataFrame với cột 'label' đã được chuyển đổi
    """
    print("\n" + "-" * 70)
    print("BƯỚC 3: CHUYỂN ĐỔI NHÃN (BINARY CLASSIFICATION)")
    print("-" * 70)

    # Thống kê phân phối nhãn trước khi chuyển đổi
    print("\n[3.1] Phân phối nhãn ban đầu:")
    label_counts = df['label'].value_counts()
    print(f"  • Tổng số loại nhãn: {len(label_counts)}")
    print(f"  • Top 10 nhãn phổ biến nhất:")
    for label, count in label_counts.head(10).items():
        percentage = (count / len(df)) * 100
        print(f"    - {label}: {count:,} ({percentage:.2f}%)")

    # Đếm số lượng normal vs attack trước khi chuyển đổi
    normal_count = (df['label'] == 'normal').sum()
    attack_count = (df['label'] != 'normal').sum()

    print(f"\n[3.2] Thống kê Normal vs Attack:")
    print(f"  • Normal: {normal_count:,} ({normal_count/len(df)*100:.2f}%)")
    print(f"  • Attack: {attack_count:,} ({attack_count/len(df)*100:.2f}%)")

    # Chuyển đổi nhãn sang dạng nhị phân
    # Sử dụng numpy where để tối ưu hiệu năng
    df['label'] = np.where(df['label'] == 'normal', 0, 1)

    print(f"\n[3.3] Chuyển đổi hoàn tất:")
    print(f"  • Label 0 (Normal): {(df['label'] == 0).sum():,}")
    print(f"  • Label 1 (Attack): {(df['label'] == 1).sum():,}")

    return df


# =============================================================================
# PHẦN 6: ENCODING DỮ LIỆU CATEGORICAL
# =============================================================================
"""
Các cột categorical trong NSL-KDD:
1. protocol_type: tcp, udp, icmp (3 giá trị)
2. service: http, ftp_data, smtp, ... (70 giá trị)
3. flag: SF, S0, REJ, RSTR, ... (11 giá trị)

Có 2 phương pháp encoding phổ biến:
1. LabelEncoder: Chuyển mỗi category thành 1 số (0, 1, 2, ...)
   - Ưu điểm: Không tăng số chiều
   - Nhược điểm: Có thể tạo ra thứ tự giả (ordinal relationship)

2. OneHotEncoder: Tạo cột nhị phân cho mỗi category
   - Ưu điểm: Không tạo thứ tự giả
   - Nhược điểm: Tăng đáng kể số chiều (đặc biệt với 'service')

Script này sử dụng LabelEncoder cho hiệu năng tốt hơn.
"""

def encode_categorical_features(df, method='label'):
    """
    Mã hóa các cột categorical thành dạng số.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame chứa các cột categorical
    method : str
        Phương pháp encoding: 'label' hoặc 'onehot'

    Returns:
    --------
    tuple: (DataFrame đã encode, dict chứa các encoder)
    """
    print("\n" + "-" * 70)
    print("BƯỚC 4: ENCODING DỮ LIỆU CATEGORICAL")
    print("-" * 70)

    # Xác định các cột categorical (dữ liệu dạng chuỗi/object)
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    # Loại bỏ 'label' khỏi danh sách nếu có (đã xử lý ở bước trước)
    if 'label' in categorical_columns:
        categorical_columns.remove('label')

    print(f"\n[4.1] Các cột Categorical cần encode:")
    for col in categorical_columns:
        unique_count = df[col].nunique()
        print(f"  • {col}: {unique_count} giá trị unique")
        # Hiển thị một vài giá trị mẫu
        sample_values = df[col].unique()[:5]
        print(f"    Mẫu: {list(sample_values)}")

    print(f"\n[4.2] Kích thước trước encoding: {df.shape}")

    # Dictionary để lưu các encoder (có thể dùng lại cho test set)
    encoders = {}

    if method == 'label':
        # === LABEL ENCODING ===
        print("\n[4.3] Sử dụng LabelEncoder:")

        for col in categorical_columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
            print(f"  ✓ Encoded '{col}': {len(le.classes_)} classes → [0, {len(le.classes_)-1}]")

    elif method == 'onehot':
        # === ONE-HOT ENCODING ===
        print("\n[4.3] Sử dụng OneHotEncoder (get_dummies):")

        # Sử dụng pandas get_dummies cho đơn giản
        df = pd.get_dummies(df, columns=categorical_columns, drop_first=False)
        print(f"  ✓ Đã tạo {len(df.columns) - len(column_names) + len(categorical_columns)} cột mới")

    print(f"\n[4.4] Kích thước sau encoding: {df.shape}")

    # Kiểm tra không còn cột object nào
    remaining_objects = df.select_dtypes(include=['object']).columns.tolist()
    if len(remaining_objects) == 0:
        print("  ✓ Tất cả các cột đã được chuyển sang dạng số")
    else:
        print(f"  ⚠ Còn {len(remaining_objects)} cột chưa được encode: {remaining_objects}")

    return df, encoders


# =============================================================================
# PHẦN 7: CHUẨN HÓA DỮ LIỆU (NORMALIZATION/SCALING)
# =============================================================================
"""
Chuẩn hóa dữ liệu giúp:
1. Các thuộc tính có scale khác nhau được đưa về cùng thang đo
2. Cải thiện hiệu suất và tốc độ hội tụ của các thuật toán ML
3. Tránh các thuộc tính có giá trị lớn chi phối mô hình

Hai phương pháp phổ biến:
1. StandardScaler (Z-score): x' = (x - mean) / std
   - Phù hợp với dữ liệu có phân phối Gaussian
   - Giá trị output có thể âm

2. MinMaxScaler: x' = (x - min) / (max - min)
   - Đưa giá trị về khoảng [0, 1]
   - Phù hợp khi cần giá trị không âm
"""

def normalize_features(df, method='standard', exclude_cols=['label']):
    """
    Chuẩn hóa các cột số trong DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame cần chuẩn hóa
    method : str
        Phương pháp: 'standard' (Z-score) hoặc 'minmax'
    exclude_cols : list
        Danh sách các cột không cần chuẩn hóa (vd: label)

    Returns:
    --------
    tuple: (DataFrame đã chuẩn hóa, scaler object)
    """
    print("\n" + "-" * 70)
    print("BƯỚC 5: CHUẨN HÓA DỮ LIỆU (NORMALIZATION)")
    print("-" * 70)

    # Xác định các cột cần chuẩn hóa
    feature_cols = [col for col in df.columns if col not in exclude_cols]

    print(f"\n[5.1] Thông tin trước chuẩn hóa:")
    print(f"  • Số cột cần chuẩn hóa: {len(feature_cols)}")
    print(f"  • Các cột không chuẩn hóa: {exclude_cols}")

    # Hiển thị thống kê một số cột mẫu
    print(f"\n[5.2] Thống kê một số features (trước chuẩn hóa):")
    sample_cols = ['duration', 'src_bytes', 'dst_bytes', 'count']
    sample_cols = [col for col in sample_cols if col in feature_cols]
    if sample_cols:
        print(df[sample_cols].describe().round(2).to_string())

    # Chọn scaler dựa trên phương pháp
    if method == 'standard':
        scaler = StandardScaler()
        print(f"\n[5.3] Sử dụng StandardScaler (Z-score normalization)")
        print("  Công thức: x' = (x - mean) / std")
    else:
        scaler = MinMaxScaler()
        print(f"\n[5.3] Sử dụng MinMaxScaler")
        print("  Công thức: x' = (x - min) / (max - min)")

    # Thực hiện chuẩn hóa
    # Chuyển đổi sang float32 để tối ưu bộ nhớ trên M1
    df[feature_cols] = scaler.fit_transform(df[feature_cols]).astype(np.float32)

    # Hiển thị thống kê sau chuẩn hóa
    print(f"\n[5.4] Thống kê một số features (sau chuẩn hóa):")
    if sample_cols:
        print(df[sample_cols].describe().round(4).to_string())

    print(f"\n  ✓ Đã chuẩn hóa {len(feature_cols)} cột features")

    return df, scaler


# =============================================================================
# PHẦN 8: PHÂN CHIA DỮ LIỆU (TRAIN/TEST SPLIT)
# =============================================================================
"""
Phân chia dữ liệu thành:
- X: Ma trận đặc trưng (features matrix)
- y: Vector nhãn mục tiêu (target vector)

Có thể tiếp tục chia X, y thành train/test sets nếu cần.
"""

def split_features_and_labels(df, label_col='label'):
    """
    Tách DataFrame thành ma trận đặc trưng X và vector nhãn y.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame đã qua tiền xử lý
    label_col : str
        Tên cột nhãn

    Returns:
    --------
    tuple: (X, y) - ma trận features và vector labels
    """
    print("\n" + "-" * 70)
    print("BƯỚC 6: PHÂN CHIA DỮ LIỆU")
    print("-" * 70)

    # Tách features (X) và labels (y)
    X = df.drop(columns=[label_col])
    y = df[label_col]

    print(f"\n[6.1] Kết quả phân chia:")
    print(f"  • Ma trận đặc trưng X: {X.shape}")
    print(f"    - Số mẫu: {X.shape[0]:,}")
    print(f"    - Số features: {X.shape[1]}")
    print(f"  • Vector nhãn y: {y.shape}")
    print(f"    - Số mẫu: {len(y):,}")

    print(f"\n[6.2] Phân phối nhãn trong y:")
    for label, count in y.value_counts().items():
        percentage = (count / len(y)) * 100
        label_name = "Normal" if label == 0 else "Attack"
        print(f"  • {label} ({label_name}): {count:,} ({percentage:.2f}%)")

    print(f"\n[6.3] Kiểu dữ liệu:")
    print(f"  • X dtype: {X.values.dtype}")
    print(f"  • y dtype: {y.dtype}")

    return X, y


def create_train_test_split(X, y, test_size=0.2, random_state=42):
    """
    Chia dữ liệu thành tập huấn luyện và tập kiểm tra.

    Parameters:
    -----------
    X : DataFrame/ndarray
        Ma trận đặc trưng
    y : Series/ndarray
        Vector nhãn
    test_size : float
        Tỷ lệ tập test (mặc định 20%)
    random_state : int
        Seed để reproducibility

    Returns:
    --------
    tuple: (X_train, X_test, y_train, y_test)
    """
    print(f"\n[6.4] Chia Train/Test (test_size={test_size}):")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y  # Đảm bảo tỷ lệ nhãn được giữ nguyên
    )

    print(f"  • Training set: {X_train.shape[0]:,} mẫu ({(1-test_size)*100:.0f}%)")
    print(f"  • Test set: {X_test.shape[0]:,} mẫu ({test_size*100:.0f}%)")

    print(f"\n  Phân phối nhãn trong Training set:")
    for label in [0, 1]:
        count = (y_train == label).sum()
        print(f"    - {label}: {count:,} ({count/len(y_train)*100:.2f}%)")

    print(f"\n  Phân phối nhãn trong Test set:")
    for label in [0, 1]:
        count = (y_test == label).sum()
        print(f"    - {label}: {count:,} ({count/len(y_test)*100:.2f}%)")

    return X_train, X_test, y_train, y_test


# =============================================================================
# PHẦN 9: HÀM CHÍNH (MAIN PIPELINE)
# =============================================================================

def preprocess_kdd_data(file_path, encoding_method='label', scaling_method='standard'):
    """
    Pipeline hoàn chỉnh để tiền xử lý dữ liệu NSL-KDD.

    Parameters:
    -----------
    file_path : str
        Đường dẫn đến file dữ liệu
    encoding_method : str
        Phương pháp encoding: 'label' hoặc 'onehot'
    scaling_method : str
        Phương pháp chuẩn hóa: 'standard' hoặc 'minmax'

    Returns:
    --------
    dict: Dictionary chứa dữ liệu đã tiền xử lý (X, y, scaler, encoder, ...)
    """
    # Bước 1: Load dữ liệu
    df = load_kdd_data(file_path)
    if df is None:
        return None

    # Bước 2: Làm sạch dữ liệu
    df = clean_data(df)

    # Bước 3: Chuyển đổi nhãn
    df = convert_to_binary_labels(df)

    # Bước 4: Encoding categorical
    df, encoders = encode_categorical_features(df, method=encoding_method)

    # Bước 5: Chuẩn hóa dữ liệu
    df, scaler = normalize_features(df, method=scaling_method)

    # Bước 6: Phân chia features và labels
    X, y = split_features_and_labels(df)

    # Tổng kết
    print("\n" + "=" * 70)
    print("TỔNG KẾT QUÁ TRÌNH TIỀN XỬ LÝ")
    print("=" * 70)
    print(f"\n✓ Kích thước dữ liệu cuối cùng:")
    print(f"  • X (features): {X.shape}")
    print(f"  • y (labels):   {y.shape}")
    print(f"  • DataFrame đã xử lý (bao gồm label): {df.shape}")
    print(f"\n✓ Tổng số features: {X.shape[1]}")
    print(f"✓ Encoding method: {encoding_method}")
    print(f"✓ Scaling method: {scaling_method}")
    print("\n" + "=" * 70)

    # Trả về dictionary chứa tất cả kết quả
    return {
        'X': X,
        'y': y,
        'processed_df': df,
        'encoders': encoders,
        'scaler': scaler,
        'feature_names': X.columns.tolist()
    }


# =============================================================================
# PHẦN 10: HUẤN LUYỆN VÀ ĐÁNH GIÁ MÔ HÌNH MACHINE LEARNING
# =============================================================================
"""
Phần này thực hiện:
1. Chia dữ liệu train/test
2. Huấn luyện nhiều mô hình ML phổ biến
3. Đánh giá và so sánh hiệu suất các mô hình
4. Hiển thị kết quả chi tiết (Accuracy, Precision, Recall, F1-Score)
"""

def get_models(mode='fast'):
    """
    Trả về dictionary chứa các mô hình ML cần huấn luyện.

    Returns:
    --------
    dict: Dictionary với tên model và instance của model
    """
    if mode == 'fast':
        # Cấu hình ưu tiên tốc độ cho máy M1, vẫn giữ chất lượng ổn cho báo cáo.
        models = {
            'Decision Tree': DecisionTreeClassifier(
                max_depth=24,
                min_samples_leaf=2,
                random_state=42
            ),
            'Random Forest': RandomForestClassifier(
                n_estimators=60,
                max_depth=24,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            'Logistic Regression': LogisticRegression(
                solver='saga',
                max_iter=400,
                random_state=42,
                n_jobs=-1
            ),
            'Hist Gradient Boosting': HistGradientBoostingClassifier(
                max_iter=100,
                max_depth=12,
                learning_rate=0.1,
                random_state=42
            )
        }
    else:
        # Cấu hình đầy đủ để tham khảo khi cần so sánh nhiều model hơn.
        models = {
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            ),
            'Logistic Regression': LogisticRegression(
                max_iter=1000,
                random_state=42,
                n_jobs=-1
            ),
            'K-Nearest Neighbors': KNeighborsClassifier(
                n_neighbors=5,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                random_state=42
            )
        }

    return models


def train_and_evaluate(X_train, X_test, y_train, y_test, models=None, model_mode='fast'):
    """
    Huấn luyện và đánh giá các mô hình Machine Learning.

    Parameters:
    -----------
    X_train, X_test : array-like
        Dữ liệu features cho training và testing
    y_train, y_test : array-like
        Nhãn cho training và testing
    models : dict, optional
        Dictionary chứa các model. Nếu None, sử dụng mặc định.
    model_mode : str
        Chế độ model: 'fast' (nhanh) hoặc 'full' (đầy đủ)

    Returns:
    --------
    dict: Kết quả đánh giá của từng model
    """
    print("\n" + "=" * 70)
    print("HUẤN LUYỆN VÀ ĐÁNH GIÁ MÔ HÌNH MACHINE LEARNING")
    print("=" * 70)

    if models is None:
        models = get_models(mode=model_mode)

    results = {}

    print(f"\n📊 Thông tin dữ liệu:")
    print(f"   • Training set: {X_train.shape[0]:,} mẫu")
    print(f"   • Test set: {X_test.shape[0]:,} mẫu")
    print(f"   • Số features: {X_train.shape[1]}")

    for name, model in models.items():
        print(f"\n{'─' * 70}")
        print(f"🔄 Đang huấn luyện: {name}")
        print(f"{'─' * 70}")

        # Huấn luyện model
        start_time = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - start_time

        # Dự đoán
        start_time = time.time()
        y_pred = model.predict(X_test)
        predict_time = time.time() - start_time

        # Tính các metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        # Tính ROC-AUC nếu model hỗ trợ predict_proba
        try:
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test)[:, 1]
                roc_auc = roc_auc_score(y_test, y_proba)
            else:
                roc_auc = None
        except:
            roc_auc = None

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)

        # Lưu kết quả
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm,
            'train_time': train_time,
            'predict_time': predict_time
        }

        # Hiển thị kết quả
        print(f"\n📈 Kết quả {name}:")
        print(f"   ┌{'─' * 40}┐")
        print(f"   │ {'Metric':<20} {'Giá trị':>17} │")
        print(f"   ├{'─' * 40}┤")
        print(f"   │ {'Accuracy':<20} {accuracy:>16.4f} │")
        print(f"   │ {'Precision':<20} {precision:>16.4f} │")
        print(f"   │ {'Recall':<20} {recall:>16.4f} │")
        print(f"   │ {'F1-Score':<20} {f1:>16.4f} │")
        if roc_auc:
            print(f"   │ {'ROC-AUC':<20} {roc_auc:>16.4f} │")
        print(f"   └{'─' * 40}┘")

        print(f"\n   ⏱ Thời gian huấn luyện: {train_time:.2f}s")
        print(f"   ⏱ Thời gian dự đoán: {predict_time:.4f}s")

        print(f"\n   📊 Confusion Matrix:")
        print(f"                    Predicted")
        print(f"                  Normal  Attack")
        print(f"   Actual Normal  {cm[0,0]:>6}  {cm[0,1]:>6}")
        print(f"   Actual Attack  {cm[1,0]:>6}  {cm[1,1]:>6}")

    return results


def print_model_comparison(results):
    """
    In bảng so sánh hiệu suất các mô hình.

    Parameters:
    -----------
    results : dict
        Kết quả từ hàm train_and_evaluate
    """
    print("\n" + "=" * 70)
    print("BẢNG SO SÁNH HIỆU SUẤT CÁC MÔ HÌNH")
    print("=" * 70)

    # Header
    print(f"\n{'Model':<22} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1-Score':>10}")
    print("─" * 70)

    # Sắp xếp theo F1-Score giảm dần
    sorted_results = sorted(results.items(), key=lambda x: x[1]['f1_score'], reverse=True)

    for name, metrics in sorted_results:
        print(f"{name:<22} {metrics['accuracy']:>10.4f} {metrics['precision']:>10.4f} "
              f"{metrics['recall']:>10.4f} {metrics['f1_score']:>10.4f}")

    print("─" * 70)

    # Tìm model tốt nhất
    best_model = sorted_results[0]
    print(f"\n🏆 MÔ HÌNH TỐT NHẤT: {best_model[0]}")
    print(f"   • Accuracy:  {best_model[1]['accuracy']:.4f} ({best_model[1]['accuracy']*100:.2f}%)")
    print(f"   • F1-Score:  {best_model[1]['f1_score']:.4f}")
    if best_model[1]['roc_auc']:
        print(f"   • ROC-AUC:   {best_model[1]['roc_auc']:.4f}")

    return best_model


def perform_cross_validation(models, X, y, cv_folds=5, scoring='accuracy'):
    """
    Thực hiện Cross-Validation cho các mô hình.
    
    Parameters:
    -----------
    models : dict
        Dictionary chứa các model cần đánh giá
    X : array-like
        Ma trận features
    y : array-like
        Vector labels
    cv_folds : int
        Số fold cho cross-validation
    scoring : str
        Metric để đánh giá ('accuracy', 'f1', 'roc_auc')
    
    Returns:
    --------
    dict: Kết quả cross-validation cho từng model
    """
    print("\n" + "=" * 70)
    print(f"CROSS-VALIDATION ({cv_folds}-FOLD)")
    print("=" * 70)
    
    # Sử dụng StratifiedKFold để đảm bảo phân phối nhãn cân bằng
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    
    cv_results = {}
    
    for name, model in models.items():
        print(f"\n🔄 Cross-validating: {name}")
        print(f"   Scoring metric: {scoring}")
        
        start_time = time.time()
        
        # Thực hiện cross-validation
        scores = cross_val_score(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)
        
        cv_time = time.time() - start_time
        
        # Lưu kết quả
        cv_results[name] = {
            'scores': scores,
            'mean_score': scores.mean(),
            'std_score': scores.std(),
            'cv_time': cv_time
        }
        
        # Hiển thị kết quả
        print(f"   ✓ Scores: {scores.round(4)}")
        print(f"   ✓ Mean score: {scores.mean():.4f} (±{scores.std():.4f})")
        print(f"   ✓ CV time: {cv_time:.2f}s")
    
    # Tìm model tốt nhất theo CV
    best_cv_model = max(cv_results.items(), key=lambda x: x[1]['mean_score'])
    
    print("\n" + "-" * 70)
    print(f"🏆 BEST MODEL (by CV): {best_cv_model[0]}")
    print(f"   Mean score: {best_cv_model[1]['mean_score']:.4f}")
    print(f"   Std deviation: {best_cv_model[1]['std_score']:.4f}")
    print("-" * 70)
    
    return cv_results


def run_ml_pipeline(X, y, test_size=0.2, random_state=42, model_mode='fast', sample_fraction=1.0, run_cv=True):
    """
    Chạy toàn bộ pipeline Machine Learning.

    Parameters:
    -----------
    X : DataFrame
        Ma trận features
    y : Series
        Vector nhãn
    test_size : float
        Tỷ lệ test set
    random_state : int
        Seed cho reproducibility
    model_mode : str
        Chế độ model: 'fast' hoặc 'full'
    sample_fraction : float
        Tỷ lệ mẫu dùng cho bước ML. 1.0 = dùng toàn bộ dữ liệu.

    Returns:
    --------
    dict: Kết quả training và model tốt nhất
    """
    # Có thể lấy mẫu một phần dữ liệu để tăng tốc độ train trên máy cá nhân
    if 0 < sample_fraction < 1.0:
        X_ml, _, y_ml, _ = train_test_split(
            X, y,
            train_size=sample_fraction,
            random_state=random_state,
            stratify=y
        )
        print(f"\n[ML] Dùng {sample_fraction*100:.0f}% dữ liệu cho huấn luyện mô hình để tăng tốc.")
    else:
        X_ml, y_ml = X, y
        print("\n[ML] Dùng 100% dữ liệu cho huấn luyện mô hình.")

    # Chia train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_ml, y_ml,
        test_size=test_size,
        random_state=random_state,
        stratify=y_ml
    )

    # Huấn luyện và đánh giá
    results = train_and_evaluate(
        X_train, X_test, y_train, y_test,
        model_mode=model_mode
    )

    # So sánh các model
    best_model = print_model_comparison(results)
    
    # Thực hiện Cross-Validation nếu được yêu cầu
    cv_results = None
    if run_cv:
        # Lấy các model để CV
        models = get_models(mode=model_mode)
        
        # Sử dụng một phần dữ liệu cho CV để tăng tốc
        if 0 < sample_fraction < 1.0:
            cv_results = perform_cross_validation(models, X_ml, y_ml, cv_folds=5)
        else:
            # Nếu dữ liệu lớn, có thể giảm số fold
            cv_results = perform_cross_validation(models, X_ml, y_ml, cv_folds=3)

    return {
        'results': results,
        'best_model_name': best_model[0],
        'best_model': best_model[1]['model'],
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'cv_results': cv_results
    }


# =============================================================================
# PHẦN 11: LƯU MODEL VÀ KẾT QUẢ
# =============================================================================
"""
Các hàm hỗ trợ lưu model, kết quả đánh giá và dữ liệu đã xử lý
để sử dụng lại sau này hoặc triển khai vào production.
"""

import joblib
from datetime import datetime

# Import module visualization nếu có
try:
    from visualization import create_all_visualizations
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("⚠ Module visualization không tìm thấy. Bỏ qua phần trực quan hóa.")

def save_model_and_results(model, results, output_dir='output'):
    """
    Lưu model đã train và kết quả đánh giá.
    
    Parameters:
    -----------
    model : sklearn model
        Model đã được huấn luyện
    results : dict
        Dictionary chứa kết quả đánh giá
    output_dir : str
        Thư mục lưu output
    """
    import os
    
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Lưu model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"{output_dir}/best_model_{timestamp}.pkl"
    joblib.dump(model, model_path)
    print(f"✓ Đã lưu model tại: {model_path}")
    
    # Lưu kết quả đánh giá
    results_path = f"{output_dir}/evaluation_results_{timestamp}.txt"
    with open(results_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH\n")
        f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        for model_name, metrics in results.items():
            f.write(f"\n{model_name}:\n")
            f.write(f"  - Accuracy:  {metrics['accuracy']:.4f}\n")
            f.write(f"  - Precision: {metrics['precision']:.4f}\n")
            f.write(f"  - Recall:    {metrics['recall']:.4f}\n")
            f.write(f"  - F1-Score:  {metrics['f1_score']:.4f}\n")
            if metrics['roc_auc']:
                f.write(f"  - ROC-AUC:   {metrics['roc_auc']:.4f}\n")
            f.write(f"  - Train time: {metrics['train_time']:.2f}s\n")
    
    print(f"✓ Đã lưu kết quả đánh giá tại: {results_path}")
    return model_path, results_path


def save_preprocessed_data(X, y, scaler, encoders, output_dir='output'):
    """
    Lưu dữ liệu đã tiền xử lý và các transformer.
    
    Parameters:
    -----------
    X : DataFrame
        Ma trận features đã xử lý
    y : Series
        Vector labels
    scaler : sklearn scaler
        Scaler đã fit
    encoders : dict
        Dictionary chứa các encoder
    output_dir : str
        Thư mục lưu output
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Lưu dữ liệu đã xử lý
    processed_df = pd.concat([X, y], axis=1)
    data_path = f"{output_dir}/processed_data_{timestamp}.csv"
    processed_df.to_csv(data_path, index=False)
    print(f"✓ Đã lưu dữ liệu đã xử lý tại: {data_path}")
    
    # Lưu scaler và encoders
    transformers = {
        'scaler': scaler,
        'encoders': encoders
    }
    transformers_path = f"{output_dir}/transformers_{timestamp}.pkl"
    joblib.dump(transformers, transformers_path)
    print(f"✓ Đã lưu transformers tại: {transformers_path}")
    
    return data_path, transformers_path


# =============================================================================
# PHẦN 12: CHẠY CHƯƠNG TRÌNH
# =============================================================================

if __name__ == "__main__":
    """
    Điểm bắt đầu của chương trình.
    Thay đổi đường dẫn file_path phù hợp với vị trí file dữ liệu của bạn.
    """

    # === CẤU HÌNH ===
    # Đường dẫn đến file dữ liệu (thay đổi theo vị trí file của bạn)
    FILE_PATH = "KDDTrain+.txt"  # File NSL-KDD đã tải

    # Phương pháp encoding: 'label' hoặc 'onehot'
    ENCODING_METHOD = 'label'

    # Phương pháp chuẩn hóa: 'standard' hoặc 'minmax'
    SCALING_METHOD = 'standard'

    # Có chạy huấn luyện ML ngay sau tiền xử lý hay không
    RUN_ML = True

    # Chế độ model:
    # - 'fast': nhanh hơn, phù hợp chạy trên máy cá nhân/M1
    # - 'full': đầy đủ model hơn, chạy lâu hơn
    ML_MODEL_MODE = 'fast'

    # Tỷ lệ dữ liệu dùng cho bước ML để tăng tốc:
    # - 1.0 = dùng toàn bộ dữ liệu
    # - 0.6 = dùng 60% dữ liệu cho ML (nhanh hơn)
    ML_SAMPLE_FRACTION = 0.6

    # === CHẠY PIPELINE ===
    try:
        results = preprocess_kdd_data(
            file_path=FILE_PATH,
            encoding_method=ENCODING_METHOD,
            scaling_method=SCALING_METHOD
        )

        if results is not None:
            print("\n✓ HOÀN TẤT TIỀN XỬ LÝ DỮ LIỆU!")
            print(f"   • X (features): {results['X'].shape}")
            print(f"   • y (labels):   {results['y'].shape}")

            if RUN_ML:
                # === CHẠY MACHINE LEARNING ===
                print("\n" + "=" * 70)
                print("BẮT ĐẦU HUẤN LUYỆN MÔ HÌNH MACHINE LEARNING")
                print("=" * 70)

                ml_results = run_ml_pipeline(
                    X=results['X'],
                    y=results['y'],
                    test_size=0.2,
                    random_state=42,
                    model_mode=ML_MODEL_MODE,
                    sample_fraction=ML_SAMPLE_FRACTION
                )

                print("\n" + "=" * 70)
                print("✓ HOÀN TẤT TOÀN BỘ QUY TRÌNH!")
                print("=" * 70)
                print(f"\n📁 Dữ liệu đã xử lý:")
                print(f"   • X (features): {results['X'].shape}")
                print(f"   • y (labels): {results['y'].shape}")
                print(f"\n🤖 Model tốt nhất: {ml_results['best_model_name']}")
                print(f"   • Accuracy: {ml_results['results'][ml_results['best_model_name']]['accuracy']*100:.2f}%")
                print(f"   • Chế độ model: {ML_MODEL_MODE}")
                print(f"   • Sample fraction: {ML_SAMPLE_FRACTION}")

                # Tự động lưu kết quả
                print("\n" + "=" * 70)
                print("LƯU KẾT QUẢ")
                print("=" * 70)
                
                # Lưu model tốt nhất và kết quả đánh giá
                model_path, results_path = save_model_and_results(
                    ml_results['best_model'],
                    ml_results['results']
                )
                
                # Lưu dữ liệu đã xử lý và transformers
                data_path, transformers_path = save_preprocessed_data(
                    results['X'],
                    results['y'],
                    results['scaler'],
                    results['encoders']
                )
                
                # Tạo visualizations nếu module có sẵn
                if VISUALIZATION_AVAILABLE:
                    create_all_visualizations(
                        ml_results['results'],
                        ml_results['X_test'],
                        ml_results['y_test'],
                        results['feature_names'],
                        ml_results['best_model']
                    )
            else:
                print("\n[INFO] Bỏ qua bước huấn luyện ML (RUN_ML=False).")
                print("[INFO] Đổi RUN_ML=True nếu bạn muốn train model ngay trong script.")

    except Exception as e:
        print(f"\n✗ Lỗi trong quá trình xử lý: {str(e)}")
        import traceback
        traceback.print_exc()
