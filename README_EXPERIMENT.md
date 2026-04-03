# HUONG DAN THUC NGHIEM HE THONG PHAT HIEN XAM NHAP MANG

Tai lieu nay duoc viet lai de dung cho phan mo ta thuc nghiem trong bao cao, dong thoi bam sat hanh vi thuc te cua code trong repo. Noi dung ben duoi tuong ung truc tiep voi cac muc:

- Chuong 4: Phuong phap thuc hien
- Muc 4.1: Tong quan quy trinh thuc nghiem
- Muc 4.2: Huong dan cai dat va chay thuc nghiem
- Chuong 5: Ket qua thuc nghiem

## 1. Muc dich tai lieu

Tai lieu nay huong dan cach tai lap toan bo quy trinh thuc nghiem cho bai toan Network Intrusion Detection System su dung bo du lieu NSL-KDD, tu khau chuan bi moi truong, chay script, thu duoc artifact, doi chieu ket qua voi bao cao, den cach trich xuat thong tin de dua vao tai lieu hoc thuat.

Pham vi cua tai lieu:

- Chay pipeline thuc nghiem bang `main_experiment.py`
- Mo ta dung cac buoc tien xu ly, huan luyen, danh gia va luu ket qua
- Liet ke artifact sinh ra sau moi lan chay
- Dua ra cac cau hinh de tai lap ket qua giong bao cao
- Ho tro viet phan "thuc nghiem" trong bao cao/luan van

## 2. Cac file lien quan den thuc nghiem

Phan thuc nghiem trong repo hien tai xoay quanh cac file sau:

- `main_experiment.py`: script chinh de thuc thi pipeline tu dau den cuoi
- `nsl_kdd_preprocessing.py`: module load du lieu, lam sach, ma hoa va chuan hoa
- `visualization.py`: module tao cac bieu do so sanh mo hinh
- `predict_new_sample.py`: module suy dien tren mau moi sau khi da co model
- `requirements.txt`: danh sach thu vien can cai dat
- `output/`: noi luu toan bo artifact sau thuc nghiem

## 3. Moi truong thuc nghiem de xuat

Phan nay duoc canh theo noi dung trong bao cao va da duoc doi chieu voi code hien tai.

### 3.1. Cau hinh phan cung khuyen nghi

- CPU: Apple M1/M2/M3 hoac Intel Core i5 tro len
- RAM: toi thieu 8GB, khuyen nghi 16GB
- O cung: toi thieu 5GB trong
- GPU: khong bat buoc

### 3.2. Cau hinh phan mem

- He dieu hanh: macOS 12+, Ubuntu 20.04+, Windows 10+
- Python: 3.8 tro len
- Moi truong ao: `venv` hoac Conda
- Git: de quan ly ma nguon

### 3.3. Luu y rieng cho repo nay

Code hien tai co toi uu nhe cho Apple Silicon thong qua bien moi truong `LOKY_MAX_CPU_COUNT`, giup tranh mot so warning cua `joblib/loky` khi chay cross-validation va cac model su dung da luong.

## 4. Du lieu dau vao

### 4.1. Bo du lieu su dung

He thong su dung tap `NSL-KDD Train+`, ten file dau vao trong project la:

```text
KDDTrain+.txt
```

Tap nay duoc dung trong toan bo pipeline de:

- load du lieu goc
- lam sach ban ghi
- dua nhan ve bai toan nhi phan `Normal` va `Attack`
- train/test split theo ti le stratified
- huan luyen 4 mo hinh machine learning

### 4.2. Dac diem du lieu

Theo pipeline hien tai:

- so mau goc: 125,973
- so thuoc tinh dau vao: 41
- cot nhan: `label`
- mot so ban NSL-KDD co them cot `difficulty_level`; code se tu dong bo cot nay neu phat hien
- mot so nhan co dau cham o cuoi, code se tu dong chuan hoa

### 4.3. Cach dat file

File du lieu phai nam o thu muc goc cua project:

```text
BTL_KPDL/
├── KDDTrain+.txt
├── main_experiment.py
└── ...
```

Neu file khong nam dung vi tri, script se dung va bao loi `FileNotFoundError`.

## 5. Workflow thuc nghiem tong the

Quy trinh thuc nghiem trong code duoc to chuc theo pipeline tuan tu, tuong ung voi phan workflow trong bao cao:

1. Load file NSL-KDD tu `KDDTrain+.txt`
2. Kiem tra va xu ly missing values
3. Loai bo duplicate records
4. Chuyen doi bai toan ve phan loai nhi phan
5. Label encoding cho 3 cot categorical:
   - `protocol_type`
   - `service`
   - `flag`
