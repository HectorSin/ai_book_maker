import os
import csv
import json

def ensure_dir_exists(directory):
    """디렉토리가 존재하는지 확인하고, 없으면 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return directory

def get_unique_dirname(base_dir):
    """중복되지 않는 디렉토리명을 생성"""
    counter = 1
    dir_path = f"{base_dir}_01"
    while os.path.exists(dir_path):
        dir_path = f"{base_dir}_{counter:02d}"
        counter += 1
    return dir_path

def create_csv_log(csv_path, headers=None):
    """CSV 로그 파일 생성"""
    if headers is None:
        headers = ['파일명', 'OCR 상태', 'GPT 상태', 'Claude 상태', '처리 경로']
    
    # 디렉토리 확인
    ensure_dir_exists(os.path.dirname(csv_path))
    
    # 파일이 존재하지 않을 경우에만 헤더 작성
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    
    return csv_path

def update_csv_status(csv_path, *args):
    """CSV에 처리 상태 업데이트"""
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(args)

def save_json(data, file_path):
    """JSON 데이터 저장"""
    ensure_dir_exists(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(file_path):
    """JSON 파일 로드"""
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)