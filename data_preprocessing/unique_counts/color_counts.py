import pandas as pd

# CSV 파일 경로 설정
input_csv_file = '../preprocessing_csv_files/nonglim_color_preprocessing.csv'

# CSV 파일 읽기
df = pd.read_csv(input_csv_file)

# '색상' 컬럼에서 중복되지 않는 값과 각 값의 개수 추출
unique_color_counts = df['색상'].value_counts().reset_index()
unique_color_counts.columns = ['색상', '개수']

# 중복되지 않는 '색상' 종류 총 개수 계산
total_unique_breeds = len(unique_color_counts)
print(f"중복되지 않는 '색상'의 종류 총 개수: {total_unique_breeds}\n")

# 중복되지 않는 '색상'과 개수 출력
print("중복되지 않는 '색상'과 각 개수:")
print(unique_color_counts.to_string(index=False))