6. Chia train/test theo stratified split
7. Chuan hoa dac trung bang `StandardScaler`
8. Huan luyen 4 mo hinh:
   - Decision Tree
   - Random Forest
   - Logistic Regression
   - Hist Gradient Boosting
9. Danh gia tren tap test bang cac chi so:
   - Accuracy
   - Precision
   - Recall
   - F1-Score
   - ROC-AUC
   - Confusion Matrix
   - Cross-validation mean/std
10. So sanh va chon mo hinh tot nhat
11. Tao artifact phuc vu bao cao va tai su dung
12. Luu model, transformers, file ket qua va bieu do

## 6. Cai dat moi truong

### 6.1. Clone ma nguon

```bash
git clone <repository-url>
cd BTL_KPDL
```

### 6.2. Tao va kich hoat moi truong ao

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 6.3. Cai dat dependency

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6.4. Kiem tra cai dat

```bash
python -c "import sklearn, pandas, matplotlib, seaborn, joblib; print('Environment OK')"
```

Neu can doi chieu voi bao cao, co the kiem tra rieng phien ban `scikit-learn`:

```bash
python -c "import sklearn; print(sklearn.__version__)"
```

## 7. Chuan bi du lieu

### 7.1. Cach lay du lieu

Ban co the download NSL-KDD bang mot trong hai cach:

Cach 1, tai truc tiep:

```bash
wget https://github.com/defcom17/NSL_KDD/raw/master/KDDTrain%2B.txt -O KDDTrain+.txt
```

Cach 2, tai thu cong:

- Trang chinh thuc: https://www.unb.ca/cic/datasets/nsl.html

### 7.2. Kiem tra file sau khi tai

```bash
ls -lh KDDTrain+.txt
```

Ky vong:

- file ton tai trong thu muc goc project
- kich thuoc xap xi 18MB

## 8. Chay thuc nghiem chinh

Sau khi moi truong va du lieu da san sang, script chinh can chay la:

```bash
python main_experiment.py
```

### 8.1. Cau hinh mac dinh cua script

Neu khong truyen tham so, script hien tai se chay voi cau hinh:

- `sample_fraction = 0.6`
- `test_size = 0.2`
- `cv_folds = 5`
- `random_state = 42`
- `mode = standard`

Day la cau hinh phu hop de tai lap ket qua bao cao tren may ca nhan ma khong qua ton thoi gian.

### 8.2. Cac lenh thuc nghiem khop voi bao cao

Lenh mac dinh:

```bash
python main_experiment.py
```

Lenh tang muc do tai lap, dung toan bo du lieu mau va tang so fold:

```bash
python main_experiment.py --sample-fraction 1.0 --cv-folds 10
```

Lenh cho may yeu hoac khi can chay nhanh:

```bash
python main_experiment.py --mode fast --sample-fraction 0.3
```

Co the chi dinh ro hon seed va ti le chia tap du lieu:

```bash
python main_experiment.py --sample-fraction 0.6 --cv-folds 5 --test-size 0.2 --random-state 42
```

### 8.3. Y nghia cua cac tham so CLI

- `--sample-fraction`: ti le lay mau du lieu truoc khi train
- `--cv-folds`: so fold cho cross-validation
- `--test-size`: ti le tap test
- `--random-state`: seed de tai lap ket qua
- `--mode standard`: cau hinh mo hinh dung cho thuc nghiem day du
- `--mode fast`: giam do phuc tap hyperparameter de rut ngan thoi gian train

### 8.4. Thoi gian chay du kien

Thoi gian chay phu thuoc vao may va backend ve bieu do, nhung co the tham khao:

- `sample_fraction = 0.3`, `mode = fast`: khoang 2 den 4 phut
- `sample_fraction = 0.6`, `mode = standard`: khoang 3 den 6 phut
- `sample_fraction = 1.0`, `cv_folds = 10`: lau hon dang ke, co the 8 den 15 phut

## 9. Dien giai output tren terminal

Khi chay thanh cong, terminal se hien cac khoi thong tin lon theo dung thu tu pipeline.

### 9.1. Header cau hinh

Script se in ra:

- timestamp cua lan chay
- output directory
- random state
- test size
- so fold cross-validation
- sample fraction
- model mode

### 9.2. Buoc 1: Load va tien xu ly

Buoc nay bao gom:

- kiem tra file du lieu
- load vao DataFrame
- in thong tin tong quan va phan bo nhan
- cleaning
- sampling neu `sample_fraction < 1.0`
- transform nhan ve `0` va `1`
- encode categorical feature
- train/test split co stratify
- standard scaling
- luu `processed_data_*.csv`
- luu `transformers_*.pkl`

### 9.3. Buoc 2: Khoi tao cac mo hinh

Script khoi tao 4 mo hinh:

