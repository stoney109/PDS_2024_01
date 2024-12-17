import pandas as pd

# CSV 파일 경로 설정
input_csv_file = '../../resource/crawling_data/nonglim_crawling_20231116.csv'

# CSV 파일 읽기
df = pd.read_csv(input_csv_file)

# '입양여부' 컬럼에서 중복되지 않는 값과 각 값의 개수 추출
unique_color_counts = df['입양여부'].value_counts().reset_index()
unique_color_counts.columns = ['입양여부', '개수']

# 중복되지 않는 '입양여부' 종류 총 개수 계산
total_unique_breeds = len(unique_color_counts)
print(f"중복되지 않는 '입양여부'의 종류 총 개수: {total_unique_breeds}\n")

# 중복되지 않는 '입양여부'과 개수 출력
print("중복되지 않는 '입양여부'과 각 개수:")
print(unique_color_counts.to_string(index=False))