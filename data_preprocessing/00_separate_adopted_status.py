import pandas as pd

# CSV 파일 경로 설정
input_csv_file = '../resource/result_all_data.csv'
output_csv_file_adopted = 'preprocessing_csv_files/test_final_adopted_data.csv.csv'
output_csv_file_unadopted = 'preprocessing_csv_files/test_final_unadopted_data.csv'

# CSV 파일 읽기
data = pd.read_csv(input_csv_file, encoding='euc-kr')

# '입양여부' 컬럼의 결측치 개수 확인
missing_values = data['입양여부'].isnull().sum()
print(f"'입양여부' 컬럼의 결측치 개수: {missing_values}")

# 결측치 제거
data = data.dropna(subset=['입양여부'])

# 입양된 데이터 필터링
adopted_data = data[data['입양여부'].str.contains('Y')].copy()

# 입양되지 않은 데이터 필터링
unadopted_data = data[data['입양여부'].str.contains('N')].copy()

# 입양된 데이터와 입양되지 않은 데이터를 각각 새로운 CSV 파일로 저장
adopted_data.to_csv(output_csv_file_adopted, encoding='utf-8-sig', index=False)
unadopted_data.to_csv(output_csv_file_unadopted, encoding='utf-8-sig', index=False)

# 각 데이터셋의 개수 출력
num_adopted = len(adopted_data)
num_unadopted = len(unadopted_data)
print(f'입양된(Y) 강아지의 수: {num_adopted}개')
print(f'입양되지 않은(N) 강아지의 수: {num_unadopted}개')