- Decision Tree
- Random Forest
- Logistic Regression
- Hist Gradient Boosting

### 9.4. Buoc 3: Training va evaluation

Moi mo hinh se duoc:

- train tren tap train
- predict tren tap test
- tinh Accuracy, Precision, Recall, F1-Score, ROC-AUC
- tao confusion matrix
- thuc hien cross-validation

### 9.5. Buoc 4: So sanh va chon mo hinh tot nhat

Ket qua duoc dua vao bang so sanh, sau do script:

- sap xep theo Accuracy giam dan
- chon mo hinh tot nhat
- tinh False Positive Rate
- tinh False Negative Rate

### 9.6. Buoc 5: Visualization

Neu thu vien do hoa da du, script se luu:

- `model_comparison.png`
- `confusion_matrices.png`
- `roc_curves.png`
- `feature_importance_decision_tree.png`
- `feature_importance_random_forest.png`

Luu y:

- feature importance chi duoc tao cho mo hinh co `feature_importances_`
- Hist Gradient Boosting trong pipeline nay khong tao file feature importance

### 9.7. Buoc 6: Luu ket qua

Script se luu:

- model tot nhat
- file evaluation chi tiet
- file summary phuc vu tong hop nhanh

## 10. Artifact sinh ra sau moi lan chay

Tat ca artifact duoc luu trong thu muc `output/`.

| File/Thu muc | Y nghia | Cach dung trong bao cao |
|---|---|---|
| `output/processed_data_<timestamp>.csv` | Du lieu train sau tien xu ly | Chung minh quy trinh preprocessing da thuc thi |
| `output/transformers_<timestamp>.pkl` | Chua scaler va label encoders | Dung lai cho prediction tren du lieu moi |
| `output/best_model_<timestamp>.pkl` | Model tot nhat sau so sanh | Mo hinh trien khai hoac demo |
| `output/evaluation_results_<timestamp>.txt` | Tong hop metric tung mo hinh | Dua vao phan ket qua thuc nghiem |
| `output/summary_<timestamp>.txt` | Ban tom tat nhanh | Trich dan vao phan ket luan nho |
| `output/visualizations/model_comparison.png` | So sanh metric giua cac model | Hinh minh hoa trong chuong ket qua |
| `output/visualizations/confusion_matrices.png` | Confusion matrix cua tat ca model | Dung trong phan phan tich loi |
| `output/visualizations/roc_curves.png` | ROC curve cua cac model | Dung de phan tich kha nang phan tach |
| `output/visualizations/feature_importance_*.png` | Do quan trong dac trung cua mo hinh cay | Dung trong phan giai thich mo hinh |

## 11. Doi chieu voi ket qua bao cao

Ket qua ky vong cho cau hinh thuc nghiem chuan duoc doi chieu tu bao cao va artifact dang co trong repo:

| Model | Accuracy xap xi | Ghi chu |
|---|---|---|
| Decision Tree | 99.76% | Tot, nhanh, de giai thich |
| Random Forest | 99.83% | On dinh, feature importance ro |
| Logistic Regression | 95.44% | Lam baseline tuyen tinh |
| Hist Gradient Boosting | 99.85% | Mo hinh tot nhat |

Repo hien dang co mot ket qua mau da luu:

```text
output/evaluation_results_20260324_215031.txt
```

Trong file nay:

- Decision Tree: Accuracy `0.9976`
- Random Forest: Accuracy `0.9983`
- Logistic Regression: Accuracy `0.9544`
- Hist Gradient Boosting: Accuracy `0.9985`

Neu ban chay lai voi cung dataset, cung `random_state` va cau hinh tuong duong, ket qua thu duoc se rat gan cac gia tri tren. Sai khac nho co the xuat hien do:

- phien ban thu vien
- so luong du lieu lay mau
- backend tinh toan tren tung may

## 12. Dien giai cac chi so danh gia

### 12.1. Accuracy

Ti le du doan dung tren toan bo tap test. Day la chi so chinh duoc dung de xep hang model trong script.

### 12.2. Precision

Do chinh xac khi he thong ket luan mot mau la tan cong.

### 12.3. Recall

Ti le phat hien dung cac mau tan cong. Chi so nay quan trong trong IDS vi bo sot tan cong thuong ton kem hon bao dong gia.

### 12.4. F1-Score

Trung hoa giua Precision va Recall. Dung de danh gia tong quan khi can can bang hai muc tieu.

### 12.5. ROC-AUC

Danh gia kha nang tach biet giua hai lop `Normal` va `Attack`. Gia tri cang gan `1.0` cang tot.

### 12.6. FPR va FNR

Script tinh them hai chi so nay cho mo hinh tot nhat:

- FPR: bao nham luu luong binh thuong thanh tan cong
- FNR: bo sot mau tan cong

Trong bai toan IDS, can theo doi dong thoi Accuracy, FPR va FNR thay vi chi nhin moi Accuracy.

## 13. Tuy chinh thuc nghiem

### 13.1. Khi muon chay nhanh

```bash
python main_experiment.py --mode fast --sample-fraction 0.3
```

Phu hop khi:

- may co RAM han che
- can test nhanh truoc khi chay full
- can demo trong thoi gian ngan

### 13.2. Khi muon do on dinh cao hon

```bash
python main_experiment.py --sample-fraction 1.0 --cv-folds 10
```

Phu hop khi:

- can dua ket qua vao bao cao cuoi cung
- can kiem tra do on dinh cua model
- can giam anh huong do sampling

### 13.3. Khi muon doi phuong an chia train/test

```bash
python main_experiment.py --test-size 0.3
```

### 13.4. Khi muon tai lap chinh xac mot lan chay

Ghi lai day du:

- lenh da su dung
- timestamp sinh ra trong terminal
- ten file artifact trong `output/`
- random state
- sample fraction
- cv folds

## 14. Troubleshooting

### 14.1. Loi khong tim thay file du lieu

Trieu chung:

```text
FileNotFoundError: Khong tim thay file du lieu: KDDTrain+.txt
```

Khac phuc:

- kiem tra file co dung ten `KDDTrain+.txt`
- dat file o thu muc goc project
- chay lai lenh `ls -lh KDDTrain+.txt`

### 14.2. Loi thieu thu vien

Trieu chung:

```text
ModuleNotFoundError: No module named 'sklearn'
```

Khac phuc:

```bash
pip install -r requirements.txt
```

Neu van loi:

```bash
pip install --upgrade --force-reinstall scikit-learn pandas matplotlib seaborn joblib
```

### 14.3. Chay cham hoac ton RAM

Khac phuc khuyen nghi:

```bash
python main_experiment.py --mode fast --sample-fraction 0.3
```

Neu can giam them:

```bash
python main_experiment.py --mode fast --sample-fraction 0.2 --cv-folds 3
```

### 14.4. Khong thay file bieu do

Sau khi chay xong, kiem tra:

```bash
ls -lh output/visualizations
```

Neu thu muc rong:

- dam bao `matplotlib` va `seaborn` da duoc cai
- chay lai script sau khi kich hoat dung moi truong ao

### 14.5. Script dung o phan ve bieu do tren moi truong khong co GUI

Trong moi truong headless, co the chay:

```bash
MPLBACKEND=Agg python main_experiment.py
```

## 15. Goi y viet vao bao cao

Neu ban can dua quy trinh nay vao phan "Mo ta thuc nghiem", mot doan ngan gon co the viet theo khuon sau:

1. Moi truong thuc nghiem:
   Python 3.8+, RAM 8GB+, dataset NSL-KDD Train+, train/test split 80/20.
2. Tien xu ly:
   Loai bo duplicate, xu ly missing values, chuyen nhan ve bai toan nhi phan, label encoding cho 3 cot categorical va standard scaling.
3. Mo hinh:
   Decision Tree, Random Forest, Logistic Regression va Hist Gradient Boosting.
4. Danh gia:
   Accuracy, Precision, Recall, F1-Score, ROC-AUC, confusion matrix va 5-fold cross-validation.
5. Ket qua:
   Hist Gradient Boosting dat hieu nang cao nhat, accuracy xap xi 99.85%.

## 16. Checklist truoc khi dua vao tai lieu

Truoc khi chot phan tai lieu, nen xac nhan:

- da ghi ro cau hinh may va phien ban Python
- da ghi ro lenh thuc nghiem da su dung
- da neu ro `sample_fraction`, `cv_folds`, `test_size`, `random_state`
- da trich dan dung model tot nhat
- da dinh kem bang metric
- da co confusion matrix hoac ROC curve neu can hinh minh hoa
- da luu timestamp cua lan chay de doi chieu artifact

## 17. Ket luan

`README_EXPERIMENT.md` nay co the duoc dung nhu tai lieu van hanh thuc nghiem cua do an. Neu can ban viet bao cao hoc thuat, hay uu tien trich thong tin tu:

- output metric thuc te trong `output/evaluation_results_<timestamp>.txt`
- hinh anh trong `output/visualizations/`
- cau hinh chay thuc nghiem da luu trong terminal va lenh CLI

Voi phien ban code hien tai, cac lenh thuc nghiem trong bao cao da duoc ho tro truc tiep thong qua CLI cua `main_experiment.py`, va cac artifact hinh anh/ket qua duoc luu dung thu muc de dua vao tai lieu.
