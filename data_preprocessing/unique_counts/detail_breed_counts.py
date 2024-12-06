import pandas as pd

# CSV 파일 경로 설정
input_csv_file = '../preprocessing_csv_files/nonglim_breed_preprocessing.csv'

# CSV 파일 읽기
df = pd.read_csv(input_csv_file)

# '세부견종' 컬럼에서 중복되지 않는 값과 각 값의 개수 추출
unique_dbreed_counts = df['세부견종'].value_counts().reset_index()
unique_dbreed_counts.columns = ['세부견종', '개수']

# 중복되지 않는 '세부견종' 종류 총 개수 계산
total_unique_dbreeds = len(unique_dbreed_counts)
print(f"중복되지 않는 '세부견종'의 종류 총 개수: {total_unique_dbreeds}\n")

# 중복되지 않는 '세부견종'과 개수 출력
print("중복되지 않는 '세부견종'과 각 개수:")
print(unique_dbreed_counts.to_string(index=